# Facebook & Instagram Integration - Documentation

**Version:** 1.0.0
**Last Updated:** 2026-03-10
**Status:** Ready for Configuration

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Guide](#setup-guide)
4. [Features](#features)
5. [Usage](#usage)
6. [Agent Skills](#agent-skills)
7. [Configuration](#configuration)
8. [Monitoring](#monitoring)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Facebook & Instagram Integration enables the Personal AI Employee to monitor and interact with Facebook Pages and Instagram Business accounts through the Meta Graph API.

### Key Features

- **Facebook Page Monitoring** - Track posts, comments, and engagement
- **Instagram Business Monitoring** - Monitor media posts and comments
- **Post Creation** - Publish to Facebook programmatically
- **Action File Creation** - Convert social media content to Obsidian action files
- **Agent Skills** - 4 social media skills for programmatic access
- **Audit Logging** - All social media actions logged to audit system
- **Unified Interface** - Single integration for both platforms

---

## Prerequisites

### 1. Facebook Developer Account

You need a Facebook Developer Account to access the Meta Graph API.

**Steps:**
1. Go to https://developers.facebook.com/
2. Sign in with your Facebook account
3. Create a Developer Account
4. Verify your account (email/phone)

### 2. Facebook Page

You need a Facebook Page (not personal profile) to use the API.

**Create a Page:**
1. Go to https://www.facebook.com/pages/create
2. Choose page type (Business, Community, etc.)
3. Fill in page details
4. Publish your page

### 3. Instagram Business Account (Optional)

For Instagram integration, you need an Instagram Business or Creator account linked to your Facebook Page.

**Convert to Business Account:**
1. Open Instagram app
2. Go to Settings → Account
3. Switch to Professional Account
4. Choose Business or Creator
5. Link to your Facebook Page

### 4. Python Dependencies

Install the required library:

```bash
pip3 install facebook-sdk
```

**facebook-sdk** is the Python library for Meta Graph API.

### 5. API Access Token

You'll need a Page Access Token with appropriate permissions.

---

## Setup Guide

### Step 1: Create Facebook App

1. **Go to Facebook Developers**
   - Visit https://developers.facebook.com/apps/
   - Click "Create App"

2. **Choose App Type**
   - Select "Business" or "Consumer"
   - Fill in app details
   - Create app

3. **Add Products**
   - Add "Facebook Login"
   - Add "Instagram Basic Display" (for Instagram)

4. **Configure Settings**
   - Set App Domains
   - Add Privacy Policy URL
   - Add Terms of Service URL

### Step 2: Get Page Access Token

1. **Use Graph API Explorer**
   - Go to https://developers.facebook.com/tools/explorer/
   - Select your app
   - Select your page

2. **Request Permissions**
   - pages_show_list
   - pages_read_engagement
   - pages_manage_posts
   - instagram_basic (for Instagram)
   - instagram_manage_comments (for Instagram)

3. **Generate Token**
   - Click "Generate Access Token"
   - Authorize permissions
   - Copy the token

4. **Get Long-Lived Token**
   ```bash
   curl -i -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
   ```

### Step 3: Get Page ID and Instagram Account ID

**Get Page ID:**
```bash
curl -i -X GET "https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_ACCESS_TOKEN"
```

**Get Instagram Account ID:**
```bash
curl -i -X GET "https://graph.facebook.com/v18.0/YOUR_PAGE_ID?fields=instagram_business_account&access_token=YOUR_ACCESS_TOKEN"
```

### Step 4: Configure Credentials

1. **Copy the template:**
   ```bash
   cd social_media_integration/credentials/
   cp meta_credentials.json.template meta_credentials.json
   ```

2. **Edit the credentials file:**
   ```bash
   nano meta_credentials.json
   ```

3. **Add your credentials:**
   ```json
   {
     "access_token": "your_long_lived_page_access_token",
     "facebook_page_id": "your_facebook_page_id",
     "instagram_account_id": "your_instagram_business_account_id"
   }
   ```

4. **Secure the file:**
   ```bash
   chmod 600 meta_credentials.json
   ```

### Step 5: Test Authentication

```bash
cd social_media_integration
python3 -c "
from facebook_instagram_monitor import MetaIntegration
meta = MetaIntegration()
if meta.authenticate():
    print('✅ Authentication successful!')
else:
    print('❌ Authentication failed')
"
```

### Step 6: Start Monitoring (Optional)

```bash
# Foreground (for testing)
python3 facebook_instagram_monitor.py

# Background (for production)
nohup python3 facebook_instagram_monitor.py > ../logs/social-media-monitor.log 2>&1 &
```

---

## Features

### 1. Facebook Page Monitoring

**Automatic Detection:**
- Checks for new posts every 5 minutes
- Creates action files in `AI_Employee_Vault/Facebook/`
- Logs all posts to audit system

**Action File Format:**
```markdown
# Facebook Post

**Date:** 2026-03-10 20:30:00
**Post ID:** 123456789_987654321
**Type:** Facebook Post

## Post Content

This is a Facebook post!

**Link:** https://facebook.com/...

## Suggested Actions

- [ ] Read and analyze post
- [ ] Check engagement
- [ ] Respond to comments
```

### 2. Instagram Business Monitoring

**Automatic Detection:**
- Checks for new media every 5 minutes
- Creates action files in `AI_Employee_Vault/Instagram/`
- Supports photos, videos, and carousels

**Action File Format:**
```markdown
# Instagram Post

**Date:** 2026-03-10 20:30:00
**Media ID:** 17841234567890
**Type:** IMAGE

## Caption

Check out this photo! #instagram

**Link:** https://instagram.com/p/...

## Suggested Actions

- [ ] Review post and engagement
- [ ] Respond to comments
```

### 3. Post Creation

**Facebook Posting:**
- Post text updates to Facebook Page
- Automatic validation
- Rate limit handling
- Audit logging

### 4. Comment Monitoring

**Track Engagement:**
- Fetch comments on posts
- Monitor replies
- Track engagement metrics

---

## Usage

### Python API

```python
from social_media_integration.facebook_instagram_monitor import MetaIntegration

# Initialize
meta = MetaIntegration()

# Authenticate
if meta.authenticate():
    print("Authenticated!")

    # Get Facebook posts
    posts = meta.get_facebook_posts(limit=10)
    for post in posts:
        print(f"Post: {post['message']}")

    # Post to Facebook
    post_id = meta.post_to_facebook("Hello from Personal AI Employee!")
    print(f"Posted: {post_id}")

    # Get Instagram media
    media = meta.get_instagram_media(limit=10)
    for item in media:
        print(f"Media: {item['caption']}")

    # Get comments
    comments = meta.get_facebook_comments(post_id, limit=10)
    for comment in comments:
        print(f"Comment: {comment['message']}")
```

### Agent Skills

```bash
# Get Facebook posts
python3 skills_cli.py --skill GetFacebookPostsSkill --params '{"limit": 10}'

# Post to Facebook
python3 skills_cli.py --skill PostToFacebookSkill --params '{"message": "Hello Facebook!"}'

# Get Instagram media
python3 skills_cli.py --skill GetInstagramMediaSkill --params '{"limit": 10}'

# Get statistics
python3 skills_cli.py --skill GetSocialMediaStatisticsSkill
```

### Automated Monitoring

```bash
# Start monitor
cd social_media_integration
python3 facebook_instagram_monitor.py

# Or in background
nohup python3 facebook_instagram_monitor.py > ../logs/social-media-monitor.log 2>&1 &

# Stop monitor
pkill -f facebook_instagram_monitor
```

---

## Agent Skills

### 1. GetFacebookPostsSkill

**Description:** Get recent Facebook posts from authenticated page

**Parameters:**
- `limit` (int, optional, default=10) - Maximum number of posts to fetch

**Returns:**
```json
{
  "count": 5,
  "posts": [
    {
      "id": "123456789_987654321",
      "message": "Post content",
      "created_time": "2026-03-10T20:30:00",
      "permalink_url": "https://facebook.com/..."
    }
  ]
}
```

---

### 2. PostToFacebookSkill

**Description:** Post a message to Facebook page

**Parameters:**
- `message` (str, required) - Message text to post

**Returns:**
```json
{
  "post_id": "123456789_987654321",
  "message": "Hello Facebook!"
}
```

---

### 3. GetInstagramMediaSkill

**Description:** Get recent Instagram media from authenticated account

**Parameters:**
- `limit` (int, optional, default=10) - Maximum number of media items to fetch

**Returns:**
```json
{
  "count": 5,
  "media": [
    {
      "id": "17841234567890",
      "caption": "Photo caption",
      "media_type": "IMAGE",
      "permalink": "https://instagram.com/p/...",
      "timestamp": "2026-03-10T20:30:00"
    }
  ]
}
```

---

### 4. GetSocialMediaStatisticsSkill

**Description:** Get statistics about Facebook and Instagram content in the vault

**Parameters:** None

**Returns:**
```json
{
  "facebook": {
    "total_posts": 15,
    "post_files": ["FACEBOOK-20260310-123.md", ...]
  },
  "instagram": {
    "total_media": 20,
    "media_files": ["INSTAGRAM-20260310-456.md", ...]
  },
  "total": 35
}
```

---

## Configuration

### Monitor Settings

Edit `facebook_instagram_monitor.py`:

```python
# Check interval (seconds)
CHECK_INTERVAL = 300  # 5 minutes

# Maximum items per check
MAX_POSTS = 5
MAX_MEDIA = 5

# Vault paths
FACEBOOK_PATH = VAULT_PATH / "Facebook"
INSTAGRAM_PATH = VAULT_PATH / "Instagram"
```

### API Rate Limits

**Meta Graph API:**
- 200 calls per hour per user
- 4,800 calls per day per app
- Rate limits vary by endpoint

**Rate Limit Handling:**
- Monitor API usage in Facebook Developer Dashboard
- Implement exponential backoff on errors
- Use batch requests for efficiency

---

## Monitoring

### Check Monitor Status

```bash
# Is it running?
ps aux | grep facebook_instagram_monitor | grep -v grep

# View logs
tail -f logs/social-media-monitor.log

# View audit logs
python3 skills_cli.py --skill QueryAuditLogsSkill --params '{"component": "social_media_monitor", "limit": 20}'
```

### Key Metrics

- Facebook posts fetched per cycle
- Instagram media fetched per cycle
- Posts created per day
- Action files created
- API errors
- Rate limit hits

---

## Best Practices

### 1. Secure Your Credentials

```bash
# Set proper permissions
chmod 600 social_media_integration/credentials/meta_credentials.json

# Add to .gitignore
echo "social_media_integration/credentials/meta_credentials.json" >> .gitignore

# Never commit credentials
git status  # Verify not tracked
```

### 2. Use Long-Lived Tokens

- Short-lived tokens expire in 1 hour
- Long-lived tokens last 60 days
- Refresh tokens before expiration
- Store securely

### 3. Monitor API Usage

- Check usage in Facebook Developer Dashboard
- Set up usage alerts
- Implement rate limit handling
- Use batch requests when possible

### 4. Respect Platform Policies

- Follow Facebook Platform Policy
- Follow Instagram Platform Policy
- Don't spam or automate excessively
- Disclose automated behavior

### 5. Test Before Production

```bash
# Test authentication
python3 -c "from facebook_instagram_monitor import MetaIntegration; m = MetaIntegration(); m.authenticate()"

# Test fetching
python3 skills_cli.py --skill GetFacebookPostsSkill --params '{"limit": 1}'

# Test posting (use test page first!)
python3 skills_cli.py --skill PostToFacebookSkill --params '{"message": "Test post"}'
```

---

## Troubleshooting

### Issue: Authentication Failed

**Error:** `❌ Authentication failed`

**Solutions:**
1. Verify access token is valid and not expired
2. Check token has required permissions
3. Verify Page ID is correct
4. Ensure facebook-sdk is installed: `pip3 list | grep facebook-sdk`
5. Regenerate token if needed

### Issue: Instagram Not Working

**Error:** `Instagram account ID not configured`

**Solutions:**
1. Verify Instagram account is Business or Creator
2. Ensure Instagram is linked to Facebook Page
3. Add instagram_account_id to credentials
4. Check Instagram permissions in app settings

### Issue: Rate Limited

**Error:** `Rate limit exceeded`

**Solutions:**
1. Wait for rate limit reset (1 hour)
2. Reduce check frequency
3. Use batch requests
4. Monitor usage in Developer Dashboard

### Issue: Posts Not Detected

**Symptoms:** Monitor running but no posts found

**Solutions:**
1. Check if page actually has posts
2. Verify authentication is successful
3. Check API permissions
4. Review logs for errors

### Issue: facebook-sdk Not Found

**Error:** `ModuleNotFoundError: No module named 'facebook'`

**Solution:**
```bash
pip3 install facebook-sdk
# Or
pip3 install --user facebook-sdk
```

---

## Summary

The Facebook & Instagram Integration provides:

- ✅ **Facebook Page Monitoring** - Automatic post detection
- ✅ **Instagram Business Monitoring** - Media tracking
- ✅ **Post Creation** - Programmatic Facebook posting
- ✅ **Agent Skills** - 4 social media skills
- ✅ **Action Files** - Obsidian integration
- ✅ **Audit Logging** - Complete activity tracking
- ✅ **Unified Interface** - Single API for both platforms
- ✅ **Comprehensive Documentation** - Setup and usage guides

**Status:** Ready for Configuration
**Version:** 1.0.0
**Last Updated:** 2026-03-10

**Note:** Requires Facebook Developer Account, Facebook Page, and API credentials to activate.

---

## Quick Start Checklist

- [ ] Create Facebook Developer Account
- [ ] Create Facebook Page
- [ ] Create Facebook App
- [ ] Generate Page Access Token
- [ ] Get Page ID
- [ ] (Optional) Link Instagram Business Account
- [ ] (Optional) Get Instagram Account ID
- [ ] Install facebook-sdk: `pip3 install facebook-sdk`
- [ ] Copy credentials template
- [ ] Add your credentials
- [ ] Test authentication
- [ ] Start monitor (optional)
- [ ] Test Agent Skills
- [ ] Add to Dashboard

**Ready to connect! 📱**
