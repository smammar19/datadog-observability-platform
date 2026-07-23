# Incident Timeline

## Incident Summary

| Item | Details |
|------|---------|
| Incident ID | INC-001 |
| Severity | P1 |
| Service | Flask Reliability Test Service |
| Monitoring Platform | Datadog |
| Incident Type | Simulated Reliability Incident |
| Cause | Runtime Chaos Injection |

---

# Timeline

| Time | Event |
|------|-------|
| T+00:00 | Chaos injection enabled with 100% simulated error rate. |
| T+00:01 | Traffic Generator began receiving HTTP 500 responses from the `/service` endpoint. |
| T+00:02 | `service.failure.count` and `service.error_rate` metrics increased significantly. |
| T+00:03 | Datadog Agent forwarded updated custom metrics to the Datadog platform. |
| T+00:04 | Availability SLO began decreasing. |
| T+00:05 | Error Budget consumption increased rapidly. |
| T+00:06 | Threshold Monitor entered the Alert state. |
| T+00:07 | Burn Rate increased beyond configured thresholds. |
| T+00:08 | Fast Burn, Medium Burn, and Slow Burn monitors entered the Alert state after satisfying their evaluation windows. |
| T+00:10 | Reliability Dashboard reflected degraded service health, increased failures, and active alerts. |
| T+00:11 | Chaos injection disabled by resetting the error rate to 0%. |
| T+00:12 | Successful requests resumed. |
| T+00:13 | Error Budget consumption stabilized. |
| T+00:14 | Availability SLO began recovering. |
| T+00:15 | Monitors gradually returned to the OK state. |

---

# Systems Involved

- Flask Reliability Test Service
- Python Traffic Generator
- DogStatsD
- Datadog Agent
- Datadog SLO Monitoring
- Burn Rate Monitors
- Reliability Overview Dashboard

---

# Impact

During the simulation:

- Service availability decreased.
- HTTP 500 responses increased.
- Availability SLO degraded.
- Error Budget was rapidly consumed.
- All configured monitors detected the incident.
- Dashboard reflected the degraded state in real time.

---

# Resolution

The incident was resolved by disabling runtime chaos injection.

After recovery:

- Successful requests resumed.
- Burn Rate returned to normal.
- Error Budget consumption stabilized.
- Availability SLO began recovering.
- All monitors eventually returned to the OK state.

---

# Lessons

The simulation validated the complete observability pipeline:

- Custom metrics
- DogStatsD metric forwarding
- Datadog Agent ingestion
- Availability SLO calculation
- Error Budget tracking
- Burn Rate monitoring
- Alert generation
- Dashboard visualization