#!/usr/bin/env python3
"""
Agent Skills Framework
Modular, reusable capabilities for AI agents
"""

import json
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod


class SkillResult:
    """Standard result format for all skills"""

    def __init__(self, success: bool, data: Any = None, error: Optional[str] = None, metadata: Optional[Dict] = None):
        self.success = success
        self.data = data
        self.error = error
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


class AgentSkill(ABC):
    """Base class for all agent skills"""

    def __init__(self):
        self.name = self.__class__.__name__
        self.version = "1.0"

    @abstractmethod
    def execute(self, **kwargs) -> SkillResult:
        """Execute the skill with given parameters"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get skill description"""
        pass

    @abstractmethod
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        """Get parameter definitions"""
        pass

    def validate_parameters(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate parameters against schema"""
        param_defs = self.get_parameters()

        # Check required parameters
        for param_name, param_def in param_defs.items():
            if param_def.get('required', False) and param_name not in params:
                return False, f"Missing required parameter: {param_name}"

        # Check parameter types
        for param_name, param_value in params.items():
            if param_name in param_defs:
                expected_type = param_defs[param_name].get('type')
                if expected_type and not isinstance(param_value, expected_type):
                    return False, f"Invalid type for {param_name}: expected {expected_type.__name__}"

        return True, None

    def get_metadata(self) -> Dict[str, Any]:
        """Get skill metadata"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.get_description(),
            "parameters": self.get_parameters()
        }


class SkillRegistry:
    """Registry for managing available skills"""

    def __init__(self):
        self.skills: Dict[str, AgentSkill] = {}

    def register(self, skill: AgentSkill):
        """Register a skill"""
        self.skills[skill.name] = skill

    def get_skill(self, name: str) -> Optional[AgentSkill]:
        """Get skill by name"""
        return self.skills.get(name)

    def list_skills(self) -> List[Dict[str, Any]]:
        """List all registered skills"""
        return [skill.get_metadata() for skill in self.skills.values()]

    def execute_skill(self, name: str, **kwargs) -> SkillResult:
        """Execute a skill by name"""
        skill = self.get_skill(name)

        if not skill:
            return SkillResult(
                success=False,
                error=f"Skill not found: {name}"
            )

        # Validate parameters
        valid, error = skill.validate_parameters(kwargs)
        if not valid:
            return SkillResult(
                success=False,
                error=error
            )

        # Execute skill
        try:
            return skill.execute(**kwargs)
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"Skill execution failed: {str(e)}"
            )


# Global skill registry
skill_registry = SkillRegistry()


def register_skill(skill_class):
    """Decorator to register a skill"""
    skill_instance = skill_class()
    skill_registry.register(skill_instance)
    return skill_class


# Convenience function
def execute_skill(name: str, **kwargs) -> SkillResult:
    """Execute a skill by name"""
    return skill_registry.execute_skill(name, **kwargs)


def list_skills() -> List[Dict[str, Any]]:
    """List all available skills"""
    return skill_registry.list_skills()
