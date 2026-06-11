# Architecture Decision Records (ADRs)

## ADR-001: Migrate from MongoDB to PostgreSQL + TimescaleDB (March 2021)

**Status:** Implemented

**Context:**
In 2020, Axonify stored all learner data (profiles, progress, event logs) on MongoDB 4.2. As customer count grew from 12 to 80, critical bugs emerged: progress saves were occasionally lost during network partitions (MongoDB's eventual consistency), and multi-document transactions were fragile under high load. An incident in November 2020 caused 3 enterprise customers to lose 2 weeks of learner progress data—the company's first major data loss incident, predating the March 2024 P0 (INC-2024-0312).

**Decision:**
Migrate relational data (learners, tenants, modules, assignments) to PostgreSQL 14 with ACID guarantees. Use the TimescaleDB extension for time-series event logs (learner actions, session events) because hypertables offer 10x compression and native time-bucket queries vs. plain PostgreSQL. Keep MongoDB only for content metadata (module JSON, question banks) where document flexibility is genuinely useful.

**Implementation:**
- 3-month project: January–March 2021
- Zero data loss achieved using dual-write pattern during transition
- 1 week production migration window: November 2020 events replayed into PostgreSQL

**Consequences:**
- (+) 40% average query performance improvement on progress APIs
- (+) ACID guarantees eliminated the progress-loss bug class entirely
- (+) TimescaleDB compression reduced storage costs 68%
- (-) Two database technologies to maintain (PostgreSQL + MongoDB)
- (-) Higher DBA expertise required; needed to hire 1 FTE

---

## ADR-012: Event-Driven SRE (Spaced Repetition Engine) with Apache Kafka (July 2023)

**Status:** Implemented (Q4 2023)

**Context:**
The Spaced Repetition Engine (SRE) computed personalized question schedules synchronously per API request. With >5,000 concurrent learners during retail morning peaks, the synchronous SRE computation added 680ms average latency to the `/next-question` API endpoint, causing session abandonment (learners waiting >1s would close the app). Horizontal scaling of SRE workers was blocked by shared-state design: Redis locks on learner schedules created contention, making scale-out ineffective.

**Decision:**
Refactor SRE to event-driven architecture using Apache Kafka:
- Topic `sre.schedule.requested`: API publishes a request when a learner starts a session
- Topic `sre.schedule.computed`: SRE worker publishes the computed schedule (pre-computation during current session for next session)
- Topic `sre.result.delivered`: delivery confirmation for observability

SRE workers: Python + confluent-kafka, autoscaled on ECS Fargate (min 2, max 20 instances based on consumer lag metric).

**Implementation:**
- 6-week project: Q3 2023
- Consumer groups: `sre-scheduler-v2` (production), `sre-scheduler-analytics` (data pipeline)
- Pre-computation: SRE schedules next session during current session (not on-demand), reducing latency

**Consequences:**
- (+) p95 API latency dropped from 820ms to 140ms under peak load
- (+) Horizontal scaling now works: consumer lag is the new scaling signal
- (+) Decoupled SRE computation from API request path
- (-) RISK REALIZED: retention policy misconfiguration in INC-2024-0312 caused Kafka disk exhaustion
- (-) Post-incident: DLQ + exponential backoff added to all SRE consumers; disk alerts added to Kafka brokers

---

## ADR-019: RAG-Based Contextual Help in Axonify Learn (April 2024)

**Status:** In Progress (Q4 2024 target)

**Context:**
Between Q1 2023 and Q1 2024, "how do I use X" support tickets increased 35% as the product surface area grew (Insights module, Connect module, new API endpoints). The support team handles ~320 tickets/week; 38% are answerable by existing documentation, consuming team capacity. Customer Success Management (CSM) team spends ~4 hours/week per customer on onboarding questions that could be self-served.

**Decision:**
Build an internal RAG (Retrieval-Augmented Generation) system indexed over:
- Product documentation (feature guides, help articles)
- API documentation (endpoint specs, code examples)
- Onboarding guides (customer-specific configuration steps)
- FAQ and troubleshooting articles

Embed as a chat widget in the Axonify Learn admin portal. Use retrieval-augmented generation with a self-correction loop to minimize hallucinations. Weekly re-index pipeline to keep docs fresh.

**Architecture:**
- Vector DB: Qdrant (dense embeddings via sentence-transformers)
- Hybrid retrieval: dense vectors + sparse BM25
- Reranking: cross-encoder (ms-marco-MiniLM)
- Self-correction: grade documents + grade generation, up to 2 retries per query
- LLM gateway: LiteLLM (switch providers with 2 env vars)
- Evaluation: RAGAS suite (faithfulness, answer relevancy, context precision/recall)
- Weekly re-index: automated pipeline triggered on doc updates

**Risks & Mitigations:**
- Risk: Hallucination — mitigated by RAGAS evaluation suite run weekly, faithfulness threshold 0.75 required before each release
- Risk: Doc freshness — mitigated by automated re-index on doc update events
- Risk: Data isolation — mitigated by tenant-aware retrieval filter in Qdrant (each customer sees only their config data + global product docs)
- Risk: Model drift — mitigated by monitoring confidence scores per query, alerting on low-confidence answers

**Effort:** 1 ML engineer + 0.5 backend engineer for 12 weeks. Expected Q4 2024 completion.

**Expected Outcomes:**
- 20% reduction in "how do I" support tickets (Q4 OKR)
- CSM team reclaims 3.2 hours/week per customer for higher-value work
- Improved onboarding speed (self-serve for common questions)

**This project (multi-agent-rag repo) is the reference implementation for ADR-019.**

---

## ADR-027: Multi-Agent LangGraph for Query Routing (June 2024)

**Status:** In Progress (design phase)

**Context:**
ADR-019 RAG system needs to handle four distinct query types with different retrieval strategies:
1. **Chitchat** (e.g., "What's the weather?"): no retrieval, generate directly
2. **Factual** (e.g., "What is the API rate limit?"): retrieve chunks, rank, generate answer
3. **Multi-hop** (e.g., "The postmortem mentioned DLQ — is that in the runbook?"): decompose into sub-questions, retrieve per sub-question, combine
4. **Summarization** (e.g., "Summarize all action items from Q3 2024"): retrieve all relevant docs, synthesize summary

**Decision:**
Use LangGraph StateGraph to implement a multi-agent system with:
- Router node: classify query type using LLM
- Per-type orchestration: route to appropriate nodes (direct generation, retrieval, decomposition, etc.)
- Self-correction loop: grade retrieved documents (relevant/irrelevant), grade generation (hallucination/answer relevance), re-retrieve or rewrite on failure (max 2 retries)
- Full execution trace: node_path in response (for debugging and observability)

**Architecture:**
- Graph: StateGraph with 8 nodes (route, decompose, retrieve, grade_documents, transform_query, generate, grade_generation, end)
- LLM: LiteLLM for all LLM calls (switchable providers)
- Retrieval: HyDE → hybrid RRF → cross-encoder rerank
- Tracing: LangSmith (optional, gated by env var)

**Effort:** 2 engineers, 6 weeks (overlaps with ADR-019)

**This ADR drives the multi-agent-rag reference implementation.**
