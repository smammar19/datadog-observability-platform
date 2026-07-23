# Contributing Factors

## Incident Information

| Item | Details |
|------|---------|
| Incident ID | INC-001 |
| Severity | P1 |
| Service | Flask Reliability Test Service |
| Monitoring Platform | Datadog |

---

# Purpose

This document identifies the factors that contributed to the incident's impact.

While the primary cause of the incident was intentional chaos injection, several additional conditions influenced how the incident evolved and how it was observed.

---

# Primary Root Cause

The primary cause of the incident was the intentional activation of runtime chaos injection, which forced requests to the `/service` endpoint to return HTTP 500 responses.

This behaviour was expected as part of the reliability testing process.

---

# Contributing Factors

## 1. High Simulated Error Rate

The chaos configuration injected a 100% error rate.

As a result:

- Every request to the `/service` endpoint failed.
- Error Budget consumption increased rapidly.
- Availability SLO degraded quickly.

Impact:

High

---

## 2. Continuous Traffic Generation

The Traffic Generator continuously sent requests to the application.

This resulted in:

- Rapid accumulation of failed requests.
- Faster metric updates.
- Quicker Burn Rate increase.
- Immediate monitor evaluation.

Impact:

Medium

---

## 3. Rolling Evaluation Windows

Burn Rate monitors evaluate conditions over rolling time windows rather than reacting instantly.

As a result:

- Alerts were not triggered immediately.
- Different monitors entered the Alert state at different times.

Impact:

Low

---

## 4. SLO-Based Alerting

The monitoring system evaluated Error Budget consumption instead of relying solely on metric thresholds.

This improved alert quality by ensuring alerts reflected service reliability rather than temporary metric spikes.

Impact:

Positive

---

## 5. Reliability Dashboard

The centralized dashboard provided immediate visibility into:

- Availability SLO
- Burn Rate
- Error Budget
- Failed Requests
- Active Alerts

This reduced investigation time.

Impact:

Positive

---

# Factors That Did NOT Contribute

The following components operated as expected throughout the incident:

- Datadog Agent
- DogStatsD
- Metric collection pipeline
- Traffic Generator
- Dashboard widgets
- Alert routing
- Burn Rate monitors

No failures were observed in the observability infrastructure itself.

---

# Summary

The incident was intentionally generated for validation purposes.

The observability platform performed as designed by:

- Collecting custom metrics.
- Detecting increased failure rates.
- Tracking Error Budget consumption.
- Triggering threshold and Burn Rate alerts.
- Providing operational visibility through the Reliability Overview Dashboard.

The contributing factors primarily affected the speed and visibility of the incident rather than introducing additional system failures.