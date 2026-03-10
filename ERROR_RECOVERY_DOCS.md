# Error Recovery & Graceful Degradation - Documentation

## Overview

Enhanced error recovery system implemented for Gmail Watcher and WhatsApp Monitor with retry mechanisms, graceful degradation, and comprehensive logging.

---

## Features Implemented

### 1. Retry Logic with Exponential Backoff

**Decorator Pattern:**
```python
@retry_with_backoff(max_retries=3, initial_delay=1)
def function_name():
    # Function code
```

**Behavior:**
- Retries failed operations up to 3 times
- Exponential backoff: 1s → 2s → 4s → 8s (max 60s)
- Returns None on failure for graceful degradation

**Applied to:**
- Gmail authentication
- Email fetching
- Email detail retrieval
- WhatsApp file parsing
- Action file creation

---

### 2. Graceful Degradation

**System continues running even when:**
- Individual email fetch fails
- Single file parsing fails
- Network temporarily unavailable
- API rate limits hit

**Behavior:**
- Logs error but continues monitoring
- Tracks consecutive failures
- Attempts re-authentication after 5 consecutive failures
- Never crashes the entire system

---

### 3. Comprehensive Logging

**Two-Level Logging:**

1. **Standard Log** (gmail-watcher.log, whatsapp-monitor.log)
   - Basic operation logs
   - Visible in terminal

2. **Detailed Log** (gmail-watcher-detailed.log, whatsapp-monitor-detailed.log)
   - Full error traces
   - Retry attempts
   - Health check results
   - Timestamps for all operations

**Log Levels:**
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Failed operations (with retry)
- DEBUG: Detailed debugging info

---

### 4. Health Monitoring

**Health Checks Track:**
- Consecutive failure count
- Last successful check timestamp
- File system status (credentials, tokens, folders)
- Service availability

**Thresholds:**
- 5 consecutive failures → Re-authentication attempt
- Health status logged periodically

---

### 5. Error Types Handled

**Gmail Watcher:**
- Authentication failures (401, 403)
- Rate limiting (429)
- Network errors (timeout, connection)
- API errors (500, 502, 503)
- Token expiration
- File system errors

**WhatsApp Monitor:**
- File encoding errors (UTF-8, Latin-1 fallback)
- Empty files
- Malformed chat exports
- File system errors
- Parsing errors

---

## Configuration

### Gmail Watcher Enhanced

**File:** `watcher/gmail_watcher_enhanced.py`

**Settings:**
```python
MAX_RETRIES = 3                      # Retry attempts per operation
INITIAL_RETRY_DELAY = 1              # Initial delay (seconds)
MAX_RETRY_DELAY = 60                 # Maximum delay (seconds)
CONSECUTIVE_FAILURE_THRESHOLD = 5    # Re-auth trigger
CHECK_INTERVAL = 120                 # Check every 2 minutes
```

**Logs:**
- Standard: `logs/gmail-watcher.log`
- Detailed: `logs/gmail-watcher-detailed.log`

---

### WhatsApp Monitor Enhanced

**File:** `whatsapp_integration/whatsapp_monitor_enhanced.py`

**Settings:**
```python
MAX_RETRIES = 3                      # Retry attempts per operation
INITIAL_RETRY_DELAY = 1              # Initial delay (seconds)
MAX_RETRY_DELAY = 30                 # Maximum delay (seconds)
CONSECUTIVE_FAILURE_THRESHOLD = 5    # Health check trigger
CHECK_INTERVAL = 60                  # Check every 1 minute
```

**Logs:**
- Standard: `logs/whatsapp-monitor.log`
- Detailed: `logs/whatsapp-monitor-detailed.log`

---

## Usage

### Starting Enhanced Watchers

```bash
# Gmail Watcher
cd watcher
nohup python3 gmail_watcher_enhanced.py > ../logs/gmail-watcher.log 2>&1 &

# WhatsApp Monitor
cd whatsapp_integration
nohup python3 whatsapp_monitor_enhanced.py > ../logs/whatsapp-monitor.log 2>&1 &
```

### Checking Status

```bash
# Check if running
ps aux | grep -E "gmail_watcher_enhanced|whatsapp_monitor_enhanced" | grep -v grep

# View detailed logs
tail -f logs/gmail-watcher-detailed.log
tail -f logs/whatsapp-monitor-detailed.log
```

### Stopping Watchers

```bash
pkill -f gmail_watcher_enhanced
pkill -f whatsapp_monitor_enhanced
```

---

## Error Recovery Examples

### Example 1: Network Timeout

**Scenario:** Gmail API times out

**Behavior:**
1. First attempt fails → Log warning
2. Wait 1 second
3. Second attempt fails → Log warning
4. Wait 2 seconds
5. Third attempt succeeds → Continue normally

**Log Output:**
```
WARNING - Attempt 1/3 failed for get_unread_important_emails: timeout. Retrying in 1s...
WARNING - Attempt 2/3 failed for get_unread_important_emails: timeout. Retrying in 2s...
INFO - Found 5 new important emails
```

---

### Example 2: Token Expiration

**Scenario:** Gmail token expires

**Behavior:**
1. Detect expired token
2. Attempt to refresh token
3. If refresh fails, re-authenticate
4. Save new token
5. Continue monitoring

**Log Output:**
```
INFO - Successfully refreshed credentials
INFO - Token saved successfully
INFO - ✅ Successfully authenticated with Gmail
```

---

### Example 3: Consecutive Failures

**Scenario:** 5 consecutive failures

**Behavior:**
1. Track failure count
2. After 5 failures, trigger re-authentication
3. Reset counter on success
4. Continue monitoring

**Log Output:**
```
ERROR - ❌ Error in monitoring cycle (failure #5): Connection refused
ERROR - 🚨 Too many consecutive failures (5). Attempting to re-authenticate...
INFO - ✅ Re-authentication successful
```

---

### Example 4: File Encoding Error

**Scenario:** WhatsApp export has non-UTF-8 characters

**Behavior:**
1. Try UTF-8 encoding → Fails
2. Log warning
3. Try Latin-1 encoding → Success
4. Parse and create action file

**Log Output:**
```
ERROR - Encoding error reading chat.txt: 'utf-8' codec can't decode. Trying different encoding...
INFO - Successfully read chat.txt with latin-1 encoding
INFO - ✅ Created action file: WHATSAPP-20260310-Contact.md
```

---

## Benefits

### 1. Reliability
- System continues running despite errors
- Automatic recovery from transient failures
- No manual intervention needed

### 2. Visibility
- Detailed logs for debugging
- Health monitoring
- Failure tracking

### 3. Maintainability
- Centralized error handling
- Consistent retry logic
- Easy to adjust thresholds

### 4. Production Ready
- Handles real-world failures
- Graceful degradation
- No data loss

---

## Testing Error Recovery

### Test 1: Network Failure Simulation

```bash
# Disconnect network
# Watchers will retry and log errors
# Reconnect network
# Watchers will recover automatically
```

### Test 2: Invalid File

```bash
# Create empty file in whatsapp_inbox/
touch whatsapp_inbox/test.txt

# Monitor will detect, log error, skip file, continue
```

### Test 3: Token Deletion

```bash
# Delete token file
rm watcher/credentials/gmail_token.pickle

# Watcher will re-authenticate automatically
```

---

## Monitoring

### Key Metrics to Watch

1. **Consecutive Failures**
   - Normal: 0-2
   - Warning: 3-4
   - Critical: 5+

2. **Last Successful Check**
   - Should update every CHECK_INTERVAL
   - If stale > 10 minutes, investigate

3. **Log File Size**
   - Rotate logs if > 100MB
   - Archive old logs

### Health Check Command

```bash
# Check health
tail -20 logs/gmail-watcher-detailed.log | grep -E "ERROR|WARNING|consecutive"
tail -20 logs/whatsapp-monitor-detailed.log | grep -E "ERROR|WARNING|consecutive"
```

---

## Troubleshooting

### Issue: Watcher keeps failing

**Solution:**
1. Check detailed logs for error patterns
2. Verify credentials are valid
3. Check network connectivity
4. Verify API quotas not exceeded

### Issue: No emails detected

**Solution:**
1. Check if watcher is running
2. Verify Gmail has important emails
3. Check processed_ids not blocking
4. Review logs for errors

### Issue: High memory usage

**Solution:**
1. Check log file sizes
2. Restart watchers periodically
3. Clear old processed_ids

---

## Future Enhancements

1. **Metrics Dashboard**
   - Success/failure rates
   - Response times
   - Error trends

2. **Alerting**
   - Email on critical failures
   - Slack notifications
   - SMS alerts

3. **Auto-Recovery**
   - Automatic watcher restart
   - Self-healing mechanisms
   - Intelligent backoff

---

**Status:** ✅ Production Ready
**Version:** 1.0 (Enhanced)
**Last Updated:** 2026-03-10
