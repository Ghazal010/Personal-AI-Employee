# Personal AI Employee - Gold Tier Complete 🏆

A production-ready, autonomous AI assistant that manages personal and business affairs using Claude Code, Obsidian, and enterprise integrations.

## 🎯 System Status

**Bronze Tier:** ✅ Complete
**Silver Tier:** ✅ Complete
**Gold Tier:** ✅ Complete (All 11 Requirements)

## ✨ Key Features

### Personal Domain
- ✅ Gmail monitoring with enhanced watcher
- ✅ WhatsApp integration and monitoring
- ✅ Twitter/X API integration with mention tracking
- ✅ Facebook & Instagram API integration
- ✅ Task management with Obsidian Kanban

### Business Domain
- ✅ Odoo 19 ERP integration (JSON-RPC)
- ✅ Customer management (CRM)
- ✅ Invoice generation and tracking
- ✅ Expense management
- ✅ Product catalog access

### Automation & Intelligence
- ✅ Ralph Wiggum Loop - Autonomous agent
- ✅ 23 Agent Skills across 7 categories
- ✅ Cross-Domain Integration (6 workflows)
- ✅ Comprehensive audit logging system
- ✅ Weekly CEO briefing generator
- ✅ Beautiful Obsidian dashboard

## 📁 Project Structure

```
Personal AI Employee/
├── AI_Employee_Vault/              # Obsidian vault
│   ├── Dashboard.md                # Beautiful status dashboard
│   ├── CEO_Briefing.md             # Weekly business reports
│   ├── Audit_Logs.md               # System audit logs
│   ├── Kanban Board.md             # Task management
│   ├── Emails/                     # Email action files
│   ├── WhatsApp_Chats/             # WhatsApp conversations
│   ├── Inbox/                      # New items
│   ├── Needs_Action/               # Pending tasks
│   └── Done/                       # Completed items
├── agent_skills/                   # 23 Agent Skills
│   ├── skill_framework.py          # Base framework
│   ├── email_skills.py             # Email operations
│   ├── whatsapp_skills.py          # WhatsApp operations
│   ├── twitter_skills.py           # Twitter/X integration
│   ├── social_media_skills.py      # Facebook/Instagram
│   ├── odoo_skills.py              # Odoo ERP operations
│   ├── task_skills.py              # Task management
│   └── audit_skills.py             # Audit & reporting
├── watcher/                        # Monitoring systems
│   ├── gmail_watcher_enhanced.py   # Gmail monitoring
│   └── inbox_watcher.py            # File system watcher
├── twitter_integration/            # Twitter/X API
│   └── twitter_monitor.py
├── social_media_integration/       # Meta APIs
│   └── facebook_instagram_monitor.py
├── whatsapp_integration/           # WhatsApp monitoring
│   └── whatsapp_monitor.js
├── odoo_integration/               # Odoo ERP
│   ├── odoo_mcp_server.py          # JSON-RPC client
│   └── install_odoo_docker.sh      # Docker setup
├── audit_logger.py                 # Centralized logging
├── cross_domain_integration.py     # Personal ↔ Business workflows
├── ralph_wiggum_loop.py            # Autonomous agent
├── skills_cli.py                   # CLI for skills
├── generate_ceo_briefing.py        # Weekly reports
└── logs/                           # Audit logs (JSONL)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+ (for WhatsApp integration)
- Docker & Docker Compose (for Odoo)
- Claude Code CLI
- Obsidian (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ghazal010/Personal-AI-Employee.git
   cd "Personal AI Employee"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup credentials**
   ```bash
   # Gmail API
   cd watcher/credentials
   # Add your credentials.json and token.json

   # Twitter API
   cd twitter_integration/credentials
   cp twitter_credentials.json.template twitter_credentials.json
   # Edit with your API keys

   # Facebook/Instagram
   cd social_media_integration/credentials
   cp meta_credentials.json.template meta_credentials.json
   # Edit with your access tokens

   # Odoo
   cd odoo_integration/credentials
   cp odoo_credentials.json.template odoo_credentials.json
   # Edit with your Odoo credentials
   ```

4. **Install Odoo (optional)**
   ```bash
   cd odoo_integration
   ./install_odoo_docker.sh
   ```

5. **Setup WhatsApp (optional)**
   ```bash
   cd whatsapp_integration
   npm install
   ```

### Running the System

**Start the autonomous agent:**
```bash
python3 ralph_wiggum_loop.py
```

**Or run individual components:**
```bash
# Gmail watcher
python3 watcher/gmail_watcher_enhanced.py

# Twitter monitor
python3 twitter_integration/twitter_monitor.py

# WhatsApp monitor
cd whatsapp_integration && node whatsapp_monitor.js

# Generate CEO briefing
python3 generate_ceo_briefing.py

# Use skills CLI
python3 skills_cli.py --list
python3 skills_cli.py --skill GetEmailStatisticsSkill
```

## 🎮 Usage Examples

### Check System Status
```bash
# View beautiful dashboard in Obsidian
open AI_Employee_Vault/Dashboard.md

# Get email statistics
python3 skills_cli.py --skill GetEmailStatisticsSkill

# Get system health
python3 skills_cli.py --skill GetAuditStatisticsSkill
```

### Process Emails Automatically
```bash
# Start Gmail watcher (runs continuously)
python3 watcher/gmail_watcher_enhanced.py

# Emails are automatically:
# - Detected and downloaded
# - Converted to action files
# - Saved in AI_Employee_Vault/Emails/
# - Logged in audit system
```

### Social Media Monitoring
```bash
# Monitor Twitter mentions
python3 twitter_integration/twitter_monitor.py

# Get Twitter statistics
python3 skills_cli.py --skill GetTwitterStatisticsSkill

# Post a tweet
python3 skills_cli.py --skill PostTweetSkill --params '{"text": "Hello from AI!"}'
```

### Business Operations (Odoo)
```bash
# Get customers
python3 skills_cli.py --skill GetOdooCustomersSkill --params '{"limit": 10}'

# Create customer
python3 skills_cli.py --skill CreateOdooCustomerSkill --params '{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890"
}'

# Get invoices
python3 skills_cli.py --skill GetOdooInvoicesSkill --params '{"state": "posted"}'

# Create invoice
python3 skills_cli.py --skill CreateOdooInvoiceSkill --params '{
  "partner_id": 7,
  "lines": [{"product_id": 1, "quantity": 1, "price_unit": 100.0, "name": "Service"}]
}'
```

### Cross-Domain Workflows
```python
from cross_domain_integration import CrossDomainIntegration

integration = CrossDomainIntegration()

# Email → Customer (auto-create customer from email)
result = integration.execute_workflow('email_to_customer', {
    'email_from': 'John Doe <john@example.com>',
    'email_subject': 'Inquiry',
    'email_body': 'I need information...'
})

# Email → Invoice (generate invoice from email request)
result = integration.execute_workflow('email_to_invoice', {
    'email_from': 'Jane Smith <jane@example.com>',
    'email_subject': 'Invoice for consulting - $500',
    'email_body': 'Please send invoice...'
})

# WhatsApp → Customer
result = integration.execute_workflow('whatsapp_to_customer', {
    'contact_name': 'Maria Garcia',
    'phone_number': '+34612345678'
})
```

### Generate Reports
```bash
# Weekly CEO briefing
python3 generate_ceo_briefing.py

# Audit log summary
python3 generate_audit_summary.py

# View in Obsidian
open AI_Employee_Vault/CEO_Briefing.md
open AI_Employee_Vault/Audit_Logs.md
```

## 🔧 Configuration

### Gmail Watcher
Edit `watcher/gmail_watcher_enhanced.py`:
- `CHECK_INTERVAL`: How often to check for new emails (default: 60 seconds)
- `MAX_RESULTS`: Maximum emails to fetch per check (default: 10)

### Ralph Wiggum Loop
Edit `ralph_wiggum_loop.py`:
- `check_interval`: Autonomous cycle interval (default: 300 seconds)
- Enable/disable specific automated actions

### Cross-Domain Workflows
Edit `cross_domain_integration.py`:
```python
ENABLED_WORKFLOWS = {
    'email_to_customer': True,
    'email_to_invoice': True,
    'email_to_expense': False,  # Requires HR module
    'whatsapp_to_customer': True,
    'social_to_customer': True,
    'task_to_invoice': True,
}
```

### Audit Logging
Edit `audit_logger.py`:
- `max_bytes`: Log file size before rotation (default: 10MB)
- `backup_count`: Number of backup files to keep (default: 5)

## 📊 Agent Skills (23 Total)

### Email Skills (3)
- `ReadEmailsSkill` - Fetch and read emails from Gmail
- `ProcessEmailSkill` - Process email and create action files
- `GetEmailStatisticsSkill` - Get email statistics and metrics

### WhatsApp Skills (3)
- `ProcessWhatsAppChatSkill` - Process WhatsApp conversations
- `GetWhatsAppStatisticsSkill` - Get WhatsApp statistics
- `ListPendingWhatsAppChatsSkill` - List pending chats

### Twitter Skills (4)
- `GetTwitterMentionsSkill` - Fetch Twitter/X mentions
- `PostTweetSkill` - Post tweets
- `GetTwitterStatisticsSkill` - Get Twitter metrics
- `ProcessTwitterMentionSkill` - Process mentions and create actions

### Social Media Skills (4)
- `GetFacebookPostsSkill` - Fetch Facebook posts
- `PostToFacebookSkill` - Post to Facebook
- `GetInstagramMediaSkill` - Fetch Instagram media
- `GetSocialMediaStatisticsSkill` - Get social media metrics

### Odoo Skills (5)
- `GetOdooCustomersSkill` - Get customers from Odoo ERP
- `CreateOdooCustomerSkill` - Create new customer in Odoo
- `GetOdooInvoicesSkill` - Get invoices from Odoo
- `CreateOdooInvoiceSkill` - Create new invoice in Odoo
- `GetOdooProductsSkill` - Get products from Odoo

### Task Skills (5)
- `GetTaskStatisticsSkill` - Get task statistics
- `ListTasksSkill` - List all tasks
- `MoveTaskSkill` - Move task between folders
- `CreateTaskSkill` - Create new task
- `UpdateTaskSkill` - Update existing task

### Audit Skills (4)
- `GetAuditStatisticsSkill` - Get audit log statistics
- `GenerateCEOBriefingSkill` - Generate weekly CEO briefing
- `GenerateAuditSummarySkill` - Generate audit summary
- `QueryAuditLogsSkill` - Query audit logs with filters

**Usage:**
```bash
# List all available skills
python3 skills_cli.py --list

# Execute a skill
python3 skills_cli.py --skill <SkillName> --params '{"param": "value"}'
```

## 🔐 Security

- All data stored locally in Obsidian vault
- Credentials stored in separate files (not committed to git)
- API keys and tokens in `.gitignore`
- Audit logging for all operations
- Secure file permissions (chmod 600 for credentials)
- No external data storage except configured APIs
- Complete audit trail in JSONL format

**Credential Files:**
```
watcher/credentials/
  ├── credentials.json      # Gmail API
  └── token.json            # Gmail OAuth token

twitter_integration/credentials/
  └── twitter_credentials.json

social_media_integration/credentials/
  └── meta_credentials.json

odoo_integration/credentials/
  └── odoo_credentials.json
```

All credential files are in `.gitignore` and must be created from templates.

## 📝 System Workflows

### 1. Email Processing Workflow
1. **Gmail Watcher** monitors inbox every 60 seconds
2. **New Email Detected** → Downloads email content
3. **Action File Created** → Saved to `AI_Employee_Vault/Emails/`
4. **Audit Logged** → Event recorded in audit system
5. **Dashboard Updated** → Shows new email count

### 2. Cross-Domain Integration Workflow
1. **Email Arrives** with invoice request
2. **Email → Customer** workflow extracts sender info
3. **Customer Created/Found** in Odoo ERP
4. **Email → Invoice** workflow parses amount
5. **Invoice Created** in Odoo as draft
6. **Audit Logged** → Complete operation trail

### 3. Autonomous Agent Workflow (Ralph Wiggum Loop)
1. **System Health Check** → Monitors all components
2. **Task Analysis** → Scans for pending tasks
3. **Automated Actions** → Executes safe operations
4. **Report Generation** → Creates CEO briefing
5. **Audit Logging** → Records all activities
6. **Sleep** → Waits for next cycle (5 minutes)

### 4. Social Media Monitoring Workflow
1. **Twitter Monitor** checks mentions every 5 minutes
2. **Mention Detected** → Creates action file
3. **Facebook/Instagram** monitors posts and comments
4. **Action Files Created** → Saved to vault
5. **Statistics Updated** → Tracked in audit logs

### 5. Business Operations Workflow
1. **Customer Inquiry** arrives via email/WhatsApp/social
2. **Customer Auto-Created** in Odoo CRM
3. **Task Created** in Obsidian Kanban
4. **Follow-up Actions** scheduled
5. **Invoice Generated** when task completed
6. **Complete Audit Trail** maintained

## 🎓 Gold Tier Completion Checklist

### Bronze Tier ✅
- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] File system watcher (inbox monitoring)
- [x] Claude Code reading/writing to vault
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] AI functionality as Agent Skills

### Silver Tier ✅
- [x] Gmail watcher with OAuth authentication
- [x] WhatsApp integration and monitoring
- [x] Enhanced dashboard with statistics
- [x] Task management system
- [x] Automated email processing
- [x] Action file generation

### Gold Tier ✅ (All 11 Requirements Complete)
- [x] **Audit Logging System** - JSONL format with rotating files
- [x] **Agent Skills Framework** - 23 modular skills across 7 categories
- [x] **CEO Briefing Generator** - Weekly business reports
- [x] **Architecture Documentation** - Complete system diagrams
- [x] **Ralph Wiggum Loop** - Autonomous agent with continuous monitoring
- [x] **Twitter/X Integration** - API v2 with mention tracking
- [x] **Facebook & Instagram** - Meta Graph API integration
- [x] **Odoo 19 ERP** - Docker installation and JSON-RPC integration
- [x] **Odoo MCP Server** - 5 Odoo skills for business operations
- [x] **Cross-Domain Integration** - 6 workflows connecting Personal + Business
- [x] **Production Ready** - Complete testing and documentation

## 📚 Documentation

Comprehensive documentation available:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system architecture with diagrams
- **[CROSS_DOMAIN_INTEGRATION_DOCS.md](CROSS_DOMAIN_INTEGRATION_DOCS.md)** - Integration workflows
- **[ODOO_MCP_SERVER_DOCS.md](ODOO_MCP_SERVER_DOCS.md)** - Odoo integration guide
- **[ODOO_INSTALLATION_DOCS.md](ODOO_INSTALLATION_DOCS.md)** - Odoo setup instructions
- **[AGENT_SKILLS_DOCS.md](AGENT_SKILLS_DOCS.md)** - Skills framework documentation
- **[RALPH_WIGGUM_DOCS.md](RALPH_WIGGUM_DOCS.md)** - Autonomous agent guide
- **[AUDIT_LOGGING_DOCS.md](AUDIT_LOGGING_DOCS.md)** - Logging system documentation
- **[TWITTER_INTEGRATION_DOCS.md](TWITTER_INTEGRATION_DOCS.md)** - Twitter/X API guide
- **[FACEBOOK_INSTAGRAM_DOCS.md](FACEBOOK_INSTAGRAM_DOCS.md)** - Meta API guide
- **[ERROR_RECOVERY_DOCS.md](ERROR_RECOVERY_DOCS.md)** - Error handling patterns
- **[GMAIL_WATCHER_SETUP.md](GMAIL_WATCHER_SETUP.md)** - Gmail setup guide
- **[WHATSAPP_SETUP_GUIDE.md](WHATSAPP_SETUP_GUIDE.md)** - WhatsApp setup guide
- **[DASHBOARD_GUIDE.md](DASHBOARD_GUIDE.md)** - Dashboard customization
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[COMPLETE_SYSTEM_STATUS.md](COMPLETE_SYSTEM_STATUS.md)** - System status overview

## 🚀 Next Steps (Platinum Tier Ideas)

- Advanced AI decision-making with Claude API
- Multi-language support
- Mobile app integration
- Advanced analytics dashboard
- Machine learning for task prioritization
- Integration with more business tools (Salesforce, HubSpot, etc.)
- Voice assistant integration
- Advanced workflow automation builder
- Real-time collaboration features
- API for third-party integrations

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This project is production-ready and open for contributions!

**Areas for contribution:**
- Additional integrations (Slack, Telegram, etc.)
- Enhanced AI capabilities
- Performance optimizations
- Bug fixes and improvements
- Documentation enhancements
- Testing and quality assurance

**How to contribute:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- Built with Claude Code and Claude Sonnet 4.6
- Powered by Anthropic's Claude API
- Obsidian for knowledge management
- Odoo for ERP functionality
- Meta Graph API for social media
- Twitter API v2 for X integration

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the documentation files
- Review the audit logs for troubleshooting

## 🎯 Project Status

**Current Version:** Gold Tier Complete (v1.0.0)
**Status:** Production Ready
**Last Updated:** 2026-03-10

**System Capabilities:**
- ✅ 23 Agent Skills operational
- ✅ 6 Cross-domain workflows active
- ✅ 4 Social media integrations live
- ✅ Full Odoo ERP integration
- ✅ Autonomous agent running
- ✅ Complete audit logging
- ✅ Weekly CEO briefings
- ✅ Beautiful Obsidian dashboard

**Deployment:** Local-first with cloud API integrations

---

**Made with ❤️ using Claude Code**
