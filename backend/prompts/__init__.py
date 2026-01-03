"""
System Prompts Package

Provides system prompts for LLM-powered diagram generation.
"""

from .system_prompts import (
    get_system_prompt,
    get_xml_rules,
    get_layout_constraints,
    get_shape_instructions,
    get_minimal_prompt,
)

__all__ = [
    "get_system_prompt",
    "get_xml_rules",
    "get_layout_constraints",
    "get_shape_instructions",
    "get_minimal_prompt",
]
