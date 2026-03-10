# Twitter (X) Integration - Documentation

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

The Twitter (X) Integration enables the Personal AI Employee to monitor Twitter mentions, post tweets, and manage Twitter interactions through both automated monitoring and Agent Skills.

### Key Features

- **Mention Monitoring** - Automatically detect and process Twitter mentions
- **Tweet Posting** - Post tweets programmatically
- **Action File Creation** - Convert mentions to Obsidian action files
- **Agent Skills** - 4 Twitter-related skills for programmatic access
- **Audit Logging** - All Twitter actions logged to audit system
- **Rate Limit Handling** - Automatic rate limit management

---

## Prerequisites

### 1. Twitter Developer Account

You need a Twitter Developer Account to access the Twitter API.

**Steps:**
1. Go to https://developer.twitter.com/
2. Sign in with your Twitter account
3. Apply for a Developer Account
4. Create a new Project and App
5. Generate API keys and tokens

**Required Access Level:**
- **Free Tier** - Basic access (read-only)
- **Basic Tier ($100/month)** - Read and write access
- **Pro Tier ($5,000/month)** - Full access with higher limits

### 2. Python Dependencies

Install the required library:

```bash
pip3 install tweepy
```

**tweepy** is the official Python library for Twitter API v2.

### 3. API Credentials

You'll need the following credentials:
- API Key (Consumer Key)
- API Secret (Consumer Secret)
- Access Token
- Access Token Secret
- Bearer Token

---

## Setup Guide

### Step 1: Get Twitter API Credentials

1. **Create Twitter Developer Account**
   - Visit https://developer.twitter.com/
   - Apply for developer access
   - Wait for approval (usually instant for basic access)

2. **Create a Project and App**
   - Go to Developer Portal
   - Create a new Project
   - Create an App within the project
   - Note down your App ID

3. **Generate Keys and Tokens**
   - Go to your App settings
   - Navigate to "Keys and tokens" tab
   - Generate:
     - API Key and Secret
     - Access Token and Secret
     - Bearer Token
   - **Save these securely** - you won't see them again!

### Step 2: Configure Credentials

1. **Copy the template:**
   ```bash
   cd twitter_integration/credentials/
   cp twitter_credentials.json.template twitter_credentials.json
   ```

2. **Edit the credentials file:**
   ```bash
   nano twitter_credentials.json
   ```

3. **Add your credentials:**
   ```json
   {
     "api_key": "your_actual_api_key_here",
     "api_secret": "your_actual_api_secret_here",
     "access_token": "your_actual_access_token_here",
     "access_token_secret": "your_actual_access_token_secret_here",
     "bearer_token": "your_actual_bearer_token_here"
   }
   ```

4. **Secure the file:**
   ```bash
   chmod 600 twitter_credentials.json
   ```

### Step 3: Test Authentication

```bash
cd twitter_integration
python3 -c "
from twitter_monitor import TwitterIntegration
twitter = TwitterIntegration()
if twitter.authenticate():
    print('✅ Authentication successful!')
else:
    print('❌ Authentication failed')
"
```

### Step 4: Start Monitoring (Optional)

```bash
# Foreground (for testing)
python3 twitter_monitor.py

# Background (for production)
nohup python3 twitter_monitor.py > ../logs/twitter-monitor.log 2>&1 &
```

---

## Features

### 1. Mention Monitoring

**Automatic Detection:**
- Checks for new mentions every 5 minutes
- Creates action files in `AI_Employee_Vault/Twitter/`
- Logs all mentions to audit system

**Action File Format:**
```markdown
# Twitter Mention

**Date:** 2026-03-10 20:30:00
**Tweet ID:** 1234567890
**Author ID:** 9876543210
**Type:** Twitter Mention

## Tweet Content

@yourusername This is a mention!

## Suggested Actions

- [ ] Read and analyze mention
- [ ] Draft response if needed
- [ ] Reply via Twitter
```

### 2. Tweet Posting

**Programmatic Posting:**
- Post tweets via Agent Skills or Python API
- Automatic character limit validation (280 chars)
- Rate limit handling
- Audit logging

### 3. Timeline Access

**Read Timeline:**
- Fetch your recent tweets
- Access home timeline
- Filter by date/count

### 4. Agent Skills Integration

**4 Twitter Skills:**
- GetTwitterMentionsSkill
- PostTweetSkill
- GetTwitterStatisticsSkill
- ProcessTwitterMentionSkill

---

## Usage

### Python API

```python
from twitter_integration.twitter_monitor import TwitterIntegration

# Initialize
twitter = TwitterIntegration()

# Authenticate
if twitter.authenticate():
    print("Authenticated!")

    # Get mentions
    mentions = twitter.get_mentions(max_results=10)
    for mention in mentions:
        print(f"@{mention['author_id']}: {mention['text']}")

    # Post tweet
    tweet_id = twitter.post_tweet("Hello from Personal AI Employee!")
    print(f"Posted tweet: {tweet_id}")

    # Get timeline
    tweets = twitter.get_timeline(max_results=10)
    for tweet in tweets:
        print(f"{tweet['created_at']}: {tweet['text']}")
```

### Agent Skills

```bash
# Get mentions
python3 skills_cli.py --skill GetTwitterMentionsSkill --params '{"max_results": 10}'

# Post tweet
python3 skills_cli.py --skill PostTweetSkill --params '{"text": "Hello Twitter!"}'

# Get statistics
python3 skills_cli.py --skill GetTwitterStatisticsSkill

# Process specific mention
python3 skills_cli.py --skill ProcessTwitterMentionSkill --params '{"tweet_id": "1234567890"}'
```

### Automated Monitoring

```bash
# Start monitor
cd twitter_integration
python3 twitter_monitor.py

# Or in background
nohup python3 twitter_monitor.py > ../logs/twitter-monitor.log 2>&1 &

# Stop monitor
pkill -f twitter_monitor
```

---

## Agent Skills

### 1. GetTwitterMentionsSkill

**Description:** Get recent Twitter mentions for authenticated account

**Parameters:**
- `max_results` (int, optional, default=10) - Maximum number of mentions to fetch

**Returns:**
```json
{
  "count": 5,
  "mentions": [
    {
      "id": "1234567890",
      "text": "@yourusername Great work!",
      "author_id": "9876543210",
      "created_at": "2026-03-10T20:30:00"
    }
  ]
}
```

**Example:**
```bash
python3 skills_cli.py --skill GetTwitterMentionsSkill --params '{"max_results": 20}'
```

---

### 2. PostTweetSkill

**Description:** Post a tweet to Twitter/X (max 280 characters)

**Parameters:**
- `text` (str, required) - Tweet text (max 280 characters)

**Returns:**
```json
{
  "tweet_id": "1234567890",
  "text": "Hello Twitter!",
  "length": 14
}
```

**Example:**
```bash
python3 skills_cli.py --skill PostTweetSkill --params '{"text": "Automated tweet from Personal AI Employee!"}'
```

---

### 3. GetTwitterStatisticsSkill

**Description:** Get statistics about Twitter mentions in the vault

**Parameters:** None

**Returns:**
```json
{
  "total_mentions": 15,
  "mention_files": ["TWITTER-20260310-1234567890.md", ...]
}
```

**Example:**
```bash
python3 skills_cli.py --skill GetTwitterStatisticsSkill
```

---

### 4. ProcessTwitterMentionSkill

**Description:** Process a Twitter mention and create action file in Obsidian vault

**Parameters:**
- `tweet_id` (str, required) - Twitter tweet ID to process

**Returns:**
```json
{
  "tweet_id": "1234567890",
  "file_path": "/path/to/TWITTER-20260310-1234567890.md",
  "text": "@yourusername Great work!"
}
```

**Example:**
```bash
python3 skills_cli.py --skill ProcessTwitterMentionSkill --params '{"tweet_id": "1234567890"}'
```

---

## Configuration

### Monitor Settings

Edit `twitter_monitor.py`:

```python
# Check interval (seconds)
CHECK_INTERVAL = 300  # 5 minutes

# Maximum mentions per check
MAX_MENTIONS = 10

# Vault path
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
TWITTER_PATH = VAULT_PATH / "Twitter"
```

### API Rate Limits

**Twitter API v2 Free Tier:**
- 500,000 tweets read per month
- 1,500 tweets write per month
- 50 requests per 15 minutes (mentions)

**Rate Limit Handling:**
- tweepy automatically waits when rate limited
- Set `wait_on_rate_limit=True` in client initialization

---

## Monitoring

### Check Monitor Status

```bash
# Is it running?
ps aux | grep twitter_monitor | grep -v grep

# View logs
tail -f logs/twitter-monitor.log

# View audit logs
python3 skills_cli.py --skill QueryAuditLogsSkill --params '{"component": "twitter_monitor", "limit": 20}'
```

### Key Metrics

- Mentions fetched per cycle
- Tweets posted per day
- Action files created
- API errors
- Rate limit hits

### Dashboard Integration

Add to Obsidian Dashboard:

```markdown
## 🐦 Twitter Activity

**This Week:**
- Mentions: [[Twitter/]] (15 files)
- Responses: 8
- Engagement: 92%

🔗 [View All Mentions →](Twitter/)
```

---

## Best Practices

### 1. Secure Your Credentials

```bash
# Set proper permissions
chmod 600 twitter_integration/credentials/twitter_credentials.json

# Add to .gitignore
echo "twitter_integration/credentials/twitter_credentials.json" >> .gitignore

# Never commit credentials
git status  # Verify not tracked
```

### 2. Monitor Rate Limits

```python
# Check rate limit status
import tweepy

client = tweepy.Client(bearer_token="...")
rate_limit = client.get_rate_limit_status()
print(rate_limit)
```

### 3. Handle Errors Gracefully

```python
try:
    mentions = twitter.get_mentions()
except tweepy.TooManyRequests:
    print("Rate limited. Waiting...")
    time.sleep(900)  # Wait 15 minutes
except tweepy.Unauthorized:
    print("Authentication failed. Check credentials.")
```

### 4. Respect Twitter's Terms

- Don't spam
- Don't automate replies without review
- Follow Twitter's Automation Rules
- Disclose bot behavior if applicable

### 5. Test Before Production

```bash
# Test authentication
python3 -c "from twitter_monitor import TwitterIntegration; t = TwitterIntegration(); t.authenticate()"

# Test mention fetching
python3 skills_cli.py --skill GetTwitterMentionsSkill --params '{"max_results": 1}'

# Test posting (use test account first!)
python3 skills_cli.py --skill PostTweetSkill --params '{"text": "Test tweet - please ignore"}'
```

---

## Troubleshooting

### Issue: Authentication Failed

**Error:** `❌ Authentication failed`

**Solutions:**
1. Verify credentials are correct in `twitter_credentials.json`
2. Check API key permissions in Twitter Developer Portal
3. Ensure App has Read and Write permissions
4. Regenerate tokens if needed
5. Check if tweepy is installed: `pip3 list | grep tweepy`

### Issue: Rate Limited

**Error:** `429 Too Many Requests`

**Solutions:**
1. Wait 15 minutes for rate limit reset
2. Reduce check frequency (increase CHECK_INTERVAL)
3. Upgrade to higher API tier if needed
4. Use `wait_on_rate_limit=True` in client

### Issue: Mentions Not Detected

**Symptoms:** Monitor running but no mentions found

**Solutions:**
1. Check if you actually have mentions on Twitter
2. Verify authentication is successful
3. Check API permissions include "Read" access
4. Review logs for errors: `tail logs/twitter-monitor.log`

### Issue: Cannot Post Tweets

**Error:** `Failed to post tweet`

**Solutions:**
1. Verify App has "Read and Write" permissions
2. Check tweet length (max 280 characters)
3. Ensure Access Token has write permissions
4. Check rate limits (1,500 tweets/month on free tier)

### Issue: tweepy Not Found

**Error:** `ModuleNotFoundError: No module named 'tweepy'`

**Solution:**
```bash
pip3 install tweepy
# Or
pip3 install --user tweepy
```

---

## API Reference

### TwitterIntegration Class

```python
class TwitterIntegration:
    def __init__(self):
        """Initialize Twitter integration"""

    def load_credentials(self) -> bool:
        """Load credentials from file"""

    def authenticate(self) -> bool:
        """Authenticate with Twitter API"""

    def get_mentions(self, max_results: int = 10) -> List[Dict]:
        """Get recent mentions"""

    def get_timeline(self, max_results: int = 10) -> List[Dict]:
        """Get home timeline tweets"""

    def post_tweet(self, text: str) -> Optional[str]:
        """Post a tweet, returns tweet ID"""

    def create_action_file(self, mention: Dict) -> Path:
        """Create action file for mention"""
```

---

## Security Considerations

### Credential Storage

- Store credentials in `twitter_credentials.json`
- Set file permissions to 600 (owner read/write only)
- Never commit credentials to git
- Use environment variables for production deployments

### API Key Rotation

Rotate keys regularly:
1. Generate new keys in Twitter Developer Portal
2. Update `twitter_credentials.json`
3. Restart monitor
4. Revoke old keys

### Access Control

- Use separate Twitter accounts for testing and production
- Limit API permissions to minimum required
- Monitor API usage in Developer Portal
- Set up alerts for unusual activity

---

## Future Enhancements

### Phase 1: Enhanced Monitoring

- [ ] Direct message monitoring
- [ ] Keyword tracking
- [ ] Hashtag monitoring
- [ ] User timeline tracking

### Phase 2: Advanced Features

- [ ] Automated responses (with approval)
- [ ] Sentiment analysis
- [ ] Engagement metrics
- [ ] Thread creation

### Phase 3: Analytics

- [ ] Follower growth tracking
- [ ] Engagement rate analysis
- [ ] Best time to post
- [ ] Content performance

---

## Summary

The Twitter (X) Integration provides:

- ✅ **Mention Monitoring** - Automatic detection and processing
- ✅ **Tweet Posting** - Programmatic tweet creation
- ✅ **Agent Skills** - 4 Twitter-related skills
- ✅ **Action Files** - Obsidian integration
- ✅ **Audit Logging** - Complete activity tracking
- ✅ **Rate Limit Handling** - Automatic management
- ✅ **Comprehensive Documentation** - Setup and usage guides

**Status:** Ready for Configuration
**Version:** 1.0.0
**Last Updated:** 2026-03-10

**Note:** Requires Twitter Developer Account and API credentials to activate.

---

## Quick Start Checklist

- [ ] Create Twitter Developer Account
- [ ] Generate API keys and tokens
- [ ] Install tweepy: `pip3 install tweepy`
- [ ] Copy credentials template
- [ ] Add your credentials
- [ ] Test authentication
- [ ] Start monitor (optional)
- [ ] Test Agent Skills
- [ ] Add to Dashboard
- [ ] Configure Ralph Wiggum Loop integration (optional)

**Ready to tweet! 🐦**
