# Personal AI Employee - System Architecture Documentation

**Version:** 1.0
**Last Updated:** 2026-03-10
**Status:** Production Ready

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [File Structure](#file-structure)
7. [Integration Points](#integration-points)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [Error Handling & Recovery](#error-handling--recovery)
11. [Monitoring & Logging](#monitoring--logging)
12. [Scalability & Performance](#scalability--performance)
13. [Future Roadmap](#future-roadmap)

---

## System Overview

### Purpose

The Personal AI Employee is an autonomous system that monitors, processes, and manages communications (email, WhatsApp) and tasks, providing a centralized command center through Obsidian with comprehensive audit logging and error recovery.

### Key Features

- **Automated Email Monitoring** - Gmail API integration with OAuth 2.0
- **WhatsApp Chat Processing** - Manual export processing with auto-detection
- **Centralized Dashboard** - Obsidian-based visual command center
- **Comprehensive Audit Logging** - JSON-based event tracking
- **Error Recovery** - Exponential backoff retry with graceful degradation
- **Weekly CEO Briefing** - Automated executive summaries
- **MCP Server Integration** - Claude Code integration for AI assistance
- **Task Management** - Kanban-style workflow tracking

### Design Principles

1. **Resilience First** - System continues operating despite failures
2. **Observability** - All actions logged and auditable
3. **Modularity** - Components can be added/removed independently
4. **Security** - OAuth 2.0, no plaintext credentials, minimal permissions
5. **User-Centric** - Obsidian UI for easy access and management

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     PERSONAL AI EMPLOYEE                         │
│                      System Architecture                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │  Gmail API   │         │  WhatsApp    │                     │
│  │  (OAuth 2.0) │         │  Exports     │                     │
│  └──────┬───────┘         └──────┬───────┘                     │
│         │                        │                              │
└─────────┼────────────────────────┼──────────────────────────────┘
          │                        │
          ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PROCESSING LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐    ┌────────────────────────┐      │
│  │  Gmail Watcher         │    │  WhatsApp Monitor      │      │
│  │  Enhanced              │    │  Enhanced              │      │
│  ├────────────────────────┤    ├────────────────────────┤      │
│  │ - OAuth Auth           │    │ - File Detection       │      │
│  │ - Email Fetching       │    │ - Chat Parsing         │      │
│  │ - Retry Logic          │    │ - Retry Logic          │      │
│  │ - Health Monitoring    │    │ - Health Monitoring    │      │
│  │ - Audit Logging        │    │ - Audit Logging        │      │
│  └────────┬───────────────┘    └────────┬───────────────┘      │
│           │                             │                       │
│           └──────────┬──────────────────┘                       │
│                      │                                          │
└──────────────────────┼──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              AI_Employee_Vault/                         │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │  ├─ Dashboard.md          (Main command center)        │    │
│  │  ├─ Kanban Board.md       (Task workflow)              │    │
│  │  ├─ CEO_Briefing.md       (Weekly summary)             │    │
│  │  ├─ Audit_Logs.md         (System events)              │    │
│  │  ├─ Emails/               (Email action files)         │    │
│  │  ├─ WhatsApp_Chats/       (Chat action files)          │    │
│  │  ├─ Needs_Action/         (Pending tasks)              │    │
│  │  ├─ In_Progress/          (Active tasks)               │    │
│  │  ├─ Done/                 (Completed tasks)            │    │
│  │  └─ .obsidian/            (Obsidian config + CSS)      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              logs/                                      │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │  ├─ audit.jsonl                (Centralized audit log) │    │
│  │  ├─ gmail-watcher-detailed.log (Gmail debug logs)      │    │
│  │  └─ whatsapp-monitor-detailed.log (WhatsApp debug)     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Obsidian Vault                             │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │  - Card-based Dashboard                                │
│  │  - Kanban Board View                                   │    │
│  │  - CEO Briefing Reports                                │    │
│  │  - Audit Log Viewer                                    │    │
│  │  - Custom CSS Styling                                  │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐    ┌────────────────────────┐      │
│  │  MCP Server (Email)    │    │  MCP Server (WhatsApp) │      │
│  │  (Future)              │    │  (Future)              │      │
│  └────────────────────────┘    └────────────────────────┘      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Claude Code Integration                    │    │
│  │              (AI Assistant Access)                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   CROSS-CUTTING CONCERNS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Audit Logger │  │ Error        │  │ Health       │         │
│  │ (audit_      │  │ Recovery     │  │ Monitoring   │         │
│  │  logger.py)  │  │ (Retry +     │  │ (Consecutive │         │
│  │              │  │  Backoff)    │  │  Failures)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Gmail Watcher Enhanced

**File:** `watcher/gmail_watcher_enhanced.py`

**Purpose:** Monitors Gmail inbox for important emails and converts them to action files.

**Key Features:**
- OAuth 2.0 authentication with token refresh
- Fetches unread important emails every 2 minutes
- Retry logic with exponential backoff (3 attempts)
- Graceful degradation (continues on failure)
- Health monitoring (consecutive failure tracking)
- Comprehensive audit logging
- Automatic re-authentication after 5 failures

**Dependencies:**
- `google-auth`
- `google-auth-oauthlib`
- `google-api-python-client`
- `audit_logger`

**Configuration:**
```python
CHECK_INTERVAL = 120  # 2 minutes
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 60  # seconds
CONSECUTIVE_FAILURE_THRESHOLD = 5
```

---

### 2. WhatsApp Monitor Enhanced

**File:** `whatsapp_integration/whatsapp_monitor_enhanced.py`

**Purpose:** Monitors folder for WhatsApp chat exports and converts them to action files.

**Key Features:**
- File-based monitoring (whatsapp_inbox/)
- Chat parsing with regex pattern matching
- Encoding fallback (UTF-8 → Latin-1)
- Retry logic with exponential backoff
- Graceful degradation
- Health monitoring
- Comprehensive audit logging

**Dependencies:**
- `audit_logger`
- Standard library (re, pathlib, datetime)

**Configuration:**
```python
CHECK_INTERVAL = 60  # 1 minute
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1  # seconds
MAX_RETRY_DELAY = 30  # seconds
CONSECUTIVE_FAILURE_THRESHOLD = 5
```

---

### 3. Audit Logger

**File:** `audit_logger.py`

**Purpose:** Centralized logging system for all system events.

**Key Features:**
- JSON Lines (JSONL) format
- Rotating file handler (10 MB max, 5 backups)
- Event type categorization
- Component-specific loggers
- Log reader with filtering
- Statistics generation
- Report generation

**Event Types:**
- Email events (received, sent, processed, error)
- WhatsApp events (received, sent, processed, error)
- System events (start, stop, error, health_check)
- Authentication events (success, failure, refresh)
- File operations (created, moved, deleted, error)
- MCP events (request, response, error)

**Log Format:**
```json
{
  "timestamp": "2026-03-10T19:57:25.976343",
  "component": "gmail_watcher",
  "event_type": "email_received",
  "action": "New important email detected",
  "status": "success",
  "details": {"email_id": "19c85882"},
  "metadata": {}
}
```

---

### 4. Obsidian Vault

**Directory:** `AI_Employee_Vault/`

**Purpose:** Visual command center and knowledge base.

**Structure:**
```
AI_Employee_Vault/
├── Dashboard.md              # Main command center
├── Kanban Board.md           # Task workflow view
├── CEO_Briefing.md           # Weekly executive summary
├── Audit_Logs.md             # System event viewer
├── Emails/                   # Email action files
├── WhatsApp_Chats/           # Chat action files
├── Needs_Action/             # Pending tasks
├── In_Progress/              # Active tasks
├── Done/                     # Completed tasks
├── Pending_Approval/         # Awaiting approval
└── .obsidian/
    ├── workspace.json        # Obsidian settings
    └── snippets/
        └── dashboard-style.css  # Custom styling
```

**Features:**
- Card-based dashboard layout
- Kanban board visualization
- Custom CSS styling with animations
- Dark mode support
- Responsive design
- Internal linking between notes

---

### 5. Report Generators

#### CEO Briefing Generator

**File:** `generate_ceo_briefing.py`

**Purpose:** Generate weekly executive summary with key metrics and recommendations.

**Features:**
- Email statistics (total, new, avg per day)
- WhatsApp statistics (total, new, avg per day)
- Task completion metrics
- System health metrics
- Trend analysis
- Actionable recommendations
- Notable events summary

#### Audit Summary Generator

**File:** `generate_audit_summary.py`

**Purpose:** Generate Obsidian-formatted audit log summary.

**Features:**
- Recent events (last 20)
- Statistics (last 7 days)
- Component breakdown
- Event type breakdown
- Success rate calculation
- Visual formatting with emojis

---

## Data Flow

### Email Processing Flow

```
1. Gmail API
   ↓
2. Gmail Watcher Enhanced
   ├─ Authenticate (OAuth 2.0)
   ├─ Fetch unread important emails
   ├─ Check if already processed
   └─ For each new email:
      ├─ Get email details (subject, sender, body)
      ├─ Create action file (EMAIL-{id}-{subject}.md)
      ├─ Save to AI_Employee_Vault/Emails/
      ├─ Log to audit.jsonl
      └─ Mark as processed
   ↓
3. Obsidian Vault
   ├─ Display in Dashboard
   ├─ Show in Kanban Board
   └─ Include in CEO Briefing
```

### WhatsApp Processing Flow

```
1. User exports WhatsApp chat
   ↓
2. User saves to whatsapp_inbox/
   ↓
3. WhatsApp Monitor Enhanced
   ├─ Detect new .txt file
   ├─ Parse chat messages (regex)
   ├─ Extract contact name and messages
   ├─ Create action file (WHATSAPP-{timestamp}-{contact}.md)
   ├─ Save to AI_Employee_Vault/WhatsApp_Chats/
   ├─ Log to audit.jsonl
   └─ Mark as processed
   ↓
4. Obsidian Vault
   ├─ Display in Dashboard
   ├─ Show in Kanban Board
   └─ Include in CEO Briefing
```

### Audit Logging Flow

```
1. Component (Gmail Watcher, WhatsApp Monitor, etc.)
   ↓
2. AuditLogger.log_event()
   ├─ Format event as JSON
   ├─ Add timestamp, component, status
   └─ Write to logs/audit.jsonl
   ↓
3. AuditLogReader
   ├─ Read and filter logs
   ├─ Generate statistics
   └─ Create reports
   ↓
4. Report Generators
   ├─ generate_audit_summary.py → Audit_Logs.md
   └─ generate_ceo_briefing.py → CEO_Briefing.md
   ↓
5. Obsidian Vault
   └─ Display in dashboard
```

---

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.13+ | Core language |
| google-auth | Latest | Gmail OAuth 2.0 |
| google-api-python-client | Latest | Gmail API |
| google-auth-oauthlib | Latest | OAuth flow |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| Obsidian | Latest | Knowledge base UI |
| Markdown | CommonMark | Content format |
| CSS3 | - | Custom styling |

### Storage

| Technology | Purpose |
|------------|---------|
| File System | Primary storage |
| JSON Lines | Audit logs |
| Markdown | Action files |
| Pickle | Token storage |

### Monitoring

| Technology | Purpose |
|------------|---------|
| Python logging | Standard logs |
| Audit Logger | Event tracking |
| Health checks | System monitoring |

---

## File Structure

```
Personal AI Employee/
│
├── AI_Employee_Vault/              # Obsidian vault
│   ├── Dashboard.md
│   ├── Kanban Board.md
│   ├── CEO_Briefing.md
│   ├── Audit_Logs.md
│   ├── Emails/
│   ├── WhatsApp_Chats/
│   ├── Needs_Action/
│   ├── In_Progress/
│   ├── Done/
│   ├── Pending_Approval/
│   └── .obsidian/
│       ├── workspace.json
│       └── snippets/
│           └── dashboard-style.css
│
├── watcher/                        # Gmail watcher
│   ├── gmail_watcher_enhanced.py
│   └── credentials/
│       ├── gmail_credentials.json
│       └── gmail_token.pickle
│
├── whatsapp_integration/           # WhatsApp monitor
│   ├── whatsapp_monitor_enhanced.py
│   ├── whatsapp_inbox/            # Drop zone for exports
│   └── .processed_chats.txt       # Tracking file
│
├── logs/                           # System logs
│   ├── audit.jsonl
│   ├── gmail-watcher-detailed.log
│   └── whatsapp-monitor-detailed.log
│
├── audit_logger.py                 # Audit logging module
├── generate_ceo_briefing.py        # CEO report generator
├── generate_audit_summary.py       # Audit summary generator
│
├── ARCHITECTURE.md                 # This file
├── AUDIT_LOGGING_DOCS.md          # Audit logging docs
├── ERROR_RECOVERY_DOCS.md         # Error recovery docs
├── README.md                       # Project overview
│
└── .gitignore                      # Git ignore rules
```

---

## Integration Points

### 1. Gmail API Integration

**Authentication:** OAuth 2.0 with offline access
**Scopes:** `gmail.readonly`
**Token Storage:** `watcher/credentials/gmail_token.pickle`
**Refresh:** Automatic token refresh on expiration

**API Calls:**
- `users().messages().list()` - List messages
- `users().messages().get()` - Get message details

### 2. Obsidian Integration

**Method:** File-based (markdown files)
**Sync:** Manual or via Obsidian Sync
**Styling:** Custom CSS snippets
**Plugins:** None required (vanilla Obsidian)

### 3. Claude Code Integration (MCP)

**Status:** Planned
**Method:** MCP (Model Context Protocol) servers
**Servers:**
- Email MCP Server (send/read emails)
- WhatsApp MCP Server (send messages)

### 4. Future Integrations

- Odoo 19 (accounting/business management)
- Twitter/X API (social media monitoring)
- Facebook/Instagram APIs (social media)
- Slack (team communication)
- Calendar APIs (scheduling)

---

## Security Architecture

### Authentication

**Gmail:**
- OAuth 2.0 with PKCE
- Offline access for token refresh
- Tokens stored locally (encrypted by OS)
- No plaintext passwords

**File System:**
- User-level permissions
- No world-readable files
- Credentials in .gitignore

### Data Protection

**Sensitive Data:**
- Email content (first 1000 chars only)
- No passwords or API keys in logs
- PII minimization in audit logs

**Access Control:**
- Local file system only
- No remote access
- No web interface (yet)

### Secrets Management

**Credentials:**
- `gmail_credentials.json` - OAuth client secrets
- `gmail_token.pickle` - Access/refresh tokens
- Both in `.gitignore`
- Never committed to git

---

## Deployment Architecture

### Current Deployment

**Environment:** macOS (Darwin 21.6.0)
**Python:** 3.13+
**Process Management:** nohup + background processes

**Running Services:**
```bash
# Gmail Watcher
cd watcher
nohup python3 gmail_watcher_enhanced.py > ../logs/gmail-watcher.log 2>&1 &

# WhatsApp Monitor
cd whatsapp_integration
nohup python3 whatsapp_monitor_enhanced.py > ../logs/whatsapp-monitor.log 2>&1 &
```

**Monitoring:**
```bash
# Check if running
ps aux | grep -E "gmail_watcher_enhanced|whatsapp_monitor_enhanced" | grep -v grep

# View logs
tail -f logs/gmail-watcher-detailed.log
tail -f logs/whatsapp-monitor-detailed.log
tail -f logs/audit.jsonl
```

**Stopping:**
```bash
pkill -f gmail_watcher_enhanced
pkill -f whatsapp_monitor_enhanced
```

### Future Deployment Options

1. **Systemd Services** (Linux)
2. **Docker Containers** (Cross-platform)
3. **Cloud Deployment** (AWS/GCP/Azure)
4. **Kubernetes** (Scalable)

---

## Error Handling & Recovery

### Retry Logic

**Pattern:** Exponential backoff with max delay

```python
@retry_with_backoff(max_retries=3, initial_delay=1)
def operation():
    # Operation code
    pass
```

**Behavior:**
- Attempt 1: Immediate
- Attempt 2: Wait 1s
- Attempt 3: Wait 2s
- Attempt 4: Wait 4s (max 60s)

**Applied To:**
- Gmail authentication
- Email fetching
- Email detail retrieval
- WhatsApp file parsing
- Action file creation

### Graceful Degradation

**Principle:** System continues running despite failures

**Implementation:**
- Return None on failure (not exception)
- Log error but continue loop
- Track consecutive failures
- Trigger re-authentication after threshold

**Example:**
```python
emails = get_unread_important_emails(service)
if emails is None:
    # Log warning, increment failure counter, continue
    consecutive_failures += 1
    continue
```

### Health Monitoring

**Metrics:**
- Consecutive failure count
- Last successful check timestamp
- File system status
- Service availability

**Thresholds:**
- 5 consecutive failures → Re-authentication
- 10 minutes no success → Alert (future)

---

## Monitoring & Logging

### Log Levels

1. **Standard Logs** (gmail-watcher.log, whatsapp-monitor.log)
   - INFO: Normal operations
   - WARNING: Recoverable issues
   - ERROR: Failed operations

2. **Detailed Logs** (*-detailed.log)
   - Full error traces
   - Retry attempts
   - Health check results
   - Timestamps for all operations

3. **Audit Logs** (audit.jsonl)
   - Structured JSON events
   - All system actions
   - Success/failure status
   - Detailed metadata

### Metrics Tracked

- Total events per component
- Success/failure rates
- Email processing count
- WhatsApp processing count
- System uptime
- Error frequency
- Response times (future)

### Dashboards

1. **Obsidian Dashboard** - Real-time overview
2. **Audit Logs View** - Event history
3. **CEO Briefing** - Weekly summary

---

## Scalability & Performance

### Current Capacity

- **Emails:** Unlimited (Gmail API limits apply)
- **WhatsApp:** Manual export (no API limits)
- **Storage:** File system (TB scale)
- **Logs:** 50 MB with rotation

### Performance Characteristics

- **Email Check:** 2 minutes interval
- **WhatsApp Check:** 1 minute interval
- **Log Write:** < 1ms per event
- **Report Generation:** < 1 second

### Bottlenecks

1. **Gmail API Rate Limits**
   - 250 quota units per user per second
   - 1 billion quota units per day
   - Current usage: ~10 units per check

2. **File System I/O**
   - Not a bottleneck at current scale
   - Could use database for 10,000+ files

3. **Manual WhatsApp Export**
   - Requires user action
   - Future: WhatsApp Business API

### Scaling Strategies

1. **Horizontal Scaling**
   - Multiple watchers for different accounts
   - Load balancing across instances

2. **Vertical Scaling**
   - Increase check frequency
   - Process more emails per cycle

3. **Database Migration**
   - PostgreSQL for structured data
   - Keep markdown for Obsidian

---

## Future Roadmap

### Phase 1: Core Enhancements (Q2 2026)

- [ ] MCP Server for Email (send/read via Claude)
- [ ] MCP Server for WhatsApp (send messages)
- [ ] Agent Skills conversion (modular capabilities)
- [ ] Ralph Wiggum Loop (autonomous task execution)

### Phase 2: Business Integration (Q3 2026)

- [ ] Odoo 19 installation and configuration
- [ ] Odoo MCP Server (accounting/CRM access)
- [ ] Cross-domain integration (personal + business)
- [ ] Invoice generation automation
- [ ] Expense tracking automation

### Phase 3: Social Media (Q4 2026)

- [ ] Twitter/X API integration
- [ ] Facebook API integration
- [ ] Instagram API integration
- [ ] Social media monitoring dashboard
- [ ] Automated posting capabilities

### Phase 4: Advanced Features (2027)

- [ ] Real-time web dashboard (React/Next.js)
- [ ] Mobile app (React Native)
- [ ] Voice interface (Whisper + TTS)
- [ ] Advanced analytics and ML insights
- [ ] Multi-user support
- [ ] Cloud deployment option

---

## Appendix

### A. Configuration Files

**Gmail Credentials:**
```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token"
  }
}
```

**Obsidian CSS Snippet:**
- Location: `AI_Employee_Vault/.obsidian/snippets/dashboard-style.css`
- Features: Card layout, animations, dark mode

### B. API Endpoints

**Gmail API:**
- Base URL: `https://gmail.googleapis.com/gmail/v1/`
- Auth: OAuth 2.0
- Docs: https://developers.google.com/gmail/api

### C. Dependencies

**Python Packages:**
```
google-auth>=2.0.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.0.0
```

**Install:**
```bash
pip3 install google-auth google-auth-oauthlib google-api-python-client
```

### D. Troubleshooting

**Common Issues:**

1. **Gmail authentication fails**
   - Check credentials.json exists
   - Verify OAuth consent screen configured
   - Delete token.pickle and re-authenticate

2. **WhatsApp monitor not detecting files**
   - Check whatsapp_inbox/ folder exists
   - Verify file extension is .txt
   - Check file permissions

3. **Obsidian not showing styles**
   - Enable CSS snippet in settings
   - Switch to Reading View (Cmd+E)
   - Reload Obsidian

---

**Document Version:** 1.0
**Last Updated:** 2026-03-10
**Maintained By:** Personal AI Employee Team
**Status:** ✅ Production Ready
