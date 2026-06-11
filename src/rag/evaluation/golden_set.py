"""Golden evaluation set for RAGAS evaluation."""

GOLDEN_QA_PAIRS = [
    # Factual (5)
    {
        "question": "What is Axonify's current ARR and how many enterprise customers do they have?",
        "ground_truth": "$42.1M ARR, 180 enterprise customers",
    },
    {
        "question": "What encryption standards does Axonify use for data at rest and in transit?",
        "ground_truth": "AES-256 at rest, TLS 1.3 in transit",
    },
    {
        "question": "What is the maximum hotel expense allowed per night for US employees?",
        "ground_truth": "$250 USD per night",
    },
    {
        "question": "Who co-founded Axonify and where is the company headquartered?",
        "ground_truth": "Priya Mehta and James Okonkwo, headquartered in Waterloo, Ontario",
    },
    {
        "question": "What rate limit applies to the Axonify REST API?",
        "ground_truth": "1,000 requests per minute per tenant",
    },
    # Multi-hop (5)
    {
        "question": "The postmortem recommended adding a dead-letter queue — is that now reflected in the data pipeline runbook?",
        "ground_truth": "Yes — action item AI-2 (DLQ + exponential backoff) is marked DONE, and the runbook describes the DLQ on sre-scheduler-pipeline publishing to sre.schedule.dlq",
    },
    {
        "question": "Which ADR was partly motivated by the increase in support tickets, and what is its current status?",
        "ground_truth": "ADR-019 (RAG-based contextual help), status is In Progress with a Q4 2024 target",
    },
    {
        "question": "What Kafka topics are involved in the SRE pipeline, and what incident exposed risks in that pipeline?",
        "ground_truth": "sre.schedule.requested, sre.schedule.computed, sre.result.delivered; INC-2024-0312 exposed disk exhaustion risk",
    },
    {
        "question": "What DORA metrics did engineering achieve in Q3 2024, and what practices in the handbook support those?",
        "ground_truth": "Lead time 2.3 days, MTTR 41 min, CFR 4.2%; supported by GitHub Flow, blue-green deploys, pre-commit hooks",
    },
    {
        "question": "Is FedRAMP certification complete, and which pricing tier includes it as an option?",
        "ground_truth": "Not complete — in progress, target Q3 2025; available as an option in the Enterprise tier",
    },
    # Summarization (5)
    {
        "question": "Summarize all action items from the March 2024 incident and their current completion status.",
        "ground_truth": "AI-1 disk alert (DONE), AI-2 DLQ + backoff (DONE), AI-3 retention limits (DONE), AI-4 PR checklist (DONE), AI-5 chaos drill (IN PROGRESS)",
    },
    {
        "question": "What is the complete onboarding timeline for a new enterprise customer, week by week?",
        "ground_truth": "Pre-kickoff (T-7): provisioning and welcome kit. Day 0 kickoff. Week 1: tenant setup, branding, SSO. Week 2: content and learner upload. Week 3: pilot launch. Week 4: full launch. Day 90: success review.",
    },
    {
        "question": "Summarize Axonify's Q3 2024 performance across financial, product, and engineering dimensions.",
        "ground_truth": "ARR $42.1M (+31% YoY), NRR 118%, 23 new logos; shipped Slack integration and knowledge gap predictions; 99.97% uptime, 0 P0 incidents, MTTR 41 min, NPS 67",
    },
    {
        "question": "What are all the leave and benefit policies for employees based in Canada?",
        "ground_truth": "15 PTO + 10 sick + 6 personal days, 18 weeks primary parental leave, RSUs with 4-year vest, extended health/dental/vision, group RRSP 4% match, $500 wellness, $2000 L&D",
    },
    {
        "question": "List all external integrations Axonify supports across its product suite.",
        "ground_truth": "Workday, SAP SuccessFactors, BambooHR, Slack, Microsoft Teams, SCORM 1.2/2004, xAPI/TinCan, AICC, SAML 2.0, OIDC (Okta, Azure AD, Ping Identity, OneLogin)",
    },
    # Adversarial/Edge (5)
    {
        "question": "What is Axonify's refund policy for Enterprise customers?",
        "ground_truth": "No refund after 60 days from contract start; pro-rated refund within days 31–60; full refund only if Axonify commits material breach",
    },
    {
        "question": "What are the exact steps to resolve a Kafka consumer lag alert?",
        "ground_truth": "1. Describe consumer group with kafka-consumer-groups.sh. 2. Check worker logs in Datadog. 3. Scale up ECS service if workers healthy. 4. If disk issue, see INC-2024-0312 playbook.",
    },
    {
        "question": "When was Axonify's SOC 2 Type II last renewed?",
        "ground_truth": "2024 (renewed by Deloitte)",
    },
    {
        "question": "What is the minimum learner count required for a Business tier contract?",
        "ground_truth": "1,000 learners",
    },
    {
        "question": "What was the total duration of the March 2024 P0 incident?",
        "ground_truth": "5 hours and 25 minutes (14:22 UTC to 19:47 UTC on March 12, 2024)",
    },
]


def get_golden_set() -> list[dict]:
    """Return the golden QA pairs for evaluation."""
    return GOLDEN_QA_PAIRS
