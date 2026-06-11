# Axonify Engineering Handbook

## Welcome & Culture

Axonify Engineering operates on three core principles:

1. **We ship working software over perfect software.** Iteration beats perfection; 80% done is better than 100% overengineered.
2. **We automate toil before complaining about it.** If a process is manual and repeated, we build tooling.
3. **We write things down.** RFCs, ADRs, runbooks, post-mortems. The person on-call at 2am might not be you.

---

## Onboarding — Week by Week

### Week 1: Foundation
- **Laptop setup:** MacBook Pro M3 or Linux (Ubuntu 22.04+)
- **Tools installation:** Homebrew (macOS) or apt (Linux), Docker Desktop, Python 3.11 via `pyenv`, Node 20 via `nvm`, `uv` for Python package management
- **Repositories:** Clone all team repositories
- **Security training:** 1.5-hour mandatory Axonify Learn module (on the platform itself)
- **Buddy assignment:** Assigned a senior engineer from your team
- **No PRs week 1:** Read code, ask questions, understand project structure

### Week 2: First Contribution
- **Good-first-issue:** Pick a "good-first-issue" label task from GitHub, create PR
- **Meetings:** Attend team sprint planning (Monday) and retrospective (Friday)
- **Local dev env:** Set up local development environment for your team's primary service using `docker compose up`
- **Code review:** Get feedback on your PR from 2 senior engineers

### Week 3: Ownership
- **Feature end-to-end:** Own a small feature from design to production (design doc → implement → test → deploy to staging)
- **Design review:** present design to team for feedback
- **Testing:** write unit + integration tests
- **Staging deployment:** deploy to staging environment, verify in browser

### Week 4: On-Call & Visibility
- **On-call shadowing:** shadow the on-call engineer for one shift (48 hours)
- **Incident response:** practice diagnosing and fixing production issues
- **Friday demo:** present your first-month learnings and projects to the team

---

## Development Environment

**Python Package Management:**
- Always use `uv` (`pip install uv` once)
- `uv sync` installs dependencies from `pyproject.toml`
- `uv run pytest` runs tests with correct PATH

**Pre-Commit Hooks:**
```bash
pre-commit install
```
Hooks run automatically on `git commit`:
- `ruff check` + `ruff format` (linting + formatting)
- `mypy` (type checking)
- `pytest` (run affected tests)
- `detect-secrets` (prevent credentials in code)

**Local Services:**
All services must be runnable locally via `docker compose up` from repo root. No manual setup of databases, caches, or queues. This ensures reproducible environments.

**Secrets Management:**
- **Never commit `.env` files** (use `.env.example` as template)
- **Development:** Load from AWS Secrets Manager via `aws secretsmanager get-secret-value` CLI, or use 1Password CLI (`op read`)
- **Production:** Secrets Manager via IAM roles (no credentials in code)

---

## Git Workflow (GitHub Flow)

1. **Create feature branch** from `main`:
   ```bash
   git checkout -b feat/AXON-1234-short-description
   ```
   Format: `feat/` (feature), `fix/` (bug), `chore/` (maintenance), `docs/` (documentation), `adr/` (architecture)

2. **Commits:** conventional commits format
   - `feat: add multi-hop query decomposition`
   - `fix: prevent infinite retry loop in SRE worker`
   - `docs: update README with provider switching table`

3. **Open PR:** use the PR template
   - **Title:** short (<70 chars)
   - **Description:** 2–3 bullet points of context
   - **Testing:** describe test coverage
   - **Screenshots:** for UI changes

4. **Review & Approval:**
   - Required: 2 approvals (at least 1 from a senior engineer on the team)
   - All CI checks must pass (lint, typecheck, tests, docker build)
   - No unresolved comments

5. **Merge:** squash merge to keep linear history
   - Delete branch after merge

**Branch Protection:** No direct commits to `main`. Branch protection enforced in GitHub.

---

## Coding Standards

**Type Hints:**
```python
from __future__ import annotations

async def call_llm(messages: list[dict], json_mode: bool = False) -> str:
    ...
```
Mandatory on all function signatures. Use `from __future__ import annotations` for forward references.

**Config & Validation:**
```python
from pydantic import BaseModel, ConfigDict

class QueryRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    question: str
    stream: bool = True
```
Use Pydantic v2 for all config, request/response models, and LLM structured outputs.

**Logging:**
```python
import structlog
logger = structlog.get_logger()
logger.info("event", key=value)
```
No `print()` in production code. Use `structlog` for structured logging.

**LLM Calls:**
```python
from rag.llm import call_llm, call_llm_json, stream_llm
```
All LLM calls via the `rag.llm` module. Never import `openai`, `anthropic`, `groq` directly. This enables provider switching with 2 env vars.

**Error Handling:**
```python
try:
    result = await fetch_schedule(learner_id)
except DatabaseConnectionError as e:
    logger.error("failed to fetch schedule", learner_id=learner_id, error=str(e))
    raise
```
Catch specific exceptions, never bare `except`. Log with context. Never silently swallow errors.

**Code Coverage:**
```bash
pytest --cov=src --cov-fail-under=80
```
Minimum 80% coverage enforced in CI.

---

## RFC Process (Request for Comments)

**When required:** Any feature requiring >3 engineer-days of work

**Process:**
1. Draft RFC in Notion (template: Problem Statement → Proposed Solution → Alternatives Considered → Open Questions → Rollout Plan → Success Metrics)
2. 48-hour comment window; tag all stakeholders
3. Author calls decision (approve, iterate, or reject)
4. If approved: create ADR for infrastructure decisions, or just proceed with implementation

**Example RFCs:**
- ADR-019: RAG-based contextual help
- ADR-012: Event-driven SRE with Kafka
- ADR-001: MongoDB → PostgreSQL migration

---

## Testing Philosophy

**Unit Tests:** Pure functions, mocked dependencies. Fast (<1ms each).
```python
def test_rrf_scoring():
    dense_docs = [("doc_1", 0.9), ("doc_2", 0.8)]
    sparse_docs = [("doc_1", 0.7), ("doc_3", 0.75)]
    scores = reciprocal_rank_fusion(dense_docs, sparse_docs, k=60)
    assert scores[("doc_1")] > scores[("doc_2")]  # doc_1 in both lists
```

**Integration Tests:** Real component interactions.
```python
async def test_retrieval_pipeline():
    embedder = SentenceTransformerEmbedder()
    client = QdrantClient(":memory:")
    docs = [Document(page_content="test")]
    # Index, then retrieve
    results = await retrieve_hybrid(query, client, embedder)
    assert len(results) > 0
```

**Contract Tests:** API contract tests using Pact for inter-service calls.

**No E2E in CI:** E2E tests (browser automation, full workflow) run nightly in staging, not in CI (too slow/flaky).

**Test behavior, not implementation:** Test what the function does, not how it does it.

---

## Deployment Process

1. **PR merged to `main`** → GitHub Actions CI runs: lint, typecheck, test, docker build
2. **CI passes** → automatic deploy to `staging` (ECS Fargate, blue-green)
3. **Staging smoke tests** run automatically (5-minute suite)
4. **Production deploy** (manual): VP Eng approves (or auto-approves for low-risk changes)
5. **Blue-green deploy:** traffic shifts 10% → 50% → 100% over 10 minutes with auto-rollback on error rate >1%
6. **Rollback:** `aws ecs update-service --task-definition <previous>` achieves rollback in <5 minutes

---

## Monitoring & Alerting

**APM:** Datadog (traces, metrics, logs, RUM)

**Alerts:**
- **P0/P1:** PagerDuty (phone call)
- **P2/P3:** Slack #alerts

**Infrastructure:** Grafana dashboards for Kafka lag, Qdrant latency, API p99, RDS CPU

**On-Call:** Weekly rotation, every engineer after 6 months tenure. Runbooks in Notion + PagerDuty.

**Post-Incident:** All P0/P1 get a written post-mortem within 5 business days.

---

## Key Contacts

- **CTO (James Okonkwo):** infrastructure, scaling decisions
- **VP Engineering (Sofia Reyes):** hiring, team structure, deployment approvals
- **On-Call Escalation:** VP Ops → CTO
