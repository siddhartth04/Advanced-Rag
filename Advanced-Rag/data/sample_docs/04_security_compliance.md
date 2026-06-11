# Axonify Security & Compliance

## Certifications & Compliance Status

**SOC 2 Type II**
- Status: Certified (valid through 2025)
- Initial audit: 2022 by Deloitte
- Renewal: 2024 by Deloitte (expires Q3 2025)
- Coverage: Security, Availability, and Confidentiality trust principles
- Report available under NDA to Enterprise customers

**GDPR (General Data Protection Regulation)**
- Status: Fully compliant since 2021
- Data Processing Agreement (DPA): available on request for Business and Enterprise tiers
- EU data residency: available in AWS eu-west-1 (Frankfurt)
- Data subject rights: customers can export or delete learner data via API

**CCPA (California Consumer Privacy Act)**
- Status: Compliant
- Privacy policy: updated Q1 2024 to reflect CCPA consumer rights
- Applicable to customers with California learners

**ISO 27001**
- Status: In progress, target certification Q2 2025
- Gap assessment: completed October 2024
- Covers: information security management system

**FedRAMP Moderate**
- Status: In progress, target authorization Q3 2025
- Applicable: US government customers
- Assessor: external third-party assessment organization (under procurement)

**PIPEDA (Personal Information Protection and Electronic Documents Act)**
- Status: Compliant (Canada's federal privacy law)
- Relevant for Canadian customers

---

## Encryption

**At Rest**
- Database encryption: AES-256 on all RDS PostgreSQL instances, TimescaleDB hypertables, and S3 buckets
- Key management: AWS KMS (customer-managed key option on Enterprise tier)
- Backup encryption: daily snapshots retained 30 days, encrypted by KMS
- S3 lifecycle: older backups transitioned to Glacier (cold archive) after 30 days

**In Transit**
- TLS 1.3 enforced on all public endpoints
- Legacy protocols: TLS 1.0 and TLS 1.1 are deprecated and blocked (certificate negotiation fails if client requests these)
- Certificate authority: AWS Certificate Manager (auto-renewed)
- HSTS: enabled, 1-year max-age

**Application-Level**
- Learner session tokens: stored as hashed JWTs in Redis (ephemeral)
- API credentials: AWS Secrets Manager, rotated every 90 days
- LLM API keys: stored in Secrets Manager, never logged

---

## Data Residency

**Three Regions Available:**
- **US (default)**: AWS us-east-1 (N. Virginia) + us-west-2 (Oregon) for redundancy
- **EU**: AWS eu-west-1 (Frankfurt) — GDPR-compliant data residency
- **Canada**: AWS ca-central-1 (Canada Central) — meets domestic data residency requirements

**Selection:** Residency is chosen at tenant provisioning (contract signing). Cannot change post-signup without manual data migration (rarely requested).

**Cross-border transfers:** None. Learner data never leaves the selected region except for backups (stored in the same region).

---

## Access Control

**Role-Based Access Control (RBAC)**
Five default roles (customizable on Enterprise tier):
1. **Super Admin**: full platform access, manages other admins, billing, tenant settings
2. **Tenant Admin**: manages all content, users, and reports within tenant
3. **Manager**: views team knowledge gaps, sends notifications, assigns modules
4. **Content Author**: creates/uploads SCORM modules, manages content libraries
5. **Learner**: access to Learn app, basic Insights dashboard

**Single Sign-On (SSO)**
- SAML 2.0: tested with Okta, Azure AD, Ping Identity, OneLogin
- OIDC/OAuth2: Google Workspace, Microsoft 365 Entra ID (Azure AD)
- Automatic role assignment: based on SAML attributes (e.g., department from HRIS)

**Multi-Factor Authentication (MFA)**
- Enforced: all Super Admin and Tenant Admin roles
- Optional: Manager role (configurable by tenant)
- Methods: TOTP (Google Authenticator, Authy), SMS (for legacy systems)

**Principle of Least Privilege**
- IAM policies reviewed quarterly
- Service-to-service communication: API keys with minimal scopes
- Database: application user has SELECT/INSERT/UPDATE, no DDL or DROP permissions
- Kafka: producer role for API service, consumer role for analytics pipeline, no admin access

---

## Network Security

**Web Application Firewall (WAF)**
- AWS WAF on all public endpoints (api.axonify.com, app.axonify.com, cdn.axonify.com)
- Ruleset: OWASP Top 10 AWS managed rules + custom rules
- Custom rules: rate limiting (500 req/min per IP), SQL injection patterns, XSS payloads
- False positive rate: monitored weekly, rules refined monthly

**DDoS Protection**
- AWS Shield Standard: baseline protection included with AWS
- AWS Shield Advanced: recommended for Enterprise tier (can be added)
- Mitigation: automatic rate-based rules on regional/CloudFront layer

**Network Segmentation**
- VPC isolation per environment: dev, staging, production
- No public database endpoints (RDS, Redshift)
- Jump host (bastion): required for accessing production databases (SSH key-based)
- VPC peering: internal only (e.g., Kafka brokers to app servers)

**Secrets Management**
- AWS Secrets Manager: centralized secret storage
- Rotation: automatic 90-day rotation for database passwords, API keys
- Access: gated by IAM policy (only service roles have access)
- Audit: CloudTrail logs all secret access

---

## Penetration Testing & Vulnerability Management

**Annual Penetration Testing**
- Vendor: CrowdStrike
- Most recent: October 2023 (annual test)
- Scope: api.axonify.com, app.axonify.com, mobile app (iOS and Android)

**Oct 2023 Pen Test Results:**
- 0 critical findings
- 2 high-severity findings (both remediated within 14 days)
- 7 medium-severity findings (all remediated within 30 days)
- 4 low-severity findings (in backlog, planned for next quarter)

**Bug Bounty Program**
- Platform: HackerOne (private program)
- Scope: api.axonify.com, app.axonify.com, mobile apps
- Payout range: $100–$5,000 depending on severity
- Response SLA: 48 hours to triage, 7 days to confirm fix commitment

---

## Incident Response

**SLA by Severity:**
- **P0 (full outage, data breach risk)**: 30-minute response SLA, 4-hour resolution target
  - Example: Kafka disk exhaustion (INC-2024-0312)
  - Escalation: CTO, VP Engineering, VP Ops
- **P1 (partial outage, significant degradation)**: 2-hour response SLA, 8-hour resolution target
  - Example: analytics API latency >5 seconds for >5 minutes
  - Escalation: on-call SRE, VP Ops
- **P2 (minor degradation, workaround available)**: 8-hour response SLA, 24-hour resolution target
  - Example: non-critical feature slow
  - Escalation: team lead

**Post-Mortems**
- Required for: P0 and P1 incidents
- Timeline: published within 5 business days of incident resolution
- Access: internal only (employee handbook in Notion)
- Example: INC-2024-0312 post-mortem is company's only P0 incident

---

## Data Retention & Deletion

**Learner Event Data**
- Retention: 7 years (required for some enterprise customers in regulated industries: healthcare, finance)
- Location: hot storage (TimescaleDB) for 90 days, cold storage (S3 Glacier) for remainder

**Application Logs**
- CloudWatch retention: 90 days
- S3 archive: 1 year in cold storage
- Purged: logs older than 1 year

**Database Backups**
- Daily snapshots: retained for 30 days
- Weekly snapshots: retained for 1 year
- Long-term archives: some backups archived in S3 (negotiable per customer contract)

**Contract Termination Data Lifecycle**
- Data export window: 30 days from contract end date
  - Formats: CSV (learner data, completion records) and xAPI statements (full event log)
  - Delivery: SFTP or secure download link
- Deletion: 60 days after contract end, all data deleted from production and backup systems
- Compliance: documented in Data Processing Agreement

---

## Third-Party Vendor Management

**Annual Vendor Assessment**
- All critical vendors required to provide SOC 2 report
- Assessment criteria: security controls, data protection, incident response

**Critical Vendors:**
- **AWS** (infrastructure): SOC 2 Type II certified
- **Datadog** (observability): SOC 2 Type II certified
- **PagerDuty** (alerting): SOC 2 Type II certified
- **Okta** (internal SSO): SOC 2 Type II certified
- **HackerOne** (bug bounty): audited annually
- **Deloitte** (compliance audit): Big 4 firm

**Vendor Risk Reviews:** completed every January; escalations to VP Ops if vendor risk score drops below acceptable threshold.

---

## Compliance Roadmap

- **Q2 2025**: ISO 27001 certification (target)
- **Q3 2025**: FedRAMP Moderate authorization (target)
- **2026**: SOC 2 Type II renewal (next biennial cycle)
