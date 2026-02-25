# Gmail Watcher Setup Guide

## 📧 Setting Up Gmail Integration

This guide walks you through setting up the Gmail Watcher for the Personal AI Employee.

---

## 🔧 Prerequisites

- Google account with Gmail
- Python 3.10+
- Internet connection

---

## 📝 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Create New Project:**
   - Click "Select a project" → "New Project"
   - Name: "Personal AI Employee"
   - Click "Create"

3. **Enable Gmail API:**
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"

### Step 2: Create OAuth Credentials

1. **Configure OAuth Consent Screen:**
   - Go to "APIs & Services" → "OAuth consent screen"
   - User Type: "External"
   - App name: "Personal AI Employee"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Scopes: Skip for now
   - Test users: Add your email
   - Click "Save and Continue"

2. **Create Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Personal AI Employee Gmail"
   - Click "Create"

3. **Download Credentials:**
   - Click the download icon next to your credential
   - Save as `gmail_credentials.json`
   - Move to: `watcher/credentials/gmail_credentials.json`

### Step 3: Install Dependencies

```bash
cd watcher
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 4: First Run (Authentication)

```bash
python3 gmail_watcher.py
```

**What happens:**
1. Browser opens automatically
2. Sign in with your Google account
3. Grant permissions to the app
4. Browser shows "Authentication successful"
5. Token saved for future use

### Step 5: Verify Setup

The watcher should now be running and monitoring your Gmail inbox.

**Test it:**
1. Send yourself an important email
2. Mark it as important (star it)
3. Wait 2 minutes
4. Check `AI_Employee_Vault/Needs_Action/` for new file

---

## 🔐 Security Notes

### What Gets Stored:

**`gmail_credentials.json`** (Never commit to git!)
- Client ID and secret
- Used for OAuth authentication

**`gmail_token.pickle`** (Never commit to git!)
- Access token and refresh token
- Allows watcher to access Gmail without re-authentication

### Permissions Granted:

- **Read-only access** to Gmail
- Cannot send, delete, or modify emails
- Only reads unread important messages

### Best Practices:

1. **Add to .gitignore:**
   ```
   watcher/credentials/
   ```

2. **Rotate credentials regularly:**
   - Delete `gmail_token.pickle`
   - Re-authenticate

3. **Revoke access if needed:**
   - Go to: https://myaccount.google.com/permissions
   - Find "Personal AI Employee"
   - Click "Remove Access"

---

## ⚙️ Configuration

### Adjust Check Interval:

Edit `gmail_watcher.py`:
```python
CHECK_INTERVAL = 120  # Change to desired seconds
```

### Change Query Filter:

Edit `gmail_watcher.py`:
```python
# Current: unread + important
q='is:unread is:important'

# Options:
q='is:unread from:client@example.com'  # Specific sender
q='is:unread subject:invoice'          # Specific subject
q='is:unread label:urgent'             # Specific label
```

### Adjust Max Results:

```python
maxResults=10  # Change to desired number
```

---

## 🚀 Running the Watcher

### Manual Start:
```bash
cd watcher
python3 gmail_watcher.py
```

### Background (macOS/Linux):
```bash
nohup python3 gmail_watcher.py > ../logs/gmail-watcher.log 2>&1 &
```

### Cron Job (Automated):
```bash
# Add to crontab
*/2 * * * * cd /path/to/Personal\ AI\ Employee && python3 watcher/gmail_watcher.py >> logs/gmail-watcher.log 2>&1
```

### Stop Watcher:
```bash
# Find process
ps aux | grep gmail_watcher

# Kill process
kill <PID>
```

---

## 🐛 Troubleshooting

### Error: "Credentials file not found"

**Solution:**
- Verify `gmail_credentials.json` is in `watcher/credentials/`
- Check file permissions

### Error: "Authentication failed"

**Solution:**
1. Delete `gmail_token.pickle`
2. Run watcher again
3. Re-authenticate in browser

### Error: "Gmail API not enabled"

**Solution:**
- Go to Google Cloud Console
- Enable Gmail API for your project

### No emails detected:

**Check:**
1. Are emails marked as important?
2. Are emails unread?
3. Is check interval too long?
4. Check watcher logs

### Rate limiting:

**Gmail API Limits:**
- 250 quota units per user per second
- 1 billion quota units per day

**If exceeded:**
- Increase CHECK_INTERVAL
- Reduce maxResults
- Wait for quota reset

---

## 📊 Monitoring

### View Logs:
```bash
tail -f logs/gmail-watcher.log
```

### Check Status:
```bash
ps aux | grep gmail_watcher
```

### Test Connection:
```bash
python3 -c "from gmail_watcher import get_gmail_service; print('OK' if get_gmail_service() else 'FAIL')"
```

---

## ✅ Verification Checklist

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth credentials downloaded
- [ ] Credentials file in correct location
- [ ] Dependencies installed
- [ ] First authentication completed
- [ ] Token file created
- [ ] Watcher running successfully
- [ ] Test email detected
- [ ] Action file created

---

## 🎯 Silver Tier Compliance

**Requirement:** Two or more Watcher scripts

**Status:** ✅ Gmail Watcher Ready

**Next:** Set up WhatsApp Watcher or LinkedIn integration

---

**Last Updated:** 2026-02-25
**Status:** Ready for use (credentials required)
**Estimated Setup Time:** 15-20 minutes
