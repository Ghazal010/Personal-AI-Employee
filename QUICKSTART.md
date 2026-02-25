# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Verify Installation

```bash
# Check all prerequisites
python3 test_bronze.py
```

You should see all tests passing ✅

### Step 2: Create Sample Data

```bash
# Generate sample inbox items
python3 create_samples.py
```

This creates 3 sample items in the Inbox folder.

### Step 3: Process Items Manually

Open Claude Code and process the inbox:

```bash
claude code
```

Then say: "Process all items in the inbox"

### Step 4: Start Automatic Monitoring

```bash
# Start the watcher (runs continuously)
./start.sh
```

Now any file you drop into `AI_Employee_Vault/Inbox/` will be automatically processed!

### Step 5: View Results

Check the results:

```bash
# View the dashboard
cat AI_Employee_Vault/Dashboard.md

# See action items
ls AI_Employee_Vault/Needs_Action/

# See completed items
ls AI_Employee_Vault/Done/
```

## 📖 Common Tasks

### Add a New Inbox Item

```bash
# Create a new file
cat > AI_Employee_Vault/Inbox/my-task.md << 'EOF'
# My Task

This is something I need to do.

**Priority:** High
**Deadline:** Tomorrow
EOF
```

The watcher will detect it within 30 seconds.

### Check System Status

```bash
# Run the test suite
python3 test_bronze.py
```

### Stop the Watcher

Press `Ctrl+C` in the terminal running `start.sh`

## 🎯 What Gets Processed?

The AI analyzes each inbox item and:

1. **Extracts key information** (dates, amounts, contacts, deadlines)
2. **Categorizes by priority** (Urgent, Important, Low)
3. **Creates action items** in Needs_Action folder
4. **Updates the dashboard** with current status
5. **Archives processed items** in Done folder
6. **Flags items requiring approval** (per Company Handbook policies)

## 🔧 Customization

### Change Watcher Interval

Edit `watcher/inbox_watcher.py`:

```python
CHECK_INTERVAL = 30  # Change to desired seconds
```

### Modify Processing Rules

Edit `AI_Employee_Vault/Company_Handbook.md` to customize:
- Priority thresholds
- Approval requirements
- Response templates
- Automation policies

### Add Custom Skills

Create new skills in `.claude/skills/`:

```json
{
  "name": "my-skill",
  "description": "What this skill does",
  "instructions": "Detailed instructions for Claude..."
}
```

## 🐛 Troubleshooting

### Watcher Not Detecting Files

- Check file permissions on Inbox folder
- Verify watcher is running (`ps aux | grep inbox_watcher`)
- Check watcher logs for errors

### Claude Code Not Processing

- Verify Claude Code is installed: `claude --version`
- Check API key is configured
- Ensure you're in the correct directory

### Files Not Moving

- Check folder permissions
- Verify paths in watcher script
- Look for error messages in watcher output

## 📚 Next Steps

Once Bronze Tier is working:

1. **Silver Tier:** Add Gmail/WhatsApp watchers
2. **Gold Tier:** Implement full autonomy with MCP servers
3. **Customize:** Adapt to your specific workflows

## 💡 Tips

- Keep inbox items in Markdown format for best results
- Include priority and deadline information
- Use clear, descriptive filenames
- Review Company_Handbook.md to understand automation policies
- Check Dashboard.md regularly for status updates

---

**Need help?** Check the main README.md or the hackathon documentation.
