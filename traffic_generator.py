import requests
import random
import time
from datadog import statsd

# ─────────────────────────────────────────────
# Must match app.py host and port exactly.
# Using 127.0.0.1 not localhost — avoids
# Windows socket resolution issues.
# ─────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:8080"

# ─────────────────────────────────────────────
# Traffic distribution weights (must sum to 100)
# /service → 75%  primary healthy traffic
# /slow    → 15%  latency simulation traffic
# /error   →  5%  fixed-failure traffic
# /health  →  5%  uptime check traffic
# ─────────────────────────────────────────────
ENDPOINTS = [
    ("/service", 75),
    ("/slow",    15),
    ("/error",    5),
    ("/health",   5),
]


def choose_endpoint():
    """
    Weighted random endpoint selection.
    Produces realistic traffic distribution.
    """
    rand = random.randint(1, 100)
    cumulative = 0

    for endpoint, weight in ENDPOINTS:
        cumulative += weight
        if rand <= cumulative:
            return endpoint

    return "/service"


def classify_endpoint(endpoint):
    """
    Returns clean tag-safe name for each endpoint.
    Used as Datadog metric tag for per-endpoint
    filtering in SLO and dashboard queries.
    """
    mapping = {
        "/service": "service",
        "/slow":    "slow",
        "/error":   "error",
        "/health":  "health",
    }
    return mapping.get(endpoint, "unknown")


def emit_metrics(endpoint_tag, status_code, latency_ms):
    """
    Send four metrics to Datadog via StatsD.
    All tagged with endpoint + status so Datadog
    can filter and split per dimension.

    Metrics emitted:
      service.request.count     — total requests (counter)
      service.response_time_ms  — latency in ms (gauge)
      service.error_rate        — 1=error 0=success (gauge)
                                  consumed directly by SLO monitors
      service.success.count     — successful requests (counter)
      service.failure.count     — failed requests (counter)

    Tags on every metric:
      endpoint:<name>           — which endpoint was called
      status:<code>             — exact HTTP status code
      status_class:<2xx|5xx>    — coarse class for SLO queries
    """
    is_error = 1 if status_code >= 500 else 0
    status_class = "5xx" if status_code >= 500 else "2xx"

    tags = [
        f"endpoint:{endpoint_tag}",
        f"status:{status_code}",
        f"status_class:{status_class}",
    ]

    # Total requests — every hit regardless of outcome
    statsd.increment("service.request.count", tags=tags)

    # Response time in milliseconds
    statsd.gauge("service.response_time_ms", latency_ms, tags=tags)

    # Binary error flag — what SLO monitors consume
    statsd.gauge("service.error_rate", is_error, tags=tags)

    # Split counters for dashboard widgets
    if is_error:
        statsd.increment("service.failure.count", tags=tags)
    else:
        statsd.increment("service.success.count", tags=tags)

    # ---------------------------------------------------
# Latency SLI Metrics
# Count requests meeting the latency objective.
# Only the primary service endpoint contributes
# to the latency SLO.
# ---------------------------------------------------
    if endpoint_tag == "service":
        if latency_ms < 300:
            statsd.increment(
                "service.latency.good.count",
                tags=tags
            )
    else:
        statsd.increment(
            "service.latency.bad.count",
            tags=tags
        )


def generate_traffic():
    """
    Continuous traffic loop.
    Sends requests to the Flask API at variable
    rate (0.5–2s between requests) to simulate
    realistic traffic variance.

    Emits Datadog metrics after every request.
    Prints structured console output.

    Run in a separate terminal from app.py.
    Keep running throughout all project phases.

    Phase 3 tip: while this is running, use
    curl or Postman to hit /scenarios/<name>
    on the Flask app to inject failures and
    watch burn-rate alerts trigger in Datadog.
    """
    print(f"[GENERATOR] Starting — target: {BASE_URL}")
    print(f"[GENERATOR] Endpoint weights: {ENDPOINTS}")
    print(f"[GENERATOR] Rate: variable 0.5–2s per request")
    print(f"[GENERATOR] Ctrl+C to stop\n")

    request_count = 0

    while True:
        endpoint = choose_endpoint()
        endpoint_tag = classify_endpoint(endpoint)
        url = BASE_URL + endpoint
        start_time = time.time()

        try:
            response = requests.get(url, timeout=10)
            latency = round((time.time() - start_time) * 1000, 2)
            status_code = response.status_code

            emit_metrics(endpoint_tag, status_code, latency)
            request_count += 1

            status_label = "SUCCESS" if status_code < 500 else "FAILURE"
            print(
                f"[{status_label}] "
                f"#{request_count:04d} "
                f"endpoint={endpoint} "
                f"status={status_code} "
                f"latency={latency}ms"
            )

        except requests.exceptions.ConnectionError:
            latency = round((time.time() - start_time) * 1000, 2)
            emit_metrics(endpoint_tag, 500, latency)
            request_count += 1

            print(
                f"[CONN_ERROR] "
                f"#{request_count:04d} "
                f"endpoint={endpoint} "
                f"latency={latency}ms "
                f"— is Flask running on {BASE_URL}?"
            )

        except Exception as e:
            latency = round((time.time() - start_time) * 1000, 2)
            emit_metrics(endpoint_tag, 500, latency)
            request_count += 1

            print(
                f"[ERROR] "
                f"#{request_count:04d} "
                f"endpoint={endpoint} "
                f"latency={latency}ms "
                f"reason={str(e)}"
            )

        # Variable sleep — realistic traffic variance
        # Prevents perfectly metronomic requests which
        # can mask burn-rate alert behaviour during testing
        time.sleep(random.uniform(0.5, 2.0))


if __name__ == "__main__":
    generate_traffic()