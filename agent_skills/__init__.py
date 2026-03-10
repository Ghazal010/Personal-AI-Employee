#!/usr/bin/env python3
"""
Agent Skills Package
Modular, reusable capabilities for AI agents
"""

from agent_skills.skill_framework import (
    AgentSkill,
    SkillResult,
    SkillRegistry,
    skill_registry,
    register_skill,
    execute_skill,
    list_skills
)

# Import all skill modules to register them
import agent_skills.email_skills
import agent_skills.whatsapp_skills
import agent_skills.audit_skills
import agent_skills.task_skills
import agent_skills.twitter_skills
import agent_skills.social_media_skills
import agent_skills.odoo_skills

__version__ = "1.0.0"
__all__ = [
    "AgentSkill",
    "SkillResult",
    "SkillRegistry",
    "skill_registry",
    "register_skill",
    "execute_skill",
    "list_skills"
]
