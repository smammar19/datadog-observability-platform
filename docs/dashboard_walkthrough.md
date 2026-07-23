# Reliability Overview Dashboard Walkthrough

## Purpose

This document explains how to use the Reliability Overview Dashboard during normal operations and incident response.

The dashboard is intended to provide engineers with a structured workflow for assessing application reliability.

---

# Step 1 – Review Service Health

Begin by examining the Service Health section.

Check:

- Availability SLO
- Latency SLO
- Error Budget Remaining
- Burn Rate

Questions to answer:

- Is the Availability SLO above the target?
- Is the Error Budget decreasing?
- Is Burn Rate increasing?
- Is immediate action required?

If all values are healthy, proceed to the Traffic section.

---

# Step 2 – Analyze Traffic

Review the Traffic section.

Check:

- Total Requests
- Successful Requests
- Failed Requests
- Success vs Failure Trend
- Endpoint Traffic

Questions to answer:

- Is request volume normal?
- Are failed requests increasing?
- Which endpoint is receiving the most traffic?

An increase in failed requests may indicate an application or infrastructure issue.

---

# Step 3 – Evaluate Performance

Open the Performance section.

Review:

- Average Response Time
- Endpoint Latency Comparison
- Latency Trend
- Latency Distribution

Questions to answer:

- Is response time increasing?
- Which endpoint is the slowest?
- Are latency objectives being met?

Performance degradation may occur even if Availability SLO remains healthy.

---

# Step 4 – Review Operational Status

Inspect the Operations section.

Review:

- Monitor Status
- Active Alerts
- Event Stream
- Top Error Endpoints

Questions to answer:

- Which monitors are currently in Alert?
- What recent operational events occurred?
- Which endpoint is generating failures?

These widgets help identify the probable source of an incident.

---

# Typical Incident Investigation Workflow

When an alert is received, the following workflow is recommended.

1. Check Service Health.
2. Verify Burn Rate.
3. Review Error Budget.
4. Inspect Failed Requests.
5. Identify affected endpoint.
6. Review Response Time.
7. Check Monitor Status.
8. Review Event Stream.
9. Investigate logs, traces, or infrastructure if necessary.

---

# Dashboard Sections Summary

| Section | Primary Purpose |
|----------|-----------------|
| Service Health | Evaluate SLO compliance and Error Budget |
| Traffic | Monitor request volume and failures |
| Performance | Identify latency issues |
| Operations | Monitor alerts and operational events |

---

# Recommended Usage

This dashboard should be the first dashboard opened when:

- A monitor enters the Alert state.
- Service degradation is reported.
- SLO compliance needs to be reviewed.
- Reliability metrics are being evaluated.
- Operational health checks are performed.

---

# Conclusion

The Reliability Overview Dashboard provides a structured operational workflow for monitoring application reliability.

Rather than focusing on individual metrics, it combines Service Level Objectives, Error Budget monitoring, traffic analysis, application performance, and operational awareness into a single dashboard that supports rapid incident detection and investigation.