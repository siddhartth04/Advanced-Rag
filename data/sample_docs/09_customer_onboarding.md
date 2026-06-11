# Axonify Customer Onboarding Guide

## Pre-Kickoff (T-7 days)

**Axonify Provisioning Team:**
- Tenant created in 24 hours post-contract signature
- Verification: customer can log in with temporary admin credentials

**Customer Success Manager (CSM):**
- Welcome Kit emailed: admin credentials, technical requirements checklist, SSO configuration guide, learner data CSV template
- Technical requirements form sent:
  - SSO provider details (entity ID, SAML metadata URL)
  - IP ranges for whitelist (if applicable: 52.204.x.x, 52.206.x.x, 54.147.x.x)
  - HRIS system for sync (Workday/SAP/BambooHR)
  - List of departments and locations for org hierarchy setup

**Customer preparation:**
- L&D lead and IT lead identified
- Internal kickoff held with stakeholders

---

## Kickoff Call (Day 0)

**Participants:** Axonify CSM, Implementation Specialist, customer L&D lead, customer IT lead

**Duration:** 90 minutes

**Agenda:**
1. Product tour (30 min): Axonify Learn, Insights, Connect (if Enterprise)
2. SSO configuration (30 min): live configuration, test authentication
3. Success metrics definition (20 min): agree on KPIs (DAU/MAU targets, knowledge improvement %)
4. Project plan review (10 min): timeline, milestones, next steps

**Deliverable:** Signed project plan with kickoff date and key milestone dates

---

## Week 1 — Tenant Setup

**Axonify Infrastructure Team:**
- Provisioning via Terraform: S3 bucket, RDS schema, tenant record in identity system, API credentials
- Custom domain configuration: `learn.customername.com` → CNAME to Axonify CDN

**Axonify Branding Team:**
- Customer logo upload (SVG, min 200px width)
- Primary color (hex): used for buttons, links, highlights
- Secondary color (hex): used for accents
- White-label applied to web portal

**Axonify Integration Team:**
- SSO integration tested and confirmed
- Admin accounts created
- IP whitelist configured (if required)

**Completion:** Customer can log in to branded portal at `learn.customername.com`

---

## Week 2 — Content & Learner Setup

**Content Migration:**
- Customer provides SCORM packages or existing training materials
- Axonify content team builds 5 starter microlearning modules (included in all tiers)
- Delivery SLA: within 5 business days
- Modules created from customer materials:
  - Company overview + culture
  - Product knowledge (top 3 products)
  - Safety/compliance fundamentals
  - Customer service standards
  - Role-specific skills (1 module per role)

**Learner Bulk Upload:**
- CSV template provided with fields: email, first_name, last_name, department, location, role, external_id (max 50,000 rows)
- Alternative: HRIS auto-sync configured (Workday/SAP/BambooHR with bi-directional sync)
- Customer data imported; provisioning completes next day

**Org Hierarchy:**
- Department/location structure created to match customer org chart
- Manager role assignments reviewed with customer
- Permissions tested (managers can see only their reports)

**Completion:** Learner roster loaded; Insights dashboard shows initial demographic data

---

## Week 3 — Pilot Launch

**Pilot Group Selection:**
- 50–500 learners from one department or location (e.g., "Store #42" or "Checkout team")
- Rationale: controlled rollout, easier to troubleshoot issues, feedback from early adopters

**CSM Pilot Checklist:**
- Push notification sent to pilot group
- Manager briefing deck provided (2-slide overview)
- Learner communication templates (email + Slack/Teams snippets)
- Example: "Sarah, your team is starting Axonify learning. Click here to get started."

**Baseline Report:**
- Knowledge gap report generated on pilot day
- Shows starting knowledge scores by topic/department
- Establishes baseline for 30/60/90-day comparison

**Pilot Metrics Review (Day 5 of pilot):**
- 30-minute CSM check-in call
- Metrics reviewed:
  - DAU/MAU: target ≥30% (by day 5)
  - Session completion rate: target ≥80%
  - Sessions per learner: target ≥1
- If metrics met: proceed to full launch. If below target: troubleshoot + extend pilot by 1 week

---

## Week 4 — Full Launch

**Prerequisite:** Pilot metrics met (or waived by SVP Customer Success)

**Rollout Strategy:**
- If <10,000 learners: enroll all at once
- If >10,000 learners: phased by location (e.g., "Store #1–#50 week 1, Store #51–#100 week 2")

**Manager Training (Webinar):**
- 45-minute live session: how to use Insights, how to interpret dashboards, how to send coaching nudges
- Recording provided for asynchronous viewing
- Q&A session

**Reporting Cadence Agreed:**
- Starter: no recurring reviews (support available, no dedicated CSM)
- Business: quarterly dashboard review call (CSM reviews Insights, knowledge trends, recommends actions)
- Enterprise: monthly executive business review (CSM + VP Sales present trends and expansion opportunities)

**Launch Communication:**
- Email templates provided (sent by customer to learners)
- Announcement slide deck (for all-hands)
- FAQ document (common learner questions)
- Manager messaging: why this matters, what to expect, how to use data

**Completion:** Learners accessing Learn app, first knowledge baseline collected

---

## Day 90 — Success Review

**NPS Survey:**
- Sent to all admin users and sample of learners (max 200)
- Target: NPS ≥50 (industry benchmark: 30–50)

**Knowledge Improvement Report:**
- Compares baseline (Week 3) vs Day 90 knowledge scores
- Expected: +10% to +20% improvement in average scores
- By topic: which topics improved most, which need attention

**Success Metrics Review Against Kickoff Targets:**
- DAU/MAU target achieved?
- Knowledge improvement target hit?
- Compliance modules passed by required date?

**Expansion Conversation:**
- Additional departments on waitlist?
- Axonify Insights adoption high enough for Axonify Connect upsell?
- Language expansion needed (e.g., Spanish for US locations)?

---

## At-Risk Playbook

**Triggers:**
- DAU/MAU <25% for 2 consecutive weeks
- NPS <40 in survey
- Renewal risk flagged by CSM (e.g., budget cuts, leadership change)

**Escalation Steps:**
1. CSM escalation call within 48 hours: diagnose root cause
   - Is engagement low due to poor manager adoption? (common)
   - Is content not resonating with learners?
   - Are technical issues blocking access?

2. Executive sponsor email from VP Sales to customer SVP/head of L&D

3. Axonify Insights deep-dive: identify specific knowledge gaps or cohorts underperforming

4. Joint action plan with 30-day check-in
   - Example: "We'll add 2 manager coaching workshops; you'll send weekly nudges to top 10 underperformers"

5. If unresolved in 60 days: escalate to VP Customer Success

---

## Ongoing Success Metrics

**Axonify tracks per customer:**
- DAU/MAU ratio (daily active / monthly active)
- Session completion rate (% of sessions completed without dropout)
- Knowledge retention improvement (% change vs baseline at 30/60/90 days)
- Streak maintenance (% learners with 5+ consecutive days of learning in past 30 days)
- Compliance module pass rate (if applicable)

**Health dashboard:** CSM views real-time health metrics in internal Axonify dashboard; alerts fire if metrics degrade

**Business review cadence:**
- Starter: support-based (no scheduled review)
- Business: quarterly (60 min, review dashboards, trends, expansion)
- Enterprise: monthly (90 min, executive-level review, includes expansion discussion)

---

## Key Success Factors

1. **Manager adoption is critical.** Customers with high manager engagement (using Insights dashboards, sending coaching nudges) have 35% higher DAU/MAU.

2. **Content quality drives engagement.** Custom, role-relevant modules outperform generic ones 4:1.

3. **Communication matters.** Customers who send weekly learner emails + manager briefings show 2x engagement.

4. **Early wins:** Focus pilot on high-engagement department to prove ROI before full rollout.

5. **Executive sponsorship:** VP/SVP involvement in kickoff strongly correlates with >90 day renewal success.
