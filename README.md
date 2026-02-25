# Personal AI Employee - Bronze Tier

A local-first, autonomous AI assistant that manages personal and business affairs using Claude Code and Obsidian.

## 🎯 Bronze Tier Features

- ✅ Obsidian vault with Dashboard and Company Handbook
- ✅ File system watcher for inbox monitoring
- ✅ Claude Code Agent Skills for vault interaction
- ✅ Basic folder structure (Inbox, Needs_Action, Done)
- ✅ Automated processing workflow

## 📁 Project Structure

```
Personal AI Employee/
├── AI_Employee_Vault/           # Main vault directory
│   ├── Dashboard.md          # Status overview and quick links
│   ├── Company_Handbook.md   # Policies and procedures
│   ├── Inbox/                # New items arrive here
│   ├── Needs_Action/         # Items requiring follow-up
│   └── Done/                 # Completed items
├── watcher/                  # File system monitoring
│   └── inbox_watcher.py      # Monitors Inbox for new files
└── .claude/
    └── skills/               # Agent Skills
        ├── vault-status.json
        ├── process-inbox.json
        └── update-dashboard.json
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10+
- UV package manager
- Claude Code CLI
- Obsidian (optional, for viewing vault)

### Installation

1. **Clone the repository**
   ```bash
   cd "Personal AI Employee"
   ```

2. **Verify Claude Code is installed**
   ```bash
   claude --version
   ```

3. **Install Python dependencies**
   ```bash
   cd watcher
   uv sync
   ```

### Running the System

1. **Start the Inbox Watcher**
   ```bash
   cd watcher
   python inbox_watcher.py
   ```

2. **Use Agent Skills with Claude Code**
   ```bash
   # Check vault status
   claude code /vault-status

   # Process an inbox item
   claude code /process-inbox path/to/file.md

   # Update dashboard
   claude code /update-dashboard
   ```

3. **Add items to process**
   - Drop files into `AI_Employee_Vault/Inbox/`
   - The watcher will detect them and trigger processing
   - Or manually invoke `/process-inbox`

## 🎮 Usage Examples

### Check System Status
```bash
claude code /vault-status
```

### Process a New Request
1. Create a file in `AI_Employee_Vault/Inbox/client-request.md`
2. The watcher detects it automatically
3. Claude processes and categorizes it
4. Dashboard updates with new activity

### Manual Processing
```bash
claude code /process-inbox AI_Employee_Vault/Inbox/invoice-request.md
```

## 🔧 Configuration

Edit `watcher/inbox_watcher.py` to customize:
- `CHECK_INTERVAL`: How often to check for new files (default: 30 seconds)
- `INBOX_PATH`: Location of the inbox folder

Edit `AI_Employee_Vault/Company_Handbook.md` to customize:
- Processing rules
- Automation policies
- Response templates

## 📊 Agent Skills

### `/vault-status`
Generates a comprehensive status report showing:
- File counts in each folder
- Recent activity
- Urgent items requiring attention

### `/process-inbox`
Processes new inbox items by:
- Analyzing content
- Extracting key information
- Creating action items
- Moving files to appropriate folders
- Updating the dashboard

### `/update-dashboard`
Refreshes the dashboard with:
- Current file counts
- Recent activity log
- Alerts and notifications

## 🔐 Security

- All data stored locally in the vault
- No external API calls for data storage
- Credentials should be stored in environment variables
- Audit trail maintained in `/Done` folder

## 📝 Workflow

1. **New Item Arrives** → Lands in `/Inbox`
2. **Watcher Detects** → Triggers Claude Code
3. **AI Analyzes** → Extracts information and categorizes
4. **Action Created** → Moves to `/Needs_Action` or `/Done`
5. **Dashboard Updates** → Shows current status

## 🎓 Bronze Tier Completion Checklist

- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] One working Watcher script (file system monitoring)
- [x] Claude Code reading from and writing to the vault
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] All AI functionality implemented as Agent Skills

## 🚧 Next Steps (Silver Tier)

- Add Gmail watcher
- Implement LinkedIn auto-posting
- Create Plan.md generation
- Add MCP server for email sending
- Human-in-the-loop approval workflow

## 📄 License

MIT

## 🤝 Contributing

This is a hackathon project. Feel free to fork and extend!
