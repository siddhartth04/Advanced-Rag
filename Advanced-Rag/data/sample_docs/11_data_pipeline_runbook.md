# Axonify Data Platform Runbook

## Pipeline Architecture Overview

Raw learner events (clicks, session starts, question answers, completions) are emitted by the Axonify Learn application to Kafka topic `learner.events.raw` (partitioned by tenant_id, 48 partitions).

```
learner.events.raw (Kafka, 48 partitions by tenant_id)
  ↓
Flink stream job: validates, enriches, deduplicates (3–5 min latency)
  ↓
learner.events.normalized (Kafka)
  ├→ TimescaleDB hypertable: learner_events (hot, last 90 days)
  └→ S3 Parquet: s3://axonify-datalake/events/ (cold, partitioned by date/tenant)
      ↓
    dbt transformations (nightly at 02:00 UTC, Airflow DAG: axonify_dbt_nightly)
      ↓
    Redshift: analytics schema (47 dbt models)
      ├→ Metabase dashboards (customer-facing analytics)
      └→ Axonify Insights API (analytics endpoints in product)
```

---

## Key Pipelines

### `learner-events-pipeline` (Flink)
- **Job name:** `axonify-flink-learner-events-v3`
- **Event types processed:** 23 (session.start, session.end, question.answered, question.skipped, module.completed, module.started, streak.maintained, streak.broken, badge.earned, notification.sent, notification.opened, survey.submitted, task.completed, +10 more)
- **Throughput:** Avg 320k events/day, peak 800k events/day (retail morning shift 08:00–10:00 local time)
- **SLA:** Events visible in Insights dashboard within 5 minutes of occurrence
- **Deployed:** ECS Fargate, 4 tasks minimum, autoscales to 12 on lag signal
- **Health check:** `GET /flink/jobs` on Flink jobmanager (internal endpoint only)
- **Alerting:** Datadog monitor on job failure, PagerDuty P1 if down >5 min

### `sre-scheduler-pipeline` (Python workers + Kafka)
- **Reads from:** `sre.schedule.requested`
- **Publishes to:** `sre.schedule.computed`, `sre.schedule.dlq` (dead-letter queue, added post-INC-2024-0312)
- **Workers:** 6 ECS tasks, autoscales 2–20 based on consumer lag metric
- **Retry policy:** Exponential backoff (100ms, 200ms, 400ms, 800ms, 1600ms), max 5 attempts, then publish to DLQ
- **DLQ alert:** PagerDuty P2 fires when DLQ receives any message (investigate within 2h)
- **Owner:** Aisha Patel (backend team)
- **Post-incident mitigation:** AI-2 action from INC-2024-0312; prevents infinite retry loops

### `nightly-dbt-run` (Airflow + dbt)
- **Schedule:** 02:00 UTC daily (Airflow DAG: `axonify_dbt_nightly`)
- **Runtime:** ~35 minutes for all 47 models
- **Models:** dimension tables (learners, modules, topics), fact tables (learner_events, completions), derived tables (knowledge_gaps, predictions)
- **On failure:** Slack alert to #data-platform + PagerDuty P2 if not resolved by 06:00 UTC
- **Owner:** Raj Krishnamurthy (data engineering)
- **Last success:** 2024-06-12 02:35 UTC

---

## Runbook: Kafka Consumer Lag Alert

**Trigger:** Datadog alert "Kafka consumer lag > 50,000 messages on group {group_id}"

**Step 1: Identify affected consumer group**
```bash
kafka-consumer-groups.sh --bootstrap-server $KAFKA_BROKERS \
  --describe --group {group_id}
```
Look for partitions with LAG > 10,000. Note partition IDs and lag values.

**Step 2: Check worker logs**
- Filter Datadog logs by service tag `kafka-consumer` and group ID
- Look for ERROR-level entries
- Common errors:
  - `DatabaseConnectionError`: RDS connection timeout or pool exhausted
  - `SREComputeException`: SRE calculation failure
  - `DeadLetterQueueError`: message failed 5 retries, now in DLQ

**Step 3: If workers healthy (no errors) but lag growing**
```bash
aws ecs update-service --cluster axonify-prod \
  --service {service_name} --desired-count {N}
```
Recommended: double current count, wait 5 minutes, check lag trend.

**Step 4: If lag growth stops but lag is large (>500k)**
- Let it drain naturally (do not scale beyond 20 tasks)
- ETA to clear: `lag / (current throughput per worker)`
- Notify #data-platform with ETA estimate

**Step 5: If disk issue suspected**
- Check Kafka broker disk alert: "Kafka broker disk > 70%"
- See INC-2024-0312 playbook in PagerDuty
- Action AI-3: topic retention limits now set to 20GB per topic via Terraform
- If disk >90%: escalate to Marco Silva (on-call SRE)

---

## Runbook: dbt Run Failure

**Trigger:** Airflow task failure alert in Slack #data-platform

**Step 1: Check Airflow logs**
- Open Airflow UI → DAG `axonify_dbt_nightly` → click failed task → View Log
- Identify which dbt model failed (look for `FAIL` or `ERROR` in output)

**Step 2: Reproduce locally**
```bash
cd dbt_models
dbt test --select {failed_model} --profiles-dir ./profiles
dbt run --select {failed_model} --profiles-dir ./profiles
```

**Step 3: Common causes & remediation**
| Cause | Check | Fix |
|-------|-------|-----|
| Schema change in TimescaleDB | Check #eng-deploys channel for recent migrations | Update dbt model to match schema |
| Null values in non-nullable columns | dbt test output for `not_null` failures | Add data quality check upstream or handle nulls |
| Redshift connection timeout | Redshift cluster health in AWS console | Restart cluster or scale up (VP Ops approval) |
| Permission denied | Check dbt service role IAM policy | Add missing Redshift SELECT permission |
| Memory exhausted | Check Redshift memory usage (WLM queues) | Increase Redshift node count or optimize query |

**Step 4: If not resolvable within 30 min**
- Call Raj Krishnamurthy (on-call data engineer) or post in #data-platform with error log

**Step 5: Business impact**
- Insights dashboard data is stale until dbt run completes
- Customer impact is low before 09:00 UTC (few EU customers active)
- If unresolved by 06:00 UTC: draft proactive customer communication with CSM team

---

## Runbook: Kafka Disk Alert (Post-INC-2024-0312)

**Alert:** Kafka broker disk > 70%

**Step 1: Check which topics are growing**
```bash
kafka-topics.sh --bootstrap-server $KAFKA_BROKERS --describe
```
List all topics and sizes. Identify topic(s) approaching 20GB limit.

**Step 2: Check topic retention policy**
```bash
kafka-configs.sh --bootstrap-server $KAFKA_BROKERS --describe \
  --entity-type topic --entity-name {topic_name}
```
Expected: `log.retention.bytes=20GB` or `log.retention.ms=604800000` (7 days)

If retention is unlimited (`-1`): **escalate immediately**. This is a misconfiguration risk (same as INC-2024-0312).

**Step 3: Check consumer lag**
```bash
kafka-consumer-groups.sh --bootstrap-server $KAFKA_BROKERS \
  --describe --group {group_id}
```
If LAG is large (>500k messages): likely a producer bug or consumer stalled.

**Step 4: Action**
- If topic is correct but growing: monitor over 1 hour (may be normal peak)
- If topic is misconfigured: alert DevOps + apply terraform fix
- If consumer stalled: escalate to team owning consumer (Aisha for SRE, Raj for analytics)

---

## On-Call Schedule

**Team:** Raj Krishnamurthy, Aisha Patel, Marco Silva, David Chen (4-person rotation)

**Schedule:** Weekly rotation, Monday 08:00 UTC to following Monday 08:00 UTC

**PagerDuty Schedule:** `data-platform-oncall`

**Escalation:** If on-call does not acknowledge within 15 minutes → escalates to Sofia Reyes (VP Eng)

**Handoff:** Friday afternoon (before on-call takes shift Monday), outgoing on-call briefs incoming on-call on any ongoing issues

---

## Metrics & Monitoring

**Key SLOs:**
- Learner events visible in Insights within 5 minutes (p95)
- Flink job uptime: 99.9%
- dbt nightly run completes by 03:30 UTC (95% of days)
- Kafka lag <50k messages (95% of time)

**Dashboards:**
- **Flink Health:** Datadog, job status, lag, throughput
- **Kafka Health:** Datadog, broker disk, topic sizes, consumer lag
- **dbt Pipeline:** Airflow, task duration, model count, last run status

**Alerts (PagerDuty):**
- P0: Flink job down, Kafka broker disk >90%, dbt failure by 06:00 UTC
- P1: Kafka lag >500k, dbt failure by 03:30 UTC
- P2: Consumer lag >50k (but growing), dbt near timeout

---

## Emergency Contacts

- **Marco Silva (SRE Lead, Kafka/Infrastructure):** marco.silva@axonify.com
- **Raj Krishnamurthy (Data Engineering Lead):** raj.krishnamurthy@axonify.com
- **Aisha Patel (Backend/SRE):** aisha.patel@axonify.com
- **VP Operations (David Chen):** david.chen@axonify.com
