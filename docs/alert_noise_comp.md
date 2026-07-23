# Threshold Alerts vs Burn Rate Alerts

## Project

Datadog Observability Platform

---

# Objective

This document compares traditional threshold-based monitoring with Error Budget Burn Rate monitoring and explains why burn-rate alerts were selected as the primary reliability alerting strategy for this project.

---

# Threshold-Based Monitoring

Threshold monitors trigger alerts whenever a metric exceeds a predefined value.

Example:

- Error Rate > 5%
- Response Time > 300 ms
- CPU Utilization > 80%

### Advantages

- Easy to configure.
- Suitable for basic infrastructure monitoring.
- Immediate alert generation.

### Limitations

- Does not consider service reliability over time.
- May trigger alerts for temporary spikes.
- Cannot determine how quickly the Error Budget is being consumed.
- Difficult to prioritize incidents based on business impact.

---

# Burn Rate Monitoring

Burn Rate monitoring evaluates how quickly the service is consuming its Error Budget relative to the defined Service Level Objective (SLO).

Instead of monitoring individual metrics, it monitors the rate at which service reliability is degrading.

The project implements:

- Fast Burn Rate Monitor (P1)
- Medium Burn Rate Monitor (P2)
- Slow Burn Rate Monitor (P3)

Each monitor evaluates different rolling time windows to detect both rapid failures and gradual degradation.

---

# Comparison

| Feature | Threshold Alerts | Burn Rate Alerts |
|----------|------------------|------------------|
| Based on metric values | ✓ | ✗ |
| Based on SLO compliance | ✗ | ✓ |
| Tracks Error Budget consumption | ✗ | ✓ |
| Detects gradual degradation | Limited | ✓ |
| Supports incident prioritization | Limited | ✓ |
| Reliability focused | ✗ | ✓ |

---

# Why Burn Rate Was Chosen

The objective of this project was to demonstrate reliability engineering rather than basic monitoring.

Burn Rate monitoring aligns directly with Service Level Objectives by evaluating the rate of Error Budget consumption instead of isolated metric spikes.

This approach provides more meaningful operational alerts and helps prioritize incidents according to their potential impact on service reliability.

---

# Role of Metrics, Logs, and Traces

Although Burn Rate monitors are driven by metrics, effective incident investigation requires all three telemetry signals.

## Metrics

Used to:

- Evaluate SLO compliance.
- Calculate Error Budget consumption.
- Trigger Burn Rate alerts.

## Logs

Used to:

- Investigate failed requests.
- Identify affected endpoints.
- Review application events.

## Traces

Used to:

- Analyze complete request execution.
- Identify latency bottlenecks.
- Correlate requests with application logs.
- Accelerate Root Cause Analysis.

---

# Example Incident Workflow

1. Burn Rate monitor detects rapid Error Budget consumption.
2. Dashboard shows increasing error rate and SLO degradation.
3. Engineers review structured logs in Log Explorer.
4. Related distributed traces are opened in Datadog APM.
5. Trace analysis identifies where request latency or failures occurred.
6. Root Cause Analysis and postmortem are completed.

---

# Conclusion

Threshold monitors remain useful for monitoring individual system metrics, but Burn Rate monitoring provides a more reliable approach for managing service reliability.

By combining Burn Rate alerting with centralized logging and distributed tracing, the observability platform supports faster detection, investigation, and resolution of reliability issues while maintaining focus on overall service health rather than isolated metric thresholds.