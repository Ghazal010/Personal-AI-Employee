#!/usr/bin/env python3
"""
Social Media Skills (Facebook & Instagram)
Skills for Facebook and Instagram operations via Meta Graph API
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_skills.skill_framework import AgentSkill, SkillResult, register_skill
from audit_logger import AuditLogger, EventType


@register_skill
class GetFacebookPostsSkill(AgentSkill):
    """Get recent Facebook posts from page"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("social_media_skill")

    def get_description(self) -> str:
        return "Get recent Facebook posts from authenticated page"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "limit": {
                "type": int,
                "required": False,
                "default": 10,
                "description": "Maximum number of posts to fetch"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute Facebook posts fetching"""
        try:
            limit = kwargs.get('limit', 10)

            # Import Meta integration
            from social_media_integration.facebook_instagram_monitor import MetaIntegration

            # Initialize and authenticate
            meta = MetaIntegration()
            if not meta.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Meta API"
                )

            # Get posts
            posts = meta.get_facebook_posts(limit=limit)

            # Log skill execution
            self.audit_logger.log_event(
                "facebook_posts_fetched",
                f"GetFacebookPostsSkill executed: {len(posts)} posts found",
                details={"count": len(posts)}
            )

            return SkillResult(
                success=True,
                data={
                    "count": len(posts),
                    "posts": posts
                },
                metadata={"limit": limit}
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error fetching Facebook posts: {str(e)}"
            )


@register_skill
class PostToFacebookSkill(AgentSkill):
    """Post a message to Facebook page"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("social_media_skill")

    def get_description(self) -> str:
        return "Post a message to Facebook page"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "message": {
                "type": str,
                "required": True,
                "description": "Message text to post"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute Facebook posting"""
        try:
            message = kwargs.get('message')

            # Import Meta integration
            from social_media_integration.facebook_instagram_monitor import MetaIntegration

            # Initialize and authenticate
            meta = MetaIntegration()
            if not meta.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Meta API"
                )

            # Post to Facebook
            post_id = meta.post_to_facebook(message)

            if not post_id:
                return SkillResult(
                    success=False,
                    error="Failed to post to Facebook"
                )

            # Log skill execution
            self.audit_logger.log_event(
                "facebook_post_created",
                f"PostToFacebookSkill executed: post {post_id}",
                details={"post_id": post_id, "message_preview": message[:50]}
            )

            return SkillResult(
                success=True,
                data={
                    "post_id": post_id,
                    "message": message
                }
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error posting to Facebook: {str(e)}"
            )


@register_skill
class GetInstagramMediaSkill(AgentSkill):
    """Get recent Instagram media from account"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("social_media_skill")

    def get_description(self) -> str:
        return "Get recent Instagram media from authenticated account"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "limit": {
                "type": int,
                "required": False,
                "default": 10,
                "description": "Maximum number of media items to fetch"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute Instagram media fetching"""
        try:
            limit = kwargs.get('limit', 10)

            # Import Meta integration
            from social_media_integration.facebook_instagram_monitor import MetaIntegration

            # Initialize and authenticate
            meta = MetaIntegration()
            if not meta.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Meta API"
                )

            # Get media
            media = meta.get_instagram_media(limit=limit)

            # Log skill execution
            self.audit_logger.log_event(
                "instagram_media_fetched",
                f"GetInstagramMediaSkill executed: {len(media)} media items found",
                details={"count": len(media)}
            )

            return SkillResult(
                success=True,
                data={
                    "count": len(media),
                    "media": media
                },
                metadata={"limit": limit}
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error fetching Instagram media: {str(e)}"
            )


@register_skill
class GetSocialMediaStatisticsSkill(AgentSkill):
    """Get social media statistics from vault"""

    def __init__(self):
        super().__init__()
        self.vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        self.facebook_path = self.vault_path / "Facebook"
        self.instagram_path = self.vault_path / "Instagram"

    def get_description(self) -> str:
        return "Get statistics about Facebook and Instagram content in the vault"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, **kwargs) -> SkillResult:
        """Execute statistics gathering"""
        try:
            # Count Facebook files
            facebook_count = 0
            facebook_files = []
            if self.facebook_path.exists():
                facebook_files = list(self.facebook_path.glob("FACEBOOK-*.md"))
                facebook_count = len(facebook_files)

            # Count Instagram files
            instagram_count = 0
            instagram_files = []
            if self.instagram_path.exists():
                instagram_files = list(self.instagram_path.glob("INSTAGRAM-*.md"))
                instagram_count = len(instagram_files)

            return SkillResult(
                success=True,
                data={
                    "facebook": {
                        "total_posts": facebook_count,
                        "post_files": [f.name for f in facebook_files]
                    },
                    "instagram": {
                        "total_media": instagram_count,
                        "media_files": [f.name for f in instagram_files]
                    },
                    "total": facebook_count + instagram_count
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error getting social media statistics: {str(e)}"
            )
