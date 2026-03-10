#!/usr/bin/env python3
"""
Twitter (X) Integration
Monitor and interact with Twitter/X API
"""

import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from audit_logger import AuditLogger, EventType

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
TWITTER_PATH = VAULT_PATH / "Twitter"
CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "twitter_credentials.json"
LOG_PATH = Path(__file__).parent.parent / "logs" / "twitter-monitor.log"
CHECK_INTERVAL = 300  # 5 minutes

# Setup logging
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Setup audit logger
audit_logger = AuditLogger("twitter_monitor")


class TwitterIntegration:
    """
    Twitter/X API Integration

    Requires Twitter Developer Account and API credentials:
    - API Key
    - API Secret
    - Access Token
    - Access Token Secret
    - Bearer Token (for API v2)
    """

    def __init__(self):
        self.credentials = None
        self.client = None
        self.authenticated = False

    def load_credentials(self) -> bool:
        """Load Twitter API credentials from file"""
        try:
            if not CREDENTIALS_PATH.exists():
                logger.error(f"Credentials file not found: {CREDENTIALS_PATH}")
                logger.error("Please create twitter_credentials.json with your API keys")
                return False

            with open(CREDENTIALS_PATH, 'r') as f:
                self.credentials = json.load(f)

            # Validate required fields
            required_fields = ['api_key', 'api_secret', 'access_token', 'access_token_secret', 'bearer_token']
            missing_fields = [field for field in required_fields if field not in self.credentials]

            if missing_fields:
                logger.error(f"Missing required credentials: {', '.join(missing_fields)}")
                return False

            logger.info("✅ Twitter credentials loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading credentials: {e}")
            return False

    def authenticate(self) -> bool:
        """
        Authenticate with Twitter API

        Note: Requires tweepy library
        Install: pip3 install tweepy
        """
        try:
            # Check if tweepy is installed
            try:
                import tweepy
            except ImportError:
                logger.error("tweepy library not installed")
                logger.error("Install with: pip3 install tweepy")
                return False

            if not self.credentials:
                if not self.load_credentials():
                    return False

            # Authenticate with Twitter API v2
            self.client = tweepy.Client(
                bearer_token=self.credentials['bearer_token'],
                consumer_key=self.credentials['api_key'],
                consumer_secret=self.credentials['api_secret'],
                access_token=self.credentials['access_token'],
                access_token_secret=self.credentials['access_token_secret'],
                wait_on_rate_limit=True
            )

            # Test authentication
            me = self.client.get_me()
            if me.data:
                logger.info(f"✅ Authenticated as: @{me.data.username}")
                self.authenticated = True
                audit_logger.log_auth_event("twitter_oauth", True, {"username": me.data.username})
                return True
            else:
                logger.error("❌ Authentication failed")
                audit_logger.log_auth_event("twitter_oauth", False)
                return False

        except Exception as e:
            logger.error(f"Authentication error: {e}")
            audit_logger.log_auth_event("twitter_oauth", False, {"error": str(e)})
            return False

    def get_mentions(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent mentions

        Args:
            max_results: Maximum number of mentions to fetch

        Returns:
            List of mention dictionaries
        """
        try:
            if not self.authenticated:
                logger.error("Not authenticated with Twitter")
                return []

            # Get user ID
            me = self.client.get_me()
            user_id = me.data.id

            # Get mentions
            mentions = self.client.get_users_mentions(
                id=user_id,
                max_results=max_results,
                tweet_fields=['created_at', 'author_id', 'text']
            )

            if not mentions.data:
                logger.info("No new mentions found")
                return []

            results = []
            for tweet in mentions.data:
                results.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'author_id': tweet.author_id,
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None
                })

            logger.info(f"Found {len(results)} mention(s)")
            audit_logger.log_event(
                "twitter_mentions_fetched",
                f"Fetched {len(results)} mentions",
                details={"count": len(results)}
            )

            return results

        except Exception as e:
            logger.error(f"Error fetching mentions: {e}")
            audit_logger.log_error("twitter_fetch_error", str(e), None)
            return []

    def get_timeline(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get home timeline tweets

        Args:
            max_results: Maximum number of tweets to fetch

        Returns:
            List of tweet dictionaries
        """
        try:
            if not self.authenticated:
                logger.error("Not authenticated with Twitter")
                return []

            # Get user ID
            me = self.client.get_me()
            user_id = me.data.id

            # Get timeline
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=['created_at', 'text']
            )

            if not tweets.data:
                logger.info("No tweets found")
                return []

            results = []
            for tweet in tweets.data:
                results.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None
                })

            logger.info(f"Found {len(results)} tweet(s)")
            return results

        except Exception as e:
            logger.error(f"Error fetching timeline: {e}")
            return []

    def post_tweet(self, text: str) -> Optional[str]:
        """
        Post a tweet

        Args:
            text: Tweet text (max 280 characters)

        Returns:
            Tweet ID if successful, None otherwise
        """
        try:
            if not self.authenticated:
                logger.error("Not authenticated with Twitter")
                return None

            if len(text) > 280:
                logger.error(f"Tweet too long: {len(text)} characters (max 280)")
                return None

            # Post tweet
            response = self.client.create_tweet(text=text)

            if response.data:
                tweet_id = response.data['id']
                logger.info(f"✅ Tweet posted: {tweet_id}")
                audit_logger.log_event(
                    "twitter_tweet_posted",
                    "Tweet posted successfully",
                    details={"tweet_id": tweet_id, "text_preview": text[:50]}
                )
                return tweet_id
            else:
                logger.error("Failed to post tweet")
                return None

        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            audit_logger.log_error("twitter_post_error", str(e), None)
            return None

    def create_action_file(self, mention: Dict[str, Any]):
        """Create action file for a mention"""
        try:
            TWITTER_PATH.mkdir(parents=True, exist_ok=True)

            # Generate filename
            tweet_id = mention['id']
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"TWITTER-{timestamp}-{tweet_id}.md"
            filepath = TWITTER_PATH / filename

            # Create content
            content = f"""# Twitter Mention

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Tweet ID:** {tweet_id}
**Author ID:** {mention.get('author_id', 'Unknown')}
**Created:** {mention.get('created_at', 'Unknown')}
**Type:** Twitter Mention
**Priority:** Review Required

## Tweet Content

{mention['text']}

---

## Suggested Actions

- [ ] Read and analyze mention
- [ ] Draft response if needed
- [ ] Reply via Twitter
- [ ] Like/retweet if appropriate
- [ ] Archive mention

## Notes

This mention was automatically detected by Twitter Monitor.

**Tweet ID:** {tweet_id}
**Source:** Twitter/X API
"""

            filepath.write_text(content, encoding='utf-8')
            logger.info(f"✅ Created action file: {filename}")

            audit_logger.log_file_created(str(filepath), "twitter")
            audit_logger.log_event(
                "twitter_mention_processed",
                "Twitter mention converted to action file",
                details={"tweet_id": tweet_id, "file_path": str(filepath)}
            )

            return filepath

        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return None


def main():
    """Main monitoring function"""
    logger.info("=" * 60)
    logger.info("🐦 Starting Twitter Monitor")
    logger.info("=" * 60)

    audit_logger.log_system_start()

    # Initialize Twitter integration
    twitter = TwitterIntegration()

    # Authenticate
    if not twitter.authenticate():
        logger.error("❌ Failed to authenticate with Twitter")
        logger.error("Please check your credentials in twitter_credentials.json")
        audit_logger.log_system_stop("authentication_failed")
        return

    logger.info("🔍 Starting monitoring loop...")

    try:
        while True:
            try:
                # Get mentions
                mentions = twitter.get_mentions(max_results=10)

                # Create action files for new mentions
                for mention in mentions:
                    twitter.create_action_file(mention)

                # Wait before next check
                logger.info(f"⏳ Waiting {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                raise

            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}")
                time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("\n👋 Twitter Monitor stopped by user")
        audit_logger.log_system_stop("user_interrupt")


if __name__ == "__main__":
    main()
