# P2 Incident Response Runbook

## Document Information

| Item | Value |
|------|-------|
| Runbook ID | RB-P2-001 |
| Incident Severity | P2 (High) |
| Service | Flask Reliability Test Service |
| Monitoring Platform | Datadog |
| Owner | Site Reliability Engineering (SRE) |
| Last Updated | July 2026 |

---

# Purpose

This runbook defines the operational procedure for responding to a **Priority 2 (P2)** incident.

A P2 incident indicates sustained service degradation that may eventually violate the Availability SLO if left unresolved. The service remains operational, but corrective action should be taken before the issue escalates into a critical incident.

---

# Trigger Conditions

Execute this runbook when one or more of the following occur:

- Medium Burn Rate Monitor enters **Alert**
- Error Budget is steadily decreasing
- Sustained increase in application error rate
- Increased response latency
- Degradation affecting one or more endpoints

---

# Incident Response Workflow

```
P2 Alert Received
        │
        ▼
Acknowledge Alert
        │
        ▼
Open Reliability Dashboard
        │
        ▼
Assess Service Health
        │
        ▼
Identify Degrading Components
        │
        ▼
Investigate Root Cause
        │
        ▼
Apply Corrective Actions
        │
        ▼
Verify Stability
        │
        ▼
Close Incident
```

---

# Response Procedure

## Step 1 – Acknowledge the Alert

Record:

- Alert Time
- Monitor Name
- Burn Rate
- Current Availability SLO

---

## Step 2 – Review Service Health

Open the Reliability Overview Dashboard.

Review:

- Availability SLO
- Latency SLO
- Burn Rate
- Error Budget Remaining

Objective:

Determine whether the degradation is stable, improving, or worsening.

---

## Step 3 – Analyze Traffic

Review:

- Total Requests
- Failed Requests
- Success vs Failure Trend
- Endpoint Traffic

Determine:

- Whether failures affect all users.
- Whether only specific endpoints are impacted.

---

## Step 4 – Review Performance

Check:

- Average Response Time
- Endpoint Latency Comparison
- Latency Trend

Determine:

- Whether latency is increasing.
- Whether application performance is degrading.

---

## Step 5 – Investigate the Root Cause

Review:

- Application logs
- Datadog Events
- Recent deployments
- Configuration changes
- Infrastructure status

Possible causes include:

- Increased application load
- Dependency degradation
- Configuration changes
- Resource contention
- Intentional testing (Chaos Injection)

---

## Step 6 – Apply Corrective Actions

Examples include:

- Disable chaos testing if active.
- Optimize application configuration.
- Restart affected services if necessary.
- Roll back recent deployment.
- Monitor the system for continued degradation.

---

## Step 7 – Verify Stability

Confirm that:

- Burn Rate decreases.
- Error Budget stabilizes.
- Failed requests decrease.
- Response time improves.
- Availability SLO remains above the target.

---

## Step 8 – Close the Incident

Close the incident after confirming:

- Service remains stable.
- No further degradation is observed.
- Medium Burn Monitor returns to OK.

---

# Verification Checklist

Before closing the incident:

- Availability SLO healthy
- Burn Rate decreasing
- Error Budget stable
- Response time normal
- Failed requests reduced
- Monitor status OK

---

# Escalation Criteria

Escalate the incident to P1 if:

- Availability drops rapidly.
- Burn Rate continues increasing.
- Error Budget consumption accelerates.
- Multiple services become unavailable.
- Customer impact becomes widespread.

---

# Recovery Indicators

The incident is considered resolved when:

- Reliability metrics stabilize.
- Burn Rate returns to acceptable levels.
- Error Budget consumption normalizes.
- Application performance returns to baseline.
- All related monitors recover.

---

# Tools Used During Investigation

- Reliability Overview Dashboard
- Availability SLO
- Burn Rate Monitor
- Error Budget Widgets
- Event Stream
- Custom Metrics
- Flask Application Logs

---

# Lessons Learned

Following every P2 incident:

- Review the root cause.
- Identify opportunities to prevent recurrence.
- Tune alert thresholds if necessary.
- Improve monitoring and dashboard visibility.
- Update operational documentation where required.