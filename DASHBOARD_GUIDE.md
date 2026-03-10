# AI Employee Dashboard Guide

## 📊 Dashboard Kaise Use Karein

### Option 1: Obsidian (Best Experience)

**Install Obsidian:**
1. Download: https://obsidian.md/download
2. Install karo
3. Open karo

**Vault Setup:**
1. Obsidian kholo
2. "Open folder as vault" click karo
3. Select karo: `/Users/user/Documents/GitHub/Personal AI Employee/AI_Employee_Vault`
4. Vault khul jayega

**Dashboard View:**
- Left sidebar mein `Dashboard.md` dikhega
- Click karo to open
- Real-time status dekhega:
  - Inbox items count
  - Needs Action items
  - Recent activity
  - Alerts

**Navigation:**
- Click on folder names to browse
- `[[Inbox/]]` - New items
- `[[Needs_Action/]]` - Pending tasks
- `[[Done/]]` - Completed items

---

### Option 2: VS Code (Alternative)

```bash
# VS Code se open karo
code "/Users/user/Documents/GitHub/Personal AI Employee/AI_Employee_Vault"
```

**Features:**
- Markdown preview (Cmd+Shift+V)
- File explorer
- Search across files

---

### Option 3: Terminal (Quick Check)

```bash
# Dashboard dekho
cat "/Users/user/Documents/GitHub/Personal AI Employee/AI_Employee_Vault/Dashboard.md"

# Inbox items count
ls -1 "/Users/user/Documents/GitHub/Personal AI Employee/AI_Employee_Vault/Inbox" | wc -l

# Needs Action items
ls -1 "/Users/user/Documents/GitHub/Personal AI Employee/AI_Employee_Vault/Needs_Action" | wc -l

# Recent activity
ls -lt "/Users/user/Documents/GitHub/Personal AI Employee/AI_Employee_Vault/Needs_Action" | head -5
```

---

## 🔄 Complete Workflow

### **Email Receive → Dashboard → Action**

```
1. Important Email Aata Hai
   ↓
2. Gmail Watcher Detect Karta Hai (har 2 min)
   ↓
3. Action File Banata Hai
   Location: AI_Employee_Vault/Needs_Action/EMAIL-xxxxx.md
   ↓
4. Dashboard Update Hota Hai
   ↓
5. Aap Obsidian/VS Code Mein Dekhte Ho
   ↓
6. Action Lete Ho (reply, task create, etc.)
   ↓
7. File Move Karte Ho Done/ Folder Mein
```

---

## 🎮 Claude Code Skills (Automation)

### **Available Skills:**

**1. Check Vault Status**
```bash
claude code
# Then type:
/vault-status
```
Shows:
- File counts in each folder
- Recent activity
- Urgent items

**2. Process Inbox Item**
```bash
claude code
# Then type:
/process-inbox AI_Employee_Vault/Inbox/some-file.md
```
AI will:
- Analyze content
- Extract key info
- Create action items
- Move to appropriate folder
- Update dashboard

**3. Update Dashboard**
```bash
claude code
# Then type:
/update-dashboard
```
Refreshes:
- Current file counts
- Recent activity log
- Alerts and notifications

---

## 📧 Email Workflow Examples

### **Example 1: Client Email Aaya**

**Gmail Watcher detects:**
```
From: client@example.com
Subject: Urgent: Project Deadline
Body: We need the report by Friday...
```

**Action file creates:**
```markdown
# Email: Urgent: Project Deadline

**From:** client@example.com
**Priority:** Important

## Suggested Actions
- [ ] Read and analyze email
- [ ] Draft response
- [ ] Create project task
- [ ] Reply to sender
```

**Aap kya karte ho:**
1. Obsidian mein file kholo
2. Email padho
3. Response draft karo
4. Claude Code se email bhejo:
   ```
   Send email to client@example.com with subject "Re: Project Deadline"
   and body "Thank you for your email. I will have the report ready by Friday."
   ```
5. File ko Done/ folder mein move karo

---

### **Example 2: Invoice Request**

**Email:**
```
Subject: Invoice Request - $5000
Body: Please send invoice for December services
```

**Action file:**
```markdown
# Email: Invoice Request - $5000

## Suggested Actions
- [ ] Create invoice
- [ ] Send to client
- [ ] Update accounting
```

**Aap kya karte ho:**
1. Invoice create karo
2. Email bhejo with attachment
3. Mark as done

---

## 🔍 Monitoring Commands

### **Check System Status**

```bash
# Gmail Watcher running hai?
ps aux | grep gmail_watcher

# Recent emails detected
ls -lt "AI_Employee_Vault/Needs_Action" | grep EMAIL | head -5

# Dashboard last update
stat -f "%Sm" "AI_Employee_Vault/Dashboard.md"

# Logs check karo
tail -f logs/gmail-watcher.log
```

### **Quick Stats**

```bash
# Total pending items
find "AI_Employee_Vault/Needs_Action" -type f | wc -l

# Completed today
find "AI_Employee_Vault/Done" -type f -mtime -1 | wc -l

# Inbox items
find "AI_Employee_Vault/Inbox" -type f | wc -l
```

---

## 🚀 Daily Workflow

### **Morning Routine:**

1. **Start Gmail Watcher** (agar background mein nahi hai)
   ```bash
   cd "/Users/user/Documents/GitHub/Personal AI Employee/watcher"
   python3 gmail_watcher.py &
   ```

2. **Open Dashboard**
   - Obsidian kholo
   - Dashboard.md dekho
   - Priorities check karo

3. **Check Needs_Action Folder**
   - New emails dekho
   - Urgent items identify karo
   - Actions plan karo

### **Throughout Day:**

1. **Monitor Alerts**
   - Dashboard refresh karo
   - New items check karo

2. **Process Items**
   - Emails reply karo (Claude Code se)
   - Tasks complete karo
   - Files Done/ mein move karo

3. **Update Dashboard**
   ```bash
   claude code
   /update-dashboard
   ```

### **Evening Routine:**

1. **Review Completed Items**
   ```bash
   ls -lt "AI_Employee_Vault/Done" | head -10
   ```

2. **Plan Tomorrow**
   - Pending items dekho
   - Priorities set karo

3. **Stop Watcher** (optional)
   ```bash
   pkill -f gmail_watcher
   ```

---

## 🎯 Pro Tips

### **Tip 1: Custom Filters**
Edit `watcher/gmail_watcher.py` to filter specific senders:
```python
q='is:unread from:important-client@example.com'
```

### **Tip 2: Email Templates**
Create templates in `AI_Employee_Vault/Templates/`:
```markdown
# Client Response Template

Dear [Client Name],

Thank you for your email regarding [Topic].

[Your response here]

Best regards,
Ghazal Shaikh
```

### **Tip 3: Automation with Claude Code**
```bash
# Batch process inbox
claude code
"Process all items in Inbox folder and categorize them"
```

### **Tip 4: Quick Email Send**
```bash
# From terminal
source ~/.ai_employee_email_config
python3 -c "
import smtplib, os
from email.mime.text import MIMEText
msg = MIMEText('Quick message')
msg['Subject'] = 'Quick Update'
msg['From'] = os.environ['EMAIL_ADDRESS']
msg['To'] = 'recipient@example.com'
s = smtplib.SMTP(os.environ['SMTP_SERVER'], int(os.environ['SMTP_PORT']))
s.starttls()
s.login(os.environ['EMAIL_ADDRESS'], os.environ['EMAIL_PASSWORD'])
s.send_message(msg)
s.quit()
print('Sent!')
"
```

---

## 📱 Mobile Access (Future)

**Option 1: Obsidian Mobile**
- Install Obsidian app on phone
- Sync vault via iCloud/Dropbox
- View dashboard on the go

**Option 2: Git Sync**
- Commit vault changes to git
- Pull on mobile device
- View in any markdown app

---

## 🔧 Troubleshooting

### Dashboard Not Updating?
```bash
# Manually update
claude code
/update-dashboard
```

### Gmail Watcher Not Detecting Emails?
```bash
# Check logs
tail -f logs/gmail-watcher.log

# Restart watcher
pkill -f gmail_watcher
cd watcher && python3 gmail_watcher.py &
```

### Obsidian Not Opening Vault?
1. Obsidian → Settings → About → Reload
2. Or manually open folder as vault

---

## ✅ Success Checklist

- [ ] Obsidian installed and vault opened
- [ ] Dashboard visible and readable
- [ ] Gmail Watcher running in background
- [ ] Test email sent and detected
- [ ] Action file created in Needs_Action/
- [ ] Claude Code skills working (/vault-status)
- [ ] Email sending working
- [ ] Workflow understood

---

**Aapka AI Employee ab fully functional hai! 🎉**

**Next Steps:**
1. Gmail Watcher setup complete karo (GMAIL_WATCHER_SETUP.md follow karo)
2. Obsidian install karo
3. Test email bhejo aur dekho action file banti hai ya nahi
4. Daily workflow start karo

**Questions? Claude Code se poochho:**
```bash
claude code
"How do I [your question]?"
```
