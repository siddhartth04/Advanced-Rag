# Axonify REST API v2 Documentation

**Base URL:** `https://api.axonify.com/v2`

**Authentication:** OAuth2 client credentials flow → Bearer JWT token (valid 1 hour)

**Response Format:** All responses are JSON (`Content-Type: application/json`)

**Pagination:** Cursor-based pagination with `next_cursor` field in response. Maximum 200 results per page.

---

## Authentication

### POST /auth/token

Obtain an access token using OAuth2 client credentials.

**Request:**
```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "grant_type": "client_credentials"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Use the access token for all subsequent requests:**
```
Authorization: Bearer {access_token}
```

---

## Learner Management

### GET /learners

List all learners in the tenant.

**Query Parameters:**
- `department` (optional, string): filter by department name
- `location` (optional, string): filter by location/store number
- `status` (optional, enum): `active`, `inactive`, or `pending` (learners awaiting first login)
- `cursor` (optional, string): pagination cursor from previous request
- `limit` (optional, integer): results per page, max 200, default 50

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "learner_123abc",
      "email": "sarah@retailco.com",
      "first_name": "Sarah",
      "last_name": "Chen",
      "department": "Checkout",
      "location": "Store #42",
      "status": "active",
      "enrolled_at": "2024-01-15T10:30:00Z",
      "last_active_at": "2024-06-12T14:22:00Z"
    }
  ],
  "next_cursor": "eyJvZmZzZXQiOiA1MCwgInNlYXJjaF9hZnRlciI6ICI5OTkifQ==",
  "total_count": 2847
}
```

### POST /learners

Create a new learner in the tenant.

**Request Body:**
```json
{
  "email": "jane@retailco.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "department": "Stockroom",
  "location": "Store #42",
  "role": "Associate",
  "external_id": "EMP-00847"
}
```

**Response (201 Created):**
```json
{
  "id": "learner_456def",
  "email": "jane@retailco.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "department": "Stockroom",
  "location": "Store #42",
  "status": "pending",
  "created_at": "2024-06-12T15:45:00Z"
}
```

### PUT /learners/{id}

Update a learner (supports partial updates).

**Request Body (example: update department):**
```json
{
  "department": "Management"
}
```

**Response (200 OK):** Updated learner object

---

### GET /learners/{id}/progress

Fetch detailed progress for a specific learner.

**Response (200 OK):**
```json
{
  "learner_id": "learner_123abc",
  "overall_knowledge_score": 0.87,
  "streak_days": 23,
  "total_sessions": 156,
  "module_progress": [
    {
      "module_id": "mod_001",
      "module_name": "Food Safety Fundamentals",
      "completion_pct": 1.0,
      "last_score": 0.95,
      "last_completed_at": "2024-06-11T08:15:00Z",
      "next_due_at": "2024-06-16T08:00:00Z"
    },
    {
      "module_id": "mod_042",
      "module_name": "Till Reconciliation",
      "completion_pct": 0.6,
      "last_score": 0.78,
      "last_completed_at": "2024-06-10T09:30:00Z",
      "next_due_at": "2024-06-13T08:00:00Z"
    }
  ]
}
```

---

## Content Management

### POST /content/modules

Upload a SCORM package (zip file) to create a new module.

**Request:** Multipart form data
- `file` (required, binary): SCORM 1.2 or 2004 package (zip, max 500 MB)
- `title` (required, string): module name
- `language` (optional, string): language code (e.g., "en", "fr", "ar"), default "en"
- `tags[]` (optional, array): tags for categorization

**Response (202 Accepted):**
```json
{
  "module_id": "mod_789ghi",
  "title": "Customer Service Excellence",
  "status": "processing",
  "estimated_ready_in_seconds": 120
}
```

**Note:** SCORM packages are processed asynchronously. Poll `/content/modules/{module_id}` to check status. Estimated processing time: 2–5 minutes for typical packages.

---

## Analytics & Reporting

### GET /analytics/knowledge-gaps

Generate a knowledge gap report showing topics where learners are underperforming.

**Query Parameters:**
- `date_from` (required, ISO 8601): start date (e.g., "2024-05-01")
- `date_to` (required, ISO 8601): end date
- `department` (optional, string): filter by department
- `topic_id` (optional, string): filter by topic
- `threshold` (optional, float 0.0–1.0): knowledge score threshold, default 0.6 (60%)

**Response (200 OK):**
```json
{
  "gaps": [
    {
      "topic_id": "topic_001",
      "topic_name": "Food Safety Certification",
      "department": "Checkout",
      "avg_score": 0.52,
      "learners_below_threshold": 47,
      "total_learners_in_department": 156,
      "recommended_action": "Assign 'Food Safety Refresh' module to all in Checkout"
    },
    {
      "topic_id": "topic_042",
      "topic_name": "Till Reconciliation",
      "department": "Stockroom",
      "avg_score": 0.71,
      "learners_below_threshold": 8,
      "total_learners_in_department": 102,
      "recommended_action": null
    }
  ],
  "generated_at": "2024-06-12T16:00:00Z"
}
```

---

## Notifications

### POST /notifications/push

Send a push notification to a learner segment.

**Request Body:**
```json
{
  "title": "New Food Safety Module",
  "body": "Complete the updated food safety module by Friday.",
  "segment": {
    "departments": ["Checkout", "Stockroom"],
    "locations": ["Store #42", "Store #15"],
    "learner_ids": null
  },
  "action_url": "/modules/mod_001",
  "schedule_at": null
}
```

- `segment`: all three fields optional; if omitted, sends to all learners
- `action_url`: deep-link into the Axonify app (e.g., direct to a module)
- `schedule_at`: ISO 8601 datetime for scheduled delivery; null = send immediately

**Response (200 OK):**
```json
{
  "notification_id": "notif_12345",
  "recipients_count": 4823,
  "status": "queued",
  "estimated_delivery_at": "2024-06-12T16:05:00Z"
}
```

---

## Reporting & Export

### GET /reports/completion

Export a completion report (CSV or JSON).

**Query Parameters:**
- `date_from` (required, ISO 8601)
- `date_to` (required, ISO 8601)
- `format` (required, enum): `json` or `csv`
- `department` (optional, string): filter by department

**Response (200 OK, Content-Type: text/csv or application/json):**

CSV format has columns:
```
learner_id,first_name,last_name,email,department,location,module_name,completion_date,score,time_spent_seconds
learner_123,Sarah,Chen,sarah@retailco.com,Checkout,"Store #42",Food Safety Fundamentals,2024-06-11,0.95,180
learner_456,Jane,Smith,jane@retailco.com,Stockroom,"Store #42",Till Reconciliation,2024-06-10,0.78,240
```

---

## Rate Limiting & Error Handling

**Rate Limits:**
- 1,000 requests per minute per tenant
- Remaining quota: `X-RateLimit-Remaining` response header
- Reset time: `X-RateLimit-Reset` response header (Unix timestamp)

**Error Format (4xx/5xx):**
```json
{
  "error": {
    "code": "LEARNER_NOT_FOUND",
    "message": "No learner with id 'learner_xyz'",
    "request_id": "req_abc123xyz"
  }
}
```

Common error codes:
- `INVALID_REQUEST`: malformed request body
- `LEARNER_NOT_FOUND`: 404 for learner not found
- `UNAUTHORIZED`: missing or invalid API token
- `RATE_LIMITED`: exceeded rate limit
- `INTERNAL_ERROR`: server error

---

## Webhooks

Register webhooks at `POST /webhooks`. Axonify will POST to your endpoint when events occur.

**Supported Events:**
- `learner.completed`: learner completed a module
- `learner.streak_broken`: learner missed a day of learning
- `knowledge_gap.detected`: learner's score dropped below threshold

**Webhook Payload Example (learner.completed):**
```json
{
  "event_type": "learner.completed",
  "tenant_id": "tenant_12345",
  "timestamp": "2024-06-12T15:45:00Z",
  "data": {
    "learner_id": "learner_123abc",
    "module_id": "mod_001",
    "module_name": "Food Safety Fundamentals",
    "score": 0.95,
    "time_spent_seconds": 420
  }
}
```

---

## SDKs

**Official SDKs:**
- **Python**: `pip install axonify-sdk`
- **Node.js**: `npm install @axonify/sdk`
- **Java**: Maven Central, `com.axonify:axonify-sdk:1.0.0`

**SDK Documentation:** https://docs.axonify.com/sdks

---

## API Status & Monitoring

Check service status: **https://status.axonify.com**

API uptime targets:
- Starter tier: 99.5%
- Business tier: 99.9%
- Enterprise tier: 99.95%
