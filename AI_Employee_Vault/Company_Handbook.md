# Company Handbook

## 📋 About

This handbook contains the operational guidelines, policies, and procedures for the Personal AI Employee system.

## 🎯 Mission

To autonomously manage personal and business affairs with minimal human intervention while maintaining transparency and control.

## 🔧 System Configuration

### Watcher Settings
- **File System Monitor:** Enabled
- **Check Interval:** 30 seconds
- **Monitored Directories:** Inbox/

### Processing Rules

#### Email Classification
- **Urgent:** Requires immediate attention (invoices, client requests)
- **Important:** Should be handled within 24 hours
- **Low Priority:** Can be batched and processed weekly

#### Task Prioritization
1. Client-facing requests
2. Financial transactions
3. Administrative tasks
4. General inquiries

### Automation Policies

#### Requires Human Approval
- Financial transactions > $100
- Client communications
- Social media posts
- Contract modifications

#### Can Auto-Execute
- File organization
- Data entry
- Report generation
- Status updates

## 📝 Standard Operating Procedures

### Inbox Processing
1. New items arrive in `/Inbox`
2. AI analyzes and categorizes
3. Creates action items in `/Needs_Action`
4. Executes or requests approval
5. Moves completed items to `/Done`

### Daily Routine
- **Morning:** Review overnight activity, generate briefing
- **Midday:** Process accumulated inbox items
- **Evening:** Summarize day's activities, prepare next day's priorities

## 🔐 Security Guidelines

- Never store credentials in plain text
- Use environment variables for sensitive data
- Log all automated actions
- Maintain audit trail in `/Done`

## 📞 Contact Protocols

### Response Templates
- Client inquiry: Professional, prompt (< 2 hours)
- Internal: Casual, informative
- Urgent: Immediate notification to human

---

*Last updated: {{date}}*
