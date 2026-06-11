# Incident Postmortem: INC-2024-0312

**Incident ID:** INC-2024-0312  
**Severity:** P0  
**Title:** Kafka Broker Disk Exhaustion — Analytics Dashboard Outage  
**Date:** March 12, 2024  
**Duration:** 5 hours 25 minutes (14:22 UTC to 19:47 UTC)

## Impact

**Customer Impact:**
- 47 enterprise customers unable to view analytics dashboards or knowledge gap reports
- Learner progress events backlogged (no data loss—events queued in Kafka and replayed post-resolution)
- No learner-facing outage (Axonify Learn app remained fully functional)
- Affected revenue risk: ~$8.4M ARR (26% of customer base impacted)

**Internal Impact:**
- 5.5 hours unplanned engineering time (on-call SRE + ops team)
- Customer communication delayed 30 minutes (responded at 20:15 UTC)
- 0 data loss (critical win)

## Timeline

**14:22 UTC** — Automated monitoring detects analytics API returning 504s (Service Unavailable). PagerDuty fires P0 alert.

**14:35 UTC** — On-call SRE Marco Silva acknowledges alert; begins investigation. Immediately checks API logs and Datadog dashboard.

**14:52 UTC** — Marco identifies Kafka cluster CPU at 100%. Consumer lag on all topics growing exponentially. Kafka broker health check shows `axonify-kafka-broker-2` disk at 99.8% utilization (1.2 GB free of 500 GB).

**15:10 UTC** — Root cause investigation begins. Marco checks Kafka topic sizes:
- `sre.schedule.computed`: 380 GB (2.8M messages produced in 3 hours)
- `learner.events.raw`: 45 GB (normal)
- Other topics: <5 GB each
Topic `sre.schedule.computed` is the culprit.

**15:45 UTC** — Marco pauses the SRE consumer group `sre-scheduler-v2` to stop producing messages. Disk pressure halts temporarily but doesn't release space.

**16:20 UTC** — Root cause confirmed: SRE worker bug introduced in deploy `v2.14.2` (March 11, 2024). PR #1847 (merged March 11) contained a retry loop condition bug in `sre_worker/scheduler.py:compute_schedule()` line 42. Retry condition `while result is None` failed to check a max-retry counter, creating an infinite loop when the downstream database (RDS) returned `None` for a new learner's initial schedule. This caused 2.8M duplicate messages to be produced to `sre.schedule.computed` in 3 hours.

**16:20 UTC** — Topic retention policy investigation: `sre.schedule.computed` configured with `log.retention.bytes=-1` (unlimited retention). This setting was inherited from the development Kafka configuration and never overridden in production.

**17:30 UTC** — Retention policy patched to `log.retention.bytes=20GB`. Oldest segments deleted; 180 GB freed. Kafka brokers return to healthy state (disk drops to 24%).

**17:45 UTC** — Kafka brokers healthy. Bug fix `v2.14.3` deployed. SRE consumer group restarted with the fix.

**19:47 UTC** — Consumer lag cleared. Analytics dashboards fully restored. P0 resolved.

**20:15 UTC** — Customer communication sent to all 47 affected tenants (email + status page update).

## Root Cause Analysis

**Primary Root Cause:**
Loop condition bug in `sre_worker/scheduler.py:compute_schedule()`. Introduced in PR #1847 (merged March 11). The retry condition `while result is None` lacked a max-retry counter:

```python
# BEFORE (buggy)
while result is None:
    result = await fetch_schedule_from_db(learner_id)

# AFTER (fixed)
retries = 0
while result is None and retries < 5:
    result = await fetch_schedule_from_db(learner_id)
    retries += 1
```

When RDS returned `None` intermittently for a new learner's initial schedule, the loop would retry indefinitely, causing the Kafka producer to emit duplicate messages for every retry attempt.

**Contributing Factors:**

1. **Kafka topic retention policy misconfiguration:** `log.retention.bytes=-1` (unlimited) inherited from dev environment, never audited or overridden in production. Allowed the disk to fill completely.

2. **No disk-space monitoring alert on Kafka brokers:** Only CPU and lag were monitored. Disk space alert would have fired at 70% threshold (would have alerted at 15:00 UTC, 20 minutes into the incident).

3. **Infinite loop bypassed circuit breaker:** The circuit breaker wrapped only the DB call, not the retry loop itself. If the breaker tripped, it wouldn't stop the retry loop.

4. **Code review gap:** PR #1847 approved by 2 reviewers on March 11 (author + 1 peer); neither caught the unbounded retry.

## Action Items

**Immediate (Completed):**
- [AI-1] **Add Kafka broker disk space alert at 70% threshold in Datadog**
  Owner: Marco Silva | Due: 2024-03-20 | Status: ✅ DONE

- [AI-2] **Add exponential backoff + max 5 retries + dead-letter-queue to all SRE worker consumers**
  Owner: Aisha Patel (SRE worker team) | Due: 2024-04-05 | Status: ✅ DONE
  Details: DLQ messages trigger a PagerDuty P2 alert for investigation.

- [AI-3] **Set `log.retention.bytes=20GB` and `log.retention.ms=604800000` (7 days) on all production Kafka topics as IaC default (Terraform)**
  Owner: Marco Silva | Due: 2024-03-25 | Status: ✅ DONE
  Details: Audit all topics for unlimited retention; enforce as Terraform default.

- [AI-4] **Add PR checklist item: "Does this change affect retry logic? If yes, ensure max-retry counter and backoff are present."**
  Owner: Sofia Reyes (VP Eng) | Due: 2024-04-01 | Status: ✅ DONE

- [AI-5] **Chaos engineering drill: simulate Kafka broker disk exhaustion in staging**
  Owner: DevOps team | Due: 2024-06-01 | Status: 🔄 IN PROGRESS

## What Went Well

✅ **PagerDuty alert fired within 7 minutes** of first 504 errors (14:22→14:29). Monitoring coverage at API layer was solid.

✅ **On-call runbook was clear.** Marco isolated the Kafka layer within 35 minutes without escalation.

✅ **Zero data loss.** Kafka's durability guarantees meant events were queued and replayed after broker recovery.

✅ **Customer communication fast.** Sent 30 minutes after resolution (within P0 SLA).

## Lessons Learned

1. **Infrastructure configuration drift is a high-risk failure mode.** Dev/prod Kafka configs diverged silently. All infrastructure configuration must be managed as IaC with explicit production overrides.

2. **Retry logic must always have a bounded exit condition.** Unbounded retries are a system reliability risk. The PR checklist fix (AI-4) will catch similar patterns.

3. **Circuit breaker placement matters.** The breaker wrapped the DB call but not the retry loop. Consider wrapping entire operations including retry logic.

4. **Disk monitoring is as critical as CPU and memory monitoring.** Datadog disk alerts (AI-1) are now on all Kafka brokers.

5. **Scale-related bugs emerge at peak load.** The infinite loop bug would not have been caught on a small staging dataset. Consider load testing retry scenarios.

## Follow-Up

All action items (AI-1 through AI-4) are complete. AI-5 (chaos drill) is in progress and scheduled for Q2 2024.

The company's only P0 incident to date (as of Q3 2024).
