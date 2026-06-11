# Production Multi-Agent RAG · LiteLLM · LangGraph · RAGAS

**Switch any LLM in 2 env vars. Self-correcting retrieval. Automated quality metrics.**

An enterprise-grade, self-correcting Multi-Agent RAG system demonstrating advanced retrieval-augmented generation concepts. Built with LiteLLM, LangGraph, RAGAS evaluation, and 100+ LLM provider support.

## 🎯 Overview

Reference implementation of **ADR-019: RAG-Based Contextual Help**. Powers an internal knowledge assistant over complete enterprise dataset (12 documents, 13.5k words covering company, products, security, architecture, incidents, HR, operations).

**Core Features:**
- **100+ LLM providers** via LiteLLM (Ollama, OpenAI, Anthropic, Groq, Gemini, Mistral, Together AI)
- **Adaptive query routing** — chitchat/factual/multi-hop/summarization strategies
- **Hypothetical Document Embeddings (HyDE)** — improve dense retrieval
- **Hybrid retrieval** — dense (vector) + sparse (BM25) with Reciprocal Rank Fusion
- **Cross-encoder reranking** — ms-marco-MiniLM for top-k results
- **Self-correction loop** — grade docs, grade generation, re-retrieve on failure (max 2 retries)
- **RAGAS evaluation** — faithfulness, answer relevancy, context precision/recall
- **FastAPI streaming** — SSE for token-by-token responses
- **Streamlit UI** — chat + eval dashboard
- **Docker Compose** — one-command local setup

## 🚀 Quick Start

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec api python scripts/ingest.py data/sample_docs
open http://localhost:8501
```

## 🔄 LiteLLM Provider Switching

Change 2 env vars, zero code changes:

```bash
# Ollama (free, local)
LLM_MODEL=ollama/llama3.1:8b
LLM_API_BASE=http://localhost:11434

# OpenAI
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...

# Anthropic
LLM_MODEL=anthropic/claude-opus-4-1
ANTHROPIC_API_KEY=sk-ant-...
```

See `.env.example` for all providers.

## 📚 Sample Data (13.5k words)

12 realistic markdown documents:
- 01_company_overview.md — founding, team, metrics, culture
- 02_product_catalog.md — Learn, Insights, Connect products
- 03_api_documentation.md — REST v2 endpoints
- 04_security_compliance.md — SOC 2, GDPR, FedRAMP, encryption
- 05_architecture_decisions.md — 3 ADRs
- 06_incident_postmortem.md — INC-2024-0312 (Kafka P0)
- 07_engineering_handbook.md — onboarding, git flow, testing, deployment
- 08_pricing_contracts.md — three tiers, refunds, SLAs
- 09_customer_onboarding.md — week-by-week timeline
- 10_hr_policies.md — time off, comp, benefits by region
- 11_data_pipeline_runbook.md — Flink, Kafka, dbt, troubleshooting
- 12_quarterly_review_q3_2024.md — financials, product shipped, team metrics

## 📖 API Endpoints

```
GET  /health              — status + llm_model
POST /query               — ask question (streaming)
POST /ingest              — ingest documents
GET  /eval/latest        — RAGAS results
```

## 🧪 Testing

```bash
pytest -q
```

All offline (mocked LiteLLM, no API keys, no network).

## 📊 RAGAS Evaluation

```bash
python -m rag.evaluation.run_ragas
```

20-question golden set. Output: `results/eval_<ts>.json`

**Metrics:** faithfulness, answer relevancy, context precision/recall

Threshold: faithfulness ≥0.75 required for production (ADR-019).

## 📁 Structure

```
src/rag/
  ├── config.py           settings
  ├── llm.py              LiteLLM wrapper
  ├── ingestion/          loaders, chunking, indexer
  ├── retrieval/          embeddings, HyDE, hybrid, reranker, router
  ├── agents/             state, nodes, prompts, graph
  ├── evaluation/         golden_set, RAGAS runner
  └── api/                FastAPI app
ui/app.py                Streamlit chat
tests/                   unit + integration tests
data/sample_docs/        12 markdown files
```

## ✅ What's Done

- ✅ Full LiteLLM integration (call_llm, call_llm_json, stream_llm)
- ✅ 12 sample documents (13.5k words, cross-referenced)
- ✅ Ingestion pipeline (loaders, chunking, Qdrant indexer)
- ✅ Retrieval (HyDE, hybrid RRF, reranker, router)
- ✅ LangGraph multi-agent system (8 nodes, self-correction)
- ✅ FastAPI streaming + Streamlit UI
- ✅ RAGAS evaluation (20-question golden set)
- ✅ Docker Compose local dev
- ✅ GitHub Actions CI (ruff, mypy, pytest, docker build)
- ✅ Comprehensive tests (chunking, RRF, router, graph, API)

## 🎯 Design Rationale

**HyDE:** Generate query-specific hypothetical doc → improve dense retrieval precision (+8-15%)

**RRF (k=60):** Stable combination of dense + sparse. k=60 empirically balances rank position and diversity

**Max 2 retries:** Prevent infinite loops; 2 retries ≈ 99% p99 latency <5s

**LiteLLM:** Zero code changes to switch providers; unified async API across 100+

## 📝 See Also

- **PROJECT_SPEC.md** — full specification (phases, architecture, decisions)
- **.env.example** — all provider configs
- **pyproject.toml** — dependencies
- **docker-compose.yml** — local dev stack

---

Built with LiteLLM · LangGraph · RAGAS · FastAPI · Streamlit · Docker