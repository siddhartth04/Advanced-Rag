# Axonify Product Catalog

## Product 1: Axonify Learn (Core Product)

The adaptive microlearning engine delivered via web and mobile (iOS + Android). Designed for frontline workforces who need bite-sized, personalized learning in their pockets.

### Key Capabilities

**Adaptive Spaced Repetition Engine (SRE)**
- Personalizes question sequencing per learner using a modified Ebbinghaus forgetting curve
- Tracks 14 learner-specific decay parameters: base memorability, difficulty perception, recency weight, interference factor, and 10 others
- Questions are shown at the optimal moment to move knowledge from short-term to long-term memory
- SRE is event-driven (post-July 2023 refactor): learners trigger SRE computation asynchronously via Kafka topics `sre.schedule.requested` and `sre.schedule.computed`
- p95 API latency improved from 820ms to 140ms after the Kafka refactor

**Daily Microlearning Format**
- Sessions: 3–5 minutes per day, designed for retail morning shifts, warehouse breaks, or healthcare duty breaks
- Frequency: daily recommended, but flexible based on learner role/department
- Completion incentives: streaks, badges, points, leaderboards

**Content Types (40+ question types)**
- Multiple choice (single/multiple correct)
- True/false binary
- Image-based identification (click the correct object in an image)
- Video scenarios (up to 2 minutes, followed by comprehension questions)
- Scenario-based branching (choose action A or B, consequences shown)
- Fill-in-the-blank (auto-graded with fuzzy matching)
- Drag-and-drop ranking (order steps or priorities)
- Binary swipe (swipe left/right for yes/no)
- Hotspot (click regions of an image to identify hazards)
- Sequencing (order events or steps correctly)
- Plus 30 more specialized question types

**Gamification Layer**
- Streaks: consecutive days of learning (displayed prominently); streak broken notification if missed
- Leaderboards: department-level and company-level rankings (weekly, monthly, all-time)
- Badges: achievement unlocks (e.g., "7-Day Streak," "Perfect Score," "Top 10 Performer")
- Points: earned per question, session, day — exchangeable for physical rewards or recognition
- Weekly Challenges: themed mini-competitions (e.g., "Food Safety Challenge," "Customer Service Master")
- Social: peer comparisons (opt-in) and team challenges

**Language Support**
- 34 languages supported (added Arabic and Hebrew in Q3 2024)
- Arabic is right-to-left compliant
- Content can be delivered in learner's preferred language with automatic translation of custom questions

**Accessibility**
- WCAG 2.1 AA compliant
- Screen reader compatible
- Keyboard navigation fully supported
- High contrast mode available
- Captions on all video content

**Offline Mode (In Progress)**
- Target: Q4 2024 mobile release
- Allows learners to download modules and complete sessions without internet (e.g., warehouse floor without WiFi)
- Sync data when connection returns
- iOS beta: 60% complete; Android: TBD

### Mobile & Web

- **iOS App**: native Swift, supports iOS 14+, 2.4M active iOS users
- **Android App**: native Kotlin, supports Android 10+, 1.8M active Android users
- **Web Portal**: responsive React + TypeScript, used by managers and admins for content creation and analytics
- White-label mobile app available on Enterprise tier (custom branding, custom domain in App Store)

---

## Product 2: Axonify Insights (Analytics & Intelligence)

The intelligence layer for managers, L&D teams, and executives. Provides real-time visibility into learner knowledge gaps and organizational learning trends.

### Key Capabilities

**Real-Time Knowledge Gap Heatmaps**
- Visualize knowledge gaps by:
  - Department (e.g., "Checkout" vs. "Stockroom" in retail)
  - Location (store #, warehouse #, region)
  - Topic (compliance, product knowledge, safety, soft skills)
  - Individual learner
- Color-coded: green (mastered >80%), yellow (developing 50–80%), red (gaps <50%)
- Drill-down: click a gap to see which questions learners struggle with

**AI-Powered Knowledge Decay Predictions**
- Machine learning model (launched Q3 2024 beta) flags learners at risk of knowledge decay before it happens
- Prediction: forecasts which learners will score below threshold within 14 days
- Recommendation: "Sarah in checkout shows decay risk for food safety — assign module X"
- Accuracy: 78% precision on held-out test set

**Manager Coaching Recommendations**
- Contextual nudges: "3 of 5 team members below threshold on till reconciliation"
- Suggested action: pre-drafted messaging templates for managers to re-teach topics or assign micro-lessons
- A/B tested in Q2 2024: teams that use recommendations show +12% improvement in follow-up scores

**Custom Report Builder**
- 15 pre-built report templates: completion rates, knowledge by department, compliance status, engagement trends, ROI estimator
- Drag-and-drop custom report builder: select dimensions (time period, department, topic, learner segment), metrics (completion %, avg score, streak %), and visualizations (charts, tables, heatmaps)
- Export: CSV, PDF, PowerPoint
- Scheduling: email reports daily, weekly, or monthly

**HRIS Integrations (Bi-Directional Sync)**
- **Workday**: learner data (name, ID, department, location, manager), auto-enroll new hires, de-enroll on termination
- **SAP SuccessFactors**: similar sync; also pulls org chart data for hierarchy-aware analytics
- **BambooHR**: learner data and org structure for SMB customers
- Sync frequency: daily (configurable)
- Net result: HR team doesn't manually maintain learner lists

**Executive Dashboard**
- Top-line metrics: NPS (Net Promoter Score from learners), completion rates (%), compliance status (% passing mandatory modules), ROI estimator (time saved + performance uplift dollar value)
- Trends: month-over-month growth in engagement, knowledge improvement, compliance
- Customizable: executives can add company-specific KPIs

---

## Product 3: Axonify Connect (Communications)

A communications module available on Business and Enterprise tiers. Enables companies to send targeted learning nudges, task acknowledgments, and emergency notifications.

### Key Capabilities

**Push Notifications**
- Send push notifications to learner mobile apps with rich content: title, body, action deep-link (e.g., "Complete food safety module")
- Segmentation: target by role, location, department, learner segment (e.g., "new hires"), or custom audience
- Schedule: send now or schedule for future date/time (ISO 8601)
- Engagement tracking: track open rate, click-through rate per notification

**Digital Newsletter Builder**
- Drag-and-drop WYSIWYG editor with 12 templates
- Sections: hero image, text blocks, learning module highlights, announcements, team shout-outs, images/videos
- Auto-personalization: insert learner name, department, or performance data (e.g., "Sarah, you're #3 on the leaderboard!")
- Distribution: email or in-app notification to segmented audience
- A/B testing: send version A vs. B to sample, auto-scale winner

**Task Assignment & Acknowledgment Tracking**
- Assign tasks to learners: "Read updated COVID protocol" with a due date
- Learner action: read document + submit acknowledgment (checkbox + optional signature)
- Audit trail: who read, when, IP address — exportable for compliance
- Use case: critical policy updates, safety procedures, regulatory changes

**Two-Way Pulse Surveys**
- Send 5-question max surveys to learner segments
- Response format: Likert scale, multiple choice, open-ended
- Time window: survey closes after 48 hours
- Real-time dashboard: response rate, sentiment analysis on open-ended replies
- Example: post-training survey ("Did this module help you?"), customer satisfaction, NPS

**Emergency Broadcast (Enterprise Only)**
- Push + Email + SMS simultaneously
- Recipient: all learners or specific segments
- Use case: critical safety alert, compliance incident, system status update
- Delivery: within 2 minutes to 95% of audience

---

## Integration Ecosystem

**Human Resources Information Systems (HRIS)**
- Workday, SAP SuccessFactors, BambooHR
- Syncs: learner profiles, org hierarchy, manager assignments, terminations
- SSO: SAML 2.0 and OIDC/OAuth2 via these providers

**Collaboration Tools**
- **Slack**: learning nudges posted in team channels (e.g., #engineering, #retail-ops); learners click to open Axonify app
- **Microsoft Teams**: Axonify tab embedded in Teams, learners access Learn directly from Teams interface; Connect notifications via Teams chat

**Learning Standards**
- SCORM 1.2 and SCORM 2004: import packages from legacy LMS
- xAPI/TinCan: modern learner event standard; Axonify publishes all learner events as xAPI statements to an LRS (Learning Record Store)
- AICC: legacy standard, supported for backward compatibility

**Authentication & SSO**
- SAML 2.0: tested with Okta, Azure AD, Ping Identity, OneLogin
- OIDC/OAuth2: Google Workspace, Microsoft 365 Entra ID
- Multi-factor authentication (MFA) enforced for admins, optional for learners

**Data Export**
- CSV: learner data, completion records, knowledge scores, event logs
- JSON: structured event data
- xAPI statements: full learner events in xAPI format for submission to external LRS

---

## Platform Architecture & Tenancy

All three products (Learn, Insights, Connect) share a single **learner identity layer** and **tenant data model**. Each customer is a discrete tenant with:
- Dedicated RDS PostgreSQL schema + TimescaleDB hypertable for events
- Isolated Qdrant namespace (for future RAG per-customer context)
- Branded subdomain: `learn.customername.com` (configurable to customer domain via CNAME)

**Customization & White-Labeling**
- All tiers: branded subdomain + company logo + primary/secondary color customization
- Business tier: adds custom domain support (e.g., learning.mycompany.com)
- Enterprise tier: white-label mobile app (custom bundle ID, custom splash screens, App Store presence)

**SLA & Uptime**
- Starter tier: 99.5% uptime SLA
- Business tier: 99.9% uptime SLA
- Enterprise tier: 99.95% uptime SLA (with financial penalties for breach)
