# ─────────────────────────────────────────────
# TRACING — must be the very first import,
# before Flask and everything else.
# ddtrace auto-instruments Flask, logging,
# and all outgoing HTTP calls automatically.
# No manual span creation needed.
# ─────────────────────────────────────────────
from ddtrace import patch_all, tracer, patch
patch_all()
patch(logging=True)

from flask import Flask, jsonify, request
import time
import random
import logging
import os

os.makedirs("logs", exist_ok=True)

# ─────────────────────────────────────────────
# Logging format — now includes dd.trace_id
# and dd.span_id injected by ddtrace.
# This is what connects your logs to traces
# in Datadog Log Management automatically.
# Format must include %(dd.trace_id)s and
# %(dd.span_id)s for correlation to work.
# ─────────────────────────────────────────────
LOG_FORMAT = (
    "%(asctime)s %(levelname)s "
    "dd.trace_id=%(dd.trace_id)s "
    "dd.span_id=%(dd.span_id)s "
    "%(message)s"
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
print("***** CUSTOM FLASK APP LOADED *****")

# ─────────────────────────────────────────────
# Global chaos configuration
# Controlled via POST /chaos or POST /scenarios
# Applies to /service and /slow only
# /error has its own fixed 30% failure rate
# ─────────────────────────────────────────────
chaos_config = {
    "error_rate": 0,
    "latency_ms": 0
}

SCENARIOS = {
    "fast_burn": {
        "error_rate": 50,
        "latency_ms": 0,
        "description": "P1 trigger — 50% errors, rapid budget drain"
    },
    "slow_burn": {
        "error_rate": 5,
        "latency_ms": 0,
        "description": "P2 trigger — 5% errors, gradual drain threshold misses"
    },
    "latency_spike": {
        "error_rate": 0,
        "latency_ms": 800,
        "description": "P3 trigger — high latency no errors"
    },
    "combined": {
        "error_rate": 20,
        "latency_ms": 500,
        "description": "Realistic degradation — errors AND latency together"
    }
}


def apply_chaos():
    """
    Apply configured latency and random error injection.
    Returns True if this request should fail (500).
    """
    if chaos_config["latency_ms"] > 0:
        time.sleep(chaos_config["latency_ms"] / 1000)

    if chaos_config["error_rate"] > 0:
        if random.randint(1, 100) <= chaos_config["error_rate"]:
            return True

    return False


def log_request(endpoint, status_code, latency_ms):
    """
    Structured log line for every request.
    ddtrace automatically injects dd.trace_id
    and dd.span_id into this log line via the
    LOG_FORMAT above — connecting every log
    entry to its trace in Datadog APM.
    """
    is_error = 1 if status_code >= 500 else 0

    # ── add trace context to current span ──────
    # This tags the active APM span with endpoint,
    # status, and error info so you can filter
    # traces by these values in Datadog APM.
    span = tracer.current_span()
    if span:
        span.set_tag("http.endpoint", endpoint)
        span.set_tag("http.status_code", status_code)
        span.set_tag("is_error", is_error)
        if status_code >= 500:
            span.error = 1   # marks span red in Datadog

    logger.info(
        f"endpoint={endpoint} "
        f"status={status_code} "
        f"latency_ms={latency_ms:.2f} "
        f"is_error={is_error}"
    )


# ─────────────────────────────────────────────
# /health
# ─────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    start = time.time()
    latency = round((time.time() - start) * 1000, 2)
    log_request("/health", 200, latency)
    return jsonify({
        "status": "healthy",
        "chaos_active": (
            chaos_config["error_rate"] > 0
            or chaos_config["latency_ms"] > 0
        )
    }), 200


# ─────────────────────────────────────────────
# /service
# ─────────────────────────────────────────────
@app.route("/service", methods=["GET"])
def service():
    start = time.time()
    failed = apply_chaos()
    latency = round((time.time() - start) * 1000, 2)

    if failed:
        log_request("/service", 500, latency)
        return jsonify({
            "error": "Simulated Service Failure",
            "chaos_config": chaos_config
        }), 500

    log_request("/service", 200, latency)
    return jsonify({
        "message": "Service Running",
        "latency_ms": latency
    }), 200


# ─────────────────────────────────────────────
# /slow
# ddtrace will show the 2s sleep as a long
# span duration in the trace flame graph —
# visually demonstrating latency degradation.
# ─────────────────────────────────────────────
@app.route("/slow", methods=["GET"])
def slow():
    start = time.time()
    time.sleep(2)
    failed = apply_chaos()
    latency = round((time.time() - start) * 1000, 2)

    if failed:
        log_request("/slow", 500, latency)
        return jsonify({
            "error": "Simulated Slow Service Failure",
            "latency_ms": latency
        }), 500

    log_request("/slow", 200, latency)
    return jsonify({
        "message": "Slow Response",
        "latency_ms": latency
    }), 200


# ─────────────────────────────────────────────
# /error
# ─────────────────────────────────────────────
@app.route("/error", methods=["GET"])
def error():
    start = time.time()

    if random.randint(1, 100) <= 30:
        latency = round((time.time() - start) * 1000, 2)
        log_request("/error", 500, latency)
        return jsonify({
            "error": "Simulated Internal Error",
            "failure_rate": "30% fixed"
        }), 500

    latency = round((time.time() - start) * 1000, 2)
    log_request("/error", 200, latency)
    return jsonify({
        "message": "Success",
        "failure_rate": "30% fixed"
    }), 200


# ─────────────────────────────────────────────
# /chaos (POST)
# ─────────────────────────────────────────────
@app.route("/chaos", methods=["POST"])
def chaos():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body required",
            "example": {"error_rate": 30, "latency_ms": 500}
        }), 400

    error_rate = data.get("error_rate", 0)
    latency_ms = data.get("latency_ms", 0)

    if not (0 <= error_rate <= 100):
        return jsonify({
            "error": "error_rate must be between 0 and 100"
        }), 400

    if latency_ms < 0:
        return jsonify({
            "error": "latency_ms must be 0 or greater"
        }), 400

    chaos_config["error_rate"] = error_rate
    chaos_config["latency_ms"] = latency_ms

    logger.info(
        f"chaos_updated error_rate={error_rate} "
        f"latency_ms={latency_ms}"
    )

    return jsonify({
        "message": "Chaos configuration updated",
        "current_config": chaos_config
    }), 200


# ─────────────────────────────────────────────
# /chaos (GET)
# ─────────────────────────────────────────────
@app.route("/chaos", methods=["GET"])
def get_chaos():
    return jsonify({
        "current_config": chaos_config,
        "chaos_active": (
            chaos_config["error_rate"] > 0
            or chaos_config["latency_ms"] > 0
        )
    }), 200


# ─────────────────────────────────────────────
# /reset (POST)
# ─────────────────────────────────────────────
@app.route("/reset", methods=["POST"])
def reset():
    chaos_config["error_rate"] = 0
    chaos_config["latency_ms"] = 0
    logger.info("chaos_reset all values cleared")
    return jsonify({
        "message": "Chaos configuration reset",
        "current_config": chaos_config
    }), 200


# ─────────────────────────────────────────────
# /scenarios (GET)
# ─────────────────────────────────────────────
@app.route("/scenarios", methods=["GET"])
def list_scenarios():
    return jsonify({
        "available_scenarios": SCENARIOS,
        "usage": "POST /scenarios/<name> to apply"
    }), 200


# ─────────────────────────────────────────────
# /scenarios/<name> (POST)
# ─────────────────────────────────────────────
@app.route("/scenarios/<name>", methods=["POST"])
def apply_scenario(name):
    if name not in SCENARIOS:
        return jsonify({
            "error": f"Unknown scenario: '{name}'",
            "available": list(SCENARIOS.keys())
        }), 404

    scenario = SCENARIOS[name]
    chaos_config["error_rate"] = scenario["error_rate"]
    chaos_config["latency_ms"] = scenario["latency_ms"]

    logger.info(
        f"scenario_applied name={name} "
        f"error_rate={scenario['error_rate']} "
        f"latency_ms={scenario['latency_ms']}"
    )

    return jsonify({
        "message": f"Scenario '{name}' applied",
        "current_config": chaos_config,
        "description": scenario["description"]
    }), 200


# ─────────────────────────────────────────────
# /
# ─────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "SLO Reliability Test Service",
        "version": "1.2",
        "tracing": "ddtrace APM enabled",
        "endpoints": {
            "/health":           "Uptime check — no chaos",
            "/service":          "Primary traffic — chaos applies",
            "/slow":             "Latency sim — 2s base + chaos",
            "/error":            "Fixed 30% failure — chaos independent",
            "/chaos":            "GET current config / POST to update",
            "/reset":            "POST to clear all chaos config",
            "/scenarios":        "GET list of available scenarios",
            "/scenarios/<name>": "POST to apply a named scenario"
        }
    }), 200


print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8080)