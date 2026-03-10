# Gmail Watcher Setup Guide (Urdu/English)

## 📧 Gmail Se Emails Receive Karne Ka Setup

### Step 1: Google Cloud Console Setup

1. **Google Cloud Console pe jao:**
   - URL: https://console.cloud.google.com/

2. **New Project banao:**
   - Click "Select a project" → "New Project"
   - Project name: "Personal AI Employee"
   - Click "Create"

3. **Gmail API enable karo:**
   - Left menu → "APIs & Services" → "Library"
   - Search: "Gmail API"
   - Click "Gmail API" → Click "Enable"

### Step 2: OAuth Credentials Create Karo

1. **OAuth Consent Screen configure karo:**
   - Go to: "APIs & Services" → "OAuth consent screen"
   - User Type: Select "External"
   - Click "Create"

   **App Information:**
   - App name: "Personal AI Employee"
   - User support email: ghazalshaikh09@gmail.com
   - Developer contact: ghazalshaikh09@gmail.com
   - Click "Save and Continue"

   **Scopes:**
   - Click "Add or Remove Scopes"
   - Search: "Gmail API"
   - Select: ".../auth/gmail.readonly" (Read-only access)
   - Click "Update" → "Save and Continue"

   **Test Users:**
   - Click "Add Users"
   - Add: ghazalshaikh09@gmail.com
   - Click "Save and Continue"

2. **OAuth Client ID create karo:**
   - Go to: "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Personal AI Employee Gmail Watcher"
   - Click "Create"

3. **Credentials download karo:**
   - Download icon (⬇️) click karo
   - File save hogi: `client_secret_XXXXX.json`
   - Rename karo: `gmail_credentials.json`

### Step 3: Credentials File Setup

```bash
# Terminal mein run karo:
cd "/Users/user/Documents/GitHub/Personal AI Employee"

# Credentials folder banao
mkdir -p watcher/credentials

# Downloaded file ko move karo
# (Downloads folder se copy karo gmail_credentials.json)
mv ~/Downloads/gmail_credentials.json watcher/credentials/

# Verify
ls -la watcher/credentials/
```

### Step 4: Python Dependencies Install Karo

```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee/watcher"

# Install Gmail API libraries
pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 5: First Run (Authentication)

```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee/watcher"

# Gmail Watcher start karo
python3 gmail_watcher.py
```

**Kya hoga:**
1. Browser automatically khulega
2. Google sign-in page aayega
3. ghazalshaikh09@gmail.com se login karo
4. "Personal AI Employee wants to access your Gmail" → Click "Allow"
5. Browser mein "Authentication successful" dikhega
6. Terminal mein "Successfully authenticated with Gmail" dikhega
7. Token save ho jayega (`gmail_token.pickle`)

### Step 6: Test Karo

1. **Apne aap ko important email bhejo:**
   - Gmail kholo
   - Compose new email
   - To: ghazalshaikh09@gmail.com
   - Subject: "Test Important Email"
   - Body: "This is a test for my AI Employee"
   - Send karo
   - Email ko "Star" (⭐) karo (important mark karne ke liye)

2. **Wait karo 2 minutes**
   - Watcher har 2 minute mein check karta hai

3. **Check karo action file bani ya nahi:**
   ```bash
   ls -la "AI_Employee_Vault/Needs_Action/"
   ```

### Step 7: Background Mein Run Karo (Optional)

**Option A: Terminal mein background**
```bash
cd "/Users/user/Documents/GitHub/Personal AI Employee/watcher"
nohup python3 gmail_watcher.py > ../logs/gmail-watcher.log 2>&1 &

# Process ID check karo
ps aux | grep gmail_watcher
```

**Option B: Cron job (automatic startup)**
```bash
# Crontab edit karo
crontab -e

# Yeh line add karo (har 2 minute mein run hoga):
*/2 * * * * cd "/Users/user/Documents/GitHub/Personal AI Employee/watcher" && python3 gmail_watcher.py >> ../logs/gmail-watcher.log 2>&1
```

**Stop karne ke liye:**
```bash
# Process find karo
ps aux | grep gmail_watcher

# Kill karo (PID replace karo)
kill <PID>
```

---

## 🔐 Security Notes

### Files (NEVER commit to git!)
- `watcher/credentials/gmail_credentials.json` - OAuth client secret
- `watcher/credentials/gmail_token.pickle` - Access token

### Permissions
- **Read-only access** to Gmail
- Cannot send, delete, or modify emails
- Only reads unread + important messages

### Revoke Access (Agar zaroorat ho)
1. Go to: https://myaccount.google.com/permissions
2. Find "Personal AI Employee"
3. Click "Remove Access"

---

## ⚙️ Configuration

### Check Interval Change Karo
Edit `watcher/gmail_watcher.py`:
```python
CHECK_INTERVAL = 120  # 120 seconds = 2 minutes
# Change to 60 for 1 minute, 300 for 5 minutes, etc.
```

### Filter Change Karo
Edit `watcher/gmail_watcher.py`:
```python
# Current: unread + important
q='is:unread is:important'

# Options:
q='is:unread from:client@example.com'  # Specific sender
q='is:unread subject:urgent'           # Specific subject
q='is:unread label:work'               # Specific label
```

---

## 🐛 Troubleshooting

### Error: "Credentials file not found"
```bash
# Check file exists
ls -la watcher/credentials/gmail_credentials.json

# If not, download again from Google Cloud Console
```

### Error: "Authentication failed"
```bash
# Delete token and re-authenticate
rm watcher/credentials/gmail_token.pickle
python3 watcher/gmail_watcher.py
```

### No emails detected
**Check:**
1. Email ko star (⭐) kiya hai? (Important mark)
2. Email unread hai?
3. Watcher running hai?
   ```bash
   ps aux | grep gmail_watcher
   ```
4. Logs check karo:
   ```bash
   tail -f logs/gmail-watcher.log
   ```

---

## ✅ Verification Checklist

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth credentials downloaded
- [ ] Credentials file in `watcher/credentials/`
- [ ] Python dependencies installed
- [ ] First authentication completed
- [ ] Token file created (`gmail_token.pickle`)
- [ ] Test email sent and detected
- [ ] Action file created in `Needs_Action/`

---

**Next:** Dashboard setup and monitoring
