"""
Tool Executor for Streaming LLM Responses

Handles execution of tools called by LLMs during streaming responses.
"""

import json
from typing import Dict, List, Any, Callable, Optional

from .diagram_tools import DiagramTools


class ToolExecutor:
    """
    Executes tools called by LLMs
    
    Integrates with streaming responses to execute tools as they're called
    and return results back to the LLM.
    """
    
    def __init__(self, shape_library_path: Optional[str] = None):
        """
        Initialize tool executor
        
        Args:
            shape_library_path: Path to shape library files
        """
        self.diagram_tools = DiagramTools(shape_library_path)
    
    def get_tools(self) -> List[Dict]:
        """
        Get all available tool definitions
        
        Returns:
            List of tool definitions for LLM
        """
        return DiagramTools.get_tool_definitions()
    
    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        return self.diagram_tools.execute_tool(tool_name, arguments)
    
    def execute_from_response(self, tool_calls: List[Dict]) -> List[Dict]:
        """
        Execute multiple tools from LLM response
        
        Args:
            tool_calls: List of tool calls from LLM
            
        Returns:
            List of tool results
        """
        results = []
        
        for tool_call in tool_calls:
            tool_name = tool_call.get("function", {}).get("name")
            
            # Parse arguments
            args_str = tool_call.get("function", {}).get("arguments", "{}")
            try:
                arguments = json.loads(args_str)
            except json.JSONDecodeError:
                results.append({
                    "tool_call_id": tool_call.get("id"),
                    "success": False,
                    "error": "Invalid JSON in tool arguments"
                })
                continue
            
            # Execute tool
            result = self.execute(tool_name, arguments)
            result["tool_call_id"] = tool_call.get("id")
            results.append(result)
        
        return results
    
    def get_current_diagram(self) -> Optional[str]:
        """Get the current diagram XML"""
        return self.diagram_tools.current_diagram_xml
    
    def set_current_diagram(self, xml: str):
        """Set the current diagram XML"""
        self.diagram_tools.current_diagram_xml = xml
