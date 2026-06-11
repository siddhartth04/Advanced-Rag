# Axonify Q3 2024 Business Review

**Period:** July 1 – September 30, 2024  
**Review Date:** October 15, 2024  
**Prepared by:** Natasha Iyer, CFO

---

## Executive Summary

Q3 2024 was Axonify's strongest quarter to date. ARR crossed $42M for the first time, 23 new enterprise logos were added (company record), and engineering achieved zero P0 incidents after INC-2024-0312 remediation completed in Q2. Net Promoter Score reached 67, a 6-point improvement from Q2. The quarter validated our Series C investment thesis: we can grow efficiently at scale.

---

## Financial Results

**ARR & Growth:**
- **ARR:** $42.1M (+31% YoY vs $32.1M in Q3 2023)
- **Net Revenue Retention (NRR):** 118% (expansion outpacing churn)
- **Gross Margin:** 76% (improving from 73% in Q2 due to infrastructure cost optimization)
- **Monthly Recurring Revenue (MRR):** $3.5M

**Customer Acquisition:**
- **New Bookings TCV:** $8.2M from 23 new enterprise logos (record)
- **CAC (blended):** $18,400
- **LTV (based on 94% retention + 118% NRR):** $142,000
- **LTV/CAC Ratio:** 7.7x (target: >5x; exceeded all 4 quarters)

**Churn & Retention:**
- **Churn:** 2 customers (both Starter tier, annual value $94k combined)
- **ARR Churn:** 0.4% (below target 1%)
- **Retention Rate (dollar basis):** 94% (in line with prior quarters)

**Cash Position:**
- **Total Cash:** $38.2M (18 months runway at current burn rate)
- **Burn Rate:** ~$2.1M/month

---

## Notable Deals (Q3 2024)

**1. RetailCo Canada Expansion**
- Status: Existing customer, expansion
- Growth: 500 → 3,200 learners
- ARR Impact: $384k → $2.4M (+525%)
- Trigger: Successful rollout in Ontario region prompted national expansion
- Deal Owner: Marcus Webb (VP Sales)

**2. LogiTrack US — New Enterprise Logo**
- Learners: 8,000 (large deployment)
- Deal Type: 3-year commitment
- TCV: $1.15M
- Use Case: Safety training compliance for warehouse staff (logistics vertical)
- Deal Owner: Marcus Webb

**3. HealthFirst UK — New Business Logo**
- Learners: 1,200
- Tier: Business (potential upsell to Enterprise)
- Requirement: GDPR-sensitive, EU data residency required
- Strategic Significance: First UK healthcare customer; referral from LogiTrack
- Deal Owner: Axonify UK sales team

---

## Product Highlights

### Shipped in Q3 2024

**Knowledge Gap Predictions (Insights module beta)**
- Launched: mid-August 2024 (beta)
- Feature: AI-powered predictions flag knowledge gaps 14 days before they appear in learner scores
- Technical: Uses decay modeling to forecast learner knowledge trajectory
- Pilot Customers: 12 (retail chains, logistics operators)
- Expected Impact: Proactive intervention instead of reactive discovery

**Slack Integration (GA)**
- Launched: early September 2024
- Feature: Learning nudges posted in team Slack channels (#engineering, #retail-ops, etc.)
- Learner Action: Click to open Axonify app or complete micro-lesson in-channel
- Adoption: 8 customers testing in pilot phase

**Language Support Expansion (Arabic + Hebrew)**
- Launched: mid-September 2024
- Total Languages: 34 (added from 32)
- Arabic: right-to-left interface compliance
- Hebrew: right-to-left + special character support
- Customer Demand: Growing EMEA presence (HealthFirst UK, Middle East prospects)

**Axonify Connect: Pulse Surveys**
- Launched: late August 2024
- Feature: Two-way 5-question surveys with 48-hour response window
- Use Case: Post-training feedback, NPS collection, sentiment gathering
- Adoption: Enterprise tier + 3 Business pilot customers

**Performance Improvements**
- Metric: API p95 latency
- Before: 320ms (June, post-Kafka issues)
- After: 180ms (September, after Kafka migration stabilized + caching optimizations)
- Improvement: 44% reduction; exceeded performance target

### In Progress (Q4 2024 Targets)

**Mobile Offline Mode (iOS + Android)**
- Current Progress: 60% complete
- Target: Q4 2024 GA release
- Impact: Learners can download modules and complete sessions without internet (retail floor, warehouse floor without WiFi)
- Technical Complexity: sync data when connection returns; handle offline state gracefully

**RAG-Based Contextual Help (ADR-019)**
- Current Progress: Architecture + retrieval pipeline complete, LangGraph agents 50% done
- Target: Q4 2024 production launch
- Expected Impact: 20% reduction in "how do I" support tickets
- Technical: Self-correcting RAG, RAGAS evaluation, weekly re-index pipeline

**FedRAMP Moderate Assessment**
- Current Progress: External assessor engaged, controls documentation in progress
- Target: Q3 2025 authorization
- Strategic: Required for US government customers (procurement pipeline building)

---

## Engineering Metrics & Reliability

**Uptime:**
- Platform uptime: 99.97% (SLA for Business tier: 99.9% — exceeded)
- Calculation: HTTP `/health` check from 3 global regions

**Incidents:**
- **P0 Incidents:** 0 (clean quarter post-remediation)
- **P1 Incidents:** 2
  - P1-2024-0721: Insights API degraded for 1h 40m due to Redshift connection pool exhaustion. Root cause: database config change in staging not applied to production. Resolved. Mitigation: IaC config audit added to pre-deploy checklist.
  - P1-2024-0904: Mobile push notification delivery delayed 3h due to APNs certificate expiry. Root cause: manual renewal process not on calendar. Resolved. Mitigation: automated certificate renewal via Let's Encrypt.

**Deployment Velocity (DORA Metrics):**
- **Deploys/week:** 3.6 (Q3 2023: 2.4, +52% improvement)
- **Lead time for change:** 2.3 days (target: <3 days ✅)
- **Change failure rate:** 4.2% (target: <5% ✅)
- **Mean Time to Recovery (MTTR):** 41 minutes (target: <2 hours ✅)

**Team Growth:**
- Start of Q3: 68 engineers
- End of Q3: 79 engineers
- Net: +11 (3 ML engineers for ADR-019, 4 backend, 2 frontend, 2 DevOps)

**Open Roles (End of Q3):**
- 2 Senior Backend Engineers
- 2 ML Engineers (RAG, LLM fine-tuning)
- 1 DevOps Engineer (Kubernetes, Terraform)
- 1 VP Marketing

---

## Customer Success & NPS

**NPS (Net Promoter Score):**
- Q3 2024: 67 (up from 61 in Q2, up from 54 in Q3 2023)
- Benchmark: SaaS industry average 30–50; Axonify trending top quartile

**CSAT (Customer Satisfaction - support tickets):**
- Rating: 4.6/5.0
- Response time: avg 2.2 hours (SLA 24 hours)
- Resolution rate: 94% first contact resolution

**At-Risk Accounts (3 flagged by CSM):**
1. **IndustrialCo:** DAU/MAU <25% for 2+ weeks; intervention playbook activated; root cause: low manager adoption
   - Action: manager training webinar scheduled, coaching templates provided
2. **RetailBrand EU:** New CSM assigned after previous CSM departure
   - Action: CSM transition call completed; business review rescheduled
3. **FinanceGroup US:** Escalation call with VP Sales and CEO scheduled
   - Concern: budget constraints post-Q3 planning

**Renewal Rate:**
- Dollar basis: 94% (in line with Q3 2023 and Q1/Q2 2024)

---

## Q4 2024 OKRs

**O1: Grow ARR to $46M**
- KR1: Close $4.2M net new ARR (new logos + expansion)
- KR2: NRR ≥120%
- KR3: Churn <$400k

**O2: Ship Mobile Offline Mode to GA**
- KR1: iOS beta by October 31, 2024
- KR2: Android by November 30, 2024
- KR3: 95% of existing mobile users able to complete a session offline in pilot

**O3: Complete FedRAMP Readiness Assessment**
- KR1: All 325 controls documented
- KR2: External assessor report received
- KR3: Plan of Action & Milestones (POA&M) submitted to FEDRAMP PMO

**O4: Hire VP Marketing + 8 Engineers**
- KR1: VP Marketing offer accepted by November 1, 2024
- KR2: 8 engineers (backend, ML, DevOps) onboarded by December 31, 2024

**O5: RAG Contextual Help Reduces Support Tickets 20%**
- KR1: ADR-019 shipped to production by November 30, 2024
- KR2: Measurable 15% reduction in Q4 support ticket volume vs Q3 baseline
- KR3: RAGAS faithfulness score >0.75 (requirement for production release)

---

## Market & Competitive Position

**TAM (Total Addressable Market):**
- Global LMS market: $8B (Gartner 2024)
- Microlearning-specific market: $1.2B (growing 18% CAGR)
- Axonify TAM: ~$600M (high-growth enterprises with >1,000 employees in retail, logistics, healthcare, finance)

**Competitive Landscape:**
- **Incumbents:** Cornerstone OnDemand ($4B public), SAP SuccessFactors, Workday Learning
- **Upstarts:** Paradiso (no funding), EdCast (acquired by Cornerstone), Degreed (Series D, $300M+)
- **Axonify Advantage:** Mobile-first, spaced repetition science, 3-minute format, vertical specialization, AI analytics

**Win Rate:**
- Q3 2024: 68% (won 23/34 qualified opportunities)
- Typical deal cycle: 3–4 months (pilot + enterprise sales)
- Average deal size: $356k TCV (Q3 2024)

---

## Looking Ahead (2025 Vision)

**Year-End 2024 Targets:**
- ARR: $46M (+9% vs Q3 baseline)
- Customers: 205+ (from 180 at Q3 end)
- Team: 87 engineers + VP Marketing hired

**2025 Strategic Priorities:**
1. **Geographic expansion:** Latin America, APAC (after EMEA stabilization)
2. **Vertical deepening:** Healthcare compliance certifications (HIPAA, HL7), Finance regulatory (SOX, PCI)
3. **AI/ML capabilities:** Generative AI for content recommendation, chatbot for learning nudges (ADR-019 foundation)
4. **Mobile-first delivery:** Offline mode, push notifications, in-app gamification
5. **Enterprise scale:** FedRAMP, ISO 27001, multi-instance deployments for Fortune 500 customers

**Funding Runway:**
- Current cash: $38.2M
- Runway: 18 months at current burn
- No immediate funding need; potential Series D in 2025 if pursuing aggressive hiring/geographic expansion
