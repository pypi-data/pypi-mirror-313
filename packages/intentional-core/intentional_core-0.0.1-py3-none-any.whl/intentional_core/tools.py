# SPDX-FileCopyrightText: 2024-present ZanSara <github@zansara.dev>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Tools baseclass for Intentional.
"""
from typing import List, Any, Dict, Set, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
import structlog
from intentional_core.utils import inheritors


log = structlog.get_logger(logger_name=__name__)


_TOOL_CLASSES = {}
""" This is a global dictionary that maps tool names to their classes """


@dataclass
class ToolParameter:
    """
    A parameter for an Intentional tool.
    """

    name: str
    description: str
    type: Any
    required: bool
    default: Any

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name={self.name}, description={self.description}, type={self.type}, "
            f"required={self.required}, default={self.default}>"
        )


class Tool(ABC):
    """
    Tools baseclass for Intentional.
    """

    id: str = None
    name: str = None
    description: str = None
    parameters: List[ToolParameter] = None

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} id={self.id}, description={self.description}, "
            f"parameters={repr(self.parameters)}>"
        )

    @abstractmethod
    async def run(self, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run the tool.
        """


def load_tools_from_dict(config: List[Dict[str, Any]]) -> Dict[str, Tool]:
    """
    Load a list of tools from a dictionary configuration.

    Args:
        config: The configuration dictionary.

    Returns:
        A list of Tool instances.
    """
    # Get all the subclasses of Tool
    if not _TOOL_CLASSES:
        subclasses: Set[Tool] = inheritors(Tool)
        log.debug("Collected tool classes", tool_classes=subclasses)
        for subclass in subclasses:
            if not subclass.id:
                log.error(
                    "Tool class '%s' does not have an id. This tool will not be usable.",
                    subclass,
                    tool_class=subclass,
                )
                continue

            if subclass.id in _TOOL_CLASSES:
                log.warning(
                    "Duplicate tool '%s' found. The older class will be replaced by the newly imported one.",
                    subclass.id,
                    old_tool_id=subclass.id,
                    old_tool_class=_TOOL_CLASSES[subclass.id],
                    new_tool_class=subclass,
                )
            _TOOL_CLASSES[subclass.id] = subclass

    # Initialize the tools
    tools = {}
    for tool_config in config:
        tool_class = tool_config.pop("id")
        log.debug("Creating tool", tool_class=tool_class)
        if tool_class not in _TOOL_CLASSES:
            raise ValueError(
                f"Unknown tool '{tool_class}'. Available tools: {list(_TOOL_CLASSES)}. "
                "Did you forget to install a plugin?"
            )
        tool_instance: Tool = _TOOL_CLASSES[tool_class](**tool_config)
        if getattr(tool_instance, "name", None) is None:
            raise ValueError(f"Tool '{tool_class}' must have a name.")
        if getattr(tool_instance, "description", None) is None:
            raise ValueError(f"Tool '{tool_class}' must have a description.")
        if getattr(tool_instance, "parameters", None) is None:
            raise ValueError(f"Tool '{tool_class}' must have parameters.")
        tools[tool_instance.name] = tool_instance

    return tools
