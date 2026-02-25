# MCP Server Configuration for Claude Code

## What is MCP?

Model Context Protocol (MCP) allows Claude Code to interact with external tools and services. This email MCP server enables Claude to send emails directly.

## Configuration Steps

### Step 1: Make the server executable

```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee/mcp_server"
chmod +x email_server.py
```

### Step 2: Test the server

```bash
python3 test_server.py
```

You should see:
```
🧪 Testing Email MCP Server...
✅ Initialize: PASSED
✅ List tools: PASSED
✅ Send email: PASSED
🎉 All tests passed!
```

### Step 3: Configure Claude Code

Add this to your Claude Code settings file:

**Location:** `~/.config/claude/settings.json`

```json
{
  "mcpServers": {
    "email": {
      "command": "python3",
      "args": [
        "/Users/user/Documents/GitHub/Personal AI Employee/mcp_server/email_server.py"
      ],
      "env": {}
    }
  }
}
```

### Step 4: Restart Claude Code

```bash
# Exit current Claude Code session
# Then start a new session
claude code
```

### Step 5: Verify MCP server is loaded

In Claude Code, ask:
```
"Can you send a test email to test@example.com?"
```

Claude should now be able to use the email MCP server!

## Usage Examples

### Send a simple email:
```
"Send an email to john@example.com with subject 'Meeting Tomorrow' and body 'Let's meet at 10 AM'"
```

### Send notification email:
```
"Send me an email notification about the completed tasks"
```

### Send report via email:
```
"Generate a daily briefing and email it to ceo@company.com"
```

## Production Configuration

For production use with real SMTP:

1. Edit `email_server.py`
2. Add SMTP configuration:

```python
# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"

# In send_email method:
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SMTP_USERNAME, SMTP_PASSWORD)
server.send_message(msg)
server.quit()
```

3. For Gmail, create an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

## Troubleshooting

### Server not starting:
```bash
# Check Python version (needs 3.8+)
python3 --version

# Test server manually
python3 email_server.py
# Then type: {"jsonrpc":"2.0","id":1,"method":"initialize"}
```

### Claude Code not finding server:
- Check settings.json path is correct
- Verify absolute path to email_server.py
- Restart Claude Code completely

### Permission denied:
```bash
chmod +x email_server.py
```

## Security Notes

- Demo mode logs emails instead of sending
- For production, use environment variables for credentials
- Never commit SMTP passwords to git
- Use app-specific passwords, not main account passwords

## What This Achieves

✅ **Silver Tier Requirement #5:** One working MCP server
✅ **100% Silver Tier Completion**
✅ Claude Code can now send emails
✅ Enables automated notifications and reports

---

**Status:** Ready to use (demo mode)
**Production:** Requires SMTP configuration
**Time to setup:** 5 minutes
