#!/usr/bin/env python3
"""
Twitter Skills
Skills for Twitter/X operations
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_skills.skill_framework import AgentSkill, SkillResult, register_skill
from audit_logger import AuditLogger, EventType


@register_skill
class GetTwitterMentionsSkill(AgentSkill):
    """Get recent Twitter mentions"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("twitter_skill")

    def get_description(self) -> str:
        return "Get recent Twitter mentions for authenticated account"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "max_results": {
                "type": int,
                "required": False,
                "default": 10,
                "description": "Maximum number of mentions to fetch"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute mention fetching"""
        try:
            max_results = kwargs.get('max_results', 10)

            # Import Twitter integration
            from twitter_integration.twitter_monitor import TwitterIntegration

            # Initialize and authenticate
            twitter = TwitterIntegration()
            if not twitter.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Twitter API"
                )

            # Get mentions
            mentions = twitter.get_mentions(max_results=max_results)

            # Log skill execution
            self.audit_logger.log_event(
                "twitter_mentions_fetched",
                f"GetTwitterMentionsSkill executed: {len(mentions)} mentions found",
                details={"count": len(mentions)}
            )

            return SkillResult(
                success=True,
                data={
                    "count": len(mentions),
                    "mentions": mentions
                },
                metadata={"max_results": max_results}
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error fetching Twitter mentions: {str(e)}"
            )


@register_skill
class PostTweetSkill(AgentSkill):
    """Post a tweet to Twitter"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("twitter_skill")

    def get_description(self) -> str:
        return "Post a tweet to Twitter/X (max 280 characters)"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "text": {
                "type": str,
                "required": True,
                "description": "Tweet text (max 280 characters)"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute tweet posting"""
        try:
            text = kwargs.get('text')

            if len(text) > 280:
                return SkillResult(
                    success=False,
                    error=f"Tweet too long: {len(text)} characters (max 280)"
                )

            # Import Twitter integration
            from twitter_integration.twitter_monitor import TwitterIntegration

            # Initialize and authenticate
            twitter = TwitterIntegration()
            if not twitter.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Twitter API"
                )

            # Post tweet
            tweet_id = twitter.post_tweet(text)

            if not tweet_id:
                return SkillResult(
                    success=False,
                    error="Failed to post tweet"
                )

            # Log skill execution
            self.audit_logger.log_event(
                "twitter_tweet_posted",
                f"PostTweetSkill executed: tweet {tweet_id}",
                details={"tweet_id": tweet_id, "text_preview": text[:50]}
            )

            return SkillResult(
                success=True,
                data={
                    "tweet_id": tweet_id,
                    "text": text,
                    "length": len(text)
                }
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error posting tweet: {str(e)}"
            )


@register_skill
class GetTwitterStatisticsSkill(AgentSkill):
    """Get Twitter statistics from vault"""

    def __init__(self):
        super().__init__()
        self.vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        self.twitter_path = self.vault_path / "Twitter"

    def get_description(self) -> str:
        return "Get statistics about Twitter mentions in the vault"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {}

    def execute(self, **kwargs) -> SkillResult:
        """Execute statistics gathering"""
        try:
            if not self.twitter_path.exists():
                return SkillResult(
                    success=True,
                    data={"total_mentions": 0, "mention_files": []}
                )

            # Count mention files
            mention_files = list(self.twitter_path.glob("TWITTER-*.md"))

            return SkillResult(
                success=True,
                data={
                    "total_mentions": len(mention_files),
                    "mention_files": [f.name for f in mention_files]
                }
            )

        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Error getting Twitter statistics: {str(e)}"
            )


@register_skill
class ProcessTwitterMentionSkill(AgentSkill):
    """Process a Twitter mention and create action file"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("twitter_skill")

    def get_description(self) -> str:
        return "Process a Twitter mention and create action file in Obsidian vault"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "tweet_id": {
                "type": str,
                "required": True,
                "description": "Twitter tweet ID to process"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute mention processing"""
        try:
            tweet_id = kwargs.get('tweet_id')

            # Import Twitter integration
            from twitter_integration.twitter_monitor import TwitterIntegration

            # Initialize and authenticate
            twitter = TwitterIntegration()
            if not twitter.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Twitter API"
                )

            # Get mentions and find the specific one
            mentions = twitter.get_mentions(max_results=100)
            mention = next((m for m in mentions if str(m['id']) == str(tweet_id)), None)

            if not mention:
                return SkillResult(
                    success=False,
                    error=f"Mention not found: {tweet_id}"
                )

            # Create action file
            filepath = twitter.create_action_file(mention)

            if not filepath:
                return SkillResult(
                    success=False,
                    error=f"Failed to create action file for mention {tweet_id}"
                )

            # Log skill execution
            self.audit_logger.log_event(
                "twitter_mention_processed",
                f"ProcessTwitterMentionSkill executed: {tweet_id}",
                details={
                    "tweet_id": tweet_id,
                    "file_path": str(filepath)
                }
            )

            return SkillResult(
                success=True,
                data={
                    "tweet_id": tweet_id,
                    "file_path": str(filepath),
                    "text": mention['text']
                }
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error processing Twitter mention: {str(e)}"
            )
