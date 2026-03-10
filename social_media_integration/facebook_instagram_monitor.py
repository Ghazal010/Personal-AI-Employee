#!/usr/bin/env python3
"""
Facebook & Instagram Integration
Monitor and interact with Facebook and Instagram APIs via Meta Graph API
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
FACEBOOK_PATH = VAULT_PATH / "Facebook"
INSTAGRAM_PATH = VAULT_PATH / "Instagram"
CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "meta_credentials.json"
LOG_PATH = Path(__file__).parent.parent / "logs" / "social-media-monitor.log"
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
audit_logger = AuditLogger("social_media_monitor")


class MetaIntegration:
    """
    Facebook & Instagram API Integration via Meta Graph API

    Requires:
    - Facebook Developer Account
    - Facebook App with appropriate permissions
    - Instagram Business or Creator Account (for Instagram)
    - Access Token with required scopes
    """

    def __init__(self):
        self.credentials = None
        self.access_token = None
        self.authenticated = False
        self.facebook_page_id = None
        self.instagram_account_id = None

    def load_credentials(self) -> bool:
        """Load Meta API credentials from file"""
        try:
            if not CREDENTIALS_PATH.exists():
                logger.error(f"Credentials file not found: {CREDENTIALS_PATH}")
                logger.error("Please create meta_credentials.json with your API credentials")
                return False

            with open(CREDENTIALS_PATH, 'r') as f:
                self.credentials = json.load(f)

            # Validate required fields
            required_fields = ['access_token', 'facebook_page_id']
            missing_fields = [field for field in required_fields if field not in self.credentials]

            if missing_fields:
                logger.error(f"Missing required credentials: {', '.join(missing_fields)}")
                return False

            self.access_token = self.credentials['access_token']
            self.facebook_page_id = self.credentials['facebook_page_id']
            self.instagram_account_id = self.credentials.get('instagram_account_id')

            logger.info("✅ Meta credentials loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading credentials: {e}")
            return False

    def authenticate(self) -> bool:
        """
        Authenticate with Meta Graph API

        Note: Requires facebook-sdk library
        Install: pip3 install facebook-sdk
        """
        try:
            # Check if facebook-sdk is installed
            try:
                import facebook
            except ImportError:
                logger.error("facebook-sdk library not installed")
                logger.error("Install with: pip3 install facebook-sdk")
                return False

            if not self.credentials:
                if not self.load_credentials():
                    return False

            # Initialize Graph API
            self.graph = facebook.GraphAPI(access_token=self.access_token, version="3.0")

            # Test authentication by getting page info
            try:
                page_info = self.graph.get_object(id=self.facebook_page_id, fields='name,id')
                logger.info(f"✅ Authenticated with Facebook Page: {page_info['name']}")
                self.authenticated = True
                audit_logger.log_auth_event("meta_oauth", True, {"page_name": page_info['name']})
                return True
            except Exception as e:
                logger.error(f"❌ Authentication failed: {e}")
                audit_logger.log_auth_event("meta_oauth", False, {"error": str(e)})
                return False

        except Exception as e:
            logger.error(f"Authentication error: {e}")
            audit_logger.log_auth_event("meta_oauth", False, {"error": str(e)})
            return False

    def get_facebook_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent Facebook posts from page

        Args:
            limit: Maximum number of posts to fetch

        Returns:
            List of post dictionaries
        """
        try:
            if not self.authenticated:
                logger.error("Not authenticated with Meta API")
                return []

            # Get posts
            posts = self.graph.get_connections(
                id=self.facebook_page_id,
                connection_name='posts',
                fields='id,message,created_time,permalink_url',
                limit=limit
            )

            results = []
            for post in posts.get('data', []):
                results.append({
                    'id': post.get('id'),
                    'message': post.get('message', ''),
                    'created_time': post.get('created_time'),
                    'permalink_url': post.get('permalink_url')
                })

            logger.info(f"Found {len(results)} Facebook post(s)")
            audit_logger.log_event(
                "facebook_posts_fetched",
                f"Fetched {len(results)} Facebook posts",
                details={"count": len(results)}
            )

            return results

        except Exception as e:
            logger.error(f"Error fetching Facebook posts: {e}")
            audit_logger.log_error("facebook_fetch_error", str(e), None)
            return []

    def get_facebook_comments(self, post_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get comments on a Facebook post

        Args:
            post_id: Facebook post ID
            limit: Maximum number of comments to fetch

        Returns:
            List of comment dictionaries
        """
        try:
            if not self.authenticated:
                logger.error("Not authenticated with Meta API")
                return []

            # Get comments
            comments = self.graph.get_connections(
                id=post_id,
                connection_name='comments',
                fields='id,message,from,created_time',
                limit=limit
            )

            results = []
            for comment in comments.get('data', []):
                results.append({
                    'id': comment.get('id'),
                    'message': comment.get('message', ''),
                    'from': comment.get('from', {}),
                    'created_time': comment.get('created_time')
                })

            logger.info(f"Found {len(results)} comment(s) on post {post_id}")
            return results

        except Exception as e:
            logger.error(f"Error fetching comments: {e}")
            return []

    def post_to_facebook(self, message: str) -> Optional[str]:
        """
        Post a message to Facebook page

        Args:
            message: Message text to post

        Returns:
            Post ID if successful, None otherwise
        """
        try:
            if not self.authenticated:
                logger.error("Not authenticated with Meta API")
                return None

            # Post to page
            result = self.graph.put_object(
                parent_object=self.facebook_page_id,
                connection_name='feed',
                message=message
            )

            post_id = result.get('id')
            if post_id:
                logger.info(f"✅ Posted to Facebook: {post_id}")
                audit_logger.log_event(
                    "facebook_post_created",
                    "Posted to Facebook page",
                    details={"post_id": post_id, "message_preview": message[:50]}
                )
                return post_id
            else:
                logger.error("Failed to post to Facebook")
                return None

        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            audit_logger.log_error("facebook_post_error", str(e), None)
            return None

    def get_instagram_media(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent Instagram media from account

        Args:
            limit: Maximum number of media items to fetch

        Returns:
            List of media dictionaries
        """
        try:
            if not self.authenticated:
                logger.error("Not authenticated with Meta API")
                return []

            if not self.instagram_account_id:
                logger.error("Instagram account ID not configured")
                return []

            # Get media
            media = self.graph.get_connections(
                id=self.instagram_account_id,
                connection_name='media',
                fields='id,caption,media_type,media_url,permalink,timestamp',
                limit=limit
            )

            results = []
            for item in media.get('data', []):
                results.append({
                    'id': item.get('id'),
                    'caption': item.get('caption', ''),
                    'media_type': item.get('media_type'),
                    'media_url': item.get('media_url'),
                    'permalink': item.get('permalink'),
                    'timestamp': item.get('timestamp')
                })

            logger.info(f"Found {len(results)} Instagram media item(s)")
            audit_logger.log_event(
                "instagram_media_fetched",
                f"Fetched {len(results)} Instagram media items",
                details={"count": len(results)}
            )

            return results

        except Exception as e:
            logger.error(f"Error fetching Instagram media: {e}")
            audit_logger.log_error("instagram_fetch_error", str(e), None)
            return []

    def get_instagram_comments(self, media_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get comments on an Instagram media item

        Args:
            media_id: Instagram media ID
            limit: Maximum number of comments to fetch

        Returns:
            List of comment dictionaries
        """
        try:
            if not self.authenticated:
                logger.error("Not authenticated with Meta API")
                return []

            # Get comments
            comments = self.graph.get_connections(
                id=media_id,
                connection_name='comments',
                fields='id,text,username,timestamp',
                limit=limit
            )

            results = []
            for comment in comments.get('data', []):
                results.append({
                    'id': comment.get('id'),
                    'text': comment.get('text', ''),
                    'username': comment.get('username'),
                    'timestamp': comment.get('timestamp')
                })

            logger.info(f"Found {len(results)} comment(s) on media {media_id}")
            return results

        except Exception as e:
            logger.error(f"Error fetching Instagram comments: {e}")
            return []

    def create_facebook_action_file(self, post: Dict[str, Any]):
        """Create action file for a Facebook post"""
        try:
            FACEBOOK_PATH.mkdir(parents=True, exist_ok=True)

            # Generate filename
            post_id = post['id'].replace('_', '-')
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"FACEBOOK-{timestamp}-{post_id[:20]}.md"
            filepath = FACEBOOK_PATH / filename

            # Create content
            content = f"""# Facebook Post

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Post ID:** {post['id']}
**Created:** {post.get('created_time', 'Unknown')}
**Type:** Facebook Post
**Priority:** Review Required

## Post Content

{post.get('message', '*No message*')}

**Link:** {post.get('permalink_url', 'N/A')}

---

## Suggested Actions

- [ ] Read and analyze post
- [ ] Check engagement (likes, comments, shares)
- [ ] Respond to comments if needed
- [ ] Share or boost if appropriate
- [ ] Archive post

## Notes

This post was automatically detected by Social Media Monitor.

**Post ID:** {post['id']}
**Source:** Facebook Graph API
"""

            filepath.write_text(content, encoding='utf-8')
            logger.info(f"✅ Created Facebook action file: {filename}")

            audit_logger.log_file_created(str(filepath), "facebook")
            audit_logger.log_event(
                "facebook_post_processed",
                "Facebook post converted to action file",
                details={"post_id": post['id'], "file_path": str(filepath)}
            )

            return filepath

        except Exception as e:
            logger.error(f"Error creating Facebook action file: {e}")
            return None

    def create_instagram_action_file(self, media: Dict[str, Any]):
        """Create action file for an Instagram media item"""
        try:
            INSTAGRAM_PATH.mkdir(parents=True, exist_ok=True)

            # Generate filename
            media_id = media['id']
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"INSTAGRAM-{timestamp}-{media_id[:20]}.md"
            filepath = INSTAGRAM_PATH / filename

            # Create content
            content = f"""# Instagram Post

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Media ID:** {media['id']}
**Type:** {media.get('media_type', 'Unknown')}
**Posted:** {media.get('timestamp', 'Unknown')}
**Priority:** Review Required

## Caption

{media.get('caption', '*No caption*')}

**Link:** {media.get('permalink', 'N/A')}

**Media URL:** {media.get('media_url', 'N/A')}

---

## Suggested Actions

- [ ] Review post and engagement
- [ ] Respond to comments
- [ ] Check insights/analytics
- [ ] Share to stories if appropriate
- [ ] Archive post

## Notes

This post was automatically detected by Social Media Monitor.

**Media ID:** {media['id']}
**Source:** Instagram Graph API
"""

            filepath.write_text(content, encoding='utf-8')
            logger.info(f"✅ Created Instagram action file: {filename}")

            audit_logger.log_file_created(str(filepath), "instagram")
            audit_logger.log_event(
                "instagram_media_processed",
                "Instagram media converted to action file",
                details={"media_id": media['id'], "file_path": str(filepath)}
            )

            return filepath

        except Exception as e:
            logger.error(f"Error creating Instagram action file: {e}")
            return None


def main():
    """Main monitoring function"""
    logger.info("=" * 60)
    logger.info("📱 Starting Social Media Monitor (Facebook & Instagram)")
    logger.info("=" * 60)

    audit_logger.log_system_start()

    # Initialize Meta integration
    meta = MetaIntegration()

    # Authenticate
    if not meta.authenticate():
        logger.error("❌ Failed to authenticate with Meta API")
        logger.error("Please check your credentials in meta_credentials.json")
        audit_logger.log_system_stop("authentication_failed")
        return

    logger.info("🔍 Starting monitoring loop...")

    try:
        while True:
            try:
                # Get Facebook posts
                logger.info("📘 Checking Facebook posts...")
                fb_posts = meta.get_facebook_posts(limit=5)
                for post in fb_posts:
                    meta.create_facebook_action_file(post)

                # Get Instagram media (if configured)
                if meta.instagram_account_id:
                    logger.info("📸 Checking Instagram media...")
                    ig_media = meta.get_instagram_media(limit=5)
                    for media in ig_media:
                        meta.create_instagram_action_file(media)

                # Wait before next check
                logger.info(f"⏳ Waiting {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                raise

            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}")
                time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("\n👋 Social Media Monitor stopped by user")
        audit_logger.log_system_stop("user_interrupt")


if __name__ == "__main__":
    main()
