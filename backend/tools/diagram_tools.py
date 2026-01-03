"""
Diagram Tools for AI-Powered Generation

Implements the 4 core tools that LLMs use to create and manipulate diagrams:
1. display_diagram - Create new diagrams
2. edit_diagram - Modify existing diagrams
3. get_shape_library - Access professional libraries
4. append_diagram - Continue truncated diagrams
"""

import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .xml_utils import (
    validate_and_fix_xml,
    wrap_mxfile,
    apply_edit_operation,
    XMLValidationError,
)


# Pydantic models for tool inputs
class DisplayDiagramInput(BaseModel):
    """Input for display_diagram tool"""
    xml: str = Field(
        description="XML string containing ONLY mxCell elements (no wrapper tags)"
    )


class EditOperation(BaseModel):
    """Single edit operation"""
    operation: str = Field(description="Operation type: 'add', 'update', or 'delete'")
    cell_id: str = Field(description="ID of the cell to edit")
    new_xml: Optional[str] = Field(
        None,
        description="New XML for the cell (required for 'add' and 'update')"
    )


class EditDiagramInput(BaseModel):
    """Input for edit_diagram tool"""
    operations: List[EditOperation] = Field(
        description="List of edit operations to apply"
    )


class GetShapeLibraryInput(BaseModel):
    """Input for get_shape_library tool"""
    library: str = Field(
        description="Library name: aws4, azure2, gcp2, kubernetes, cisco19, flowchart"
    )


class AppendDiagramInput(BaseModel):
    """Input for append_diagram tool"""
    xml: str = Field(
        description="Additional mxCell elements to append to the current diagram"
    )


class DiagramTools:
    """
    AI tools for diagram generation and manipulation
    
    These tools are designed to be called by LLMs via function calling.
    Each tool has a clear purpose and follows draw.io's XML format.
    """
    
    def __init__(self, shape_library_path: Optional[str] = None):
        """
        Initialize diagram tools
        
        Args:
            shape_library_path: Path to shape library markdown files
        """
        self.shape_library_path = shape_library_path or os.path.join(
            os.path.dirname(__file__),
            "..", "shape_libraries"
        )
        self.current_diagram_xml: Optional[str] = None
    
    @staticmethod
    def get_tool_definitions() -> List[Dict]:
        """
        Get OpenAI-compatible tool definitions
        
        Returns:
            List of tool definition dictionaries
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "display_diagram",
                    "description": """Display a diagram on draw.io. 
Pass ONLY the mxCell elements - wrapper tags will be added automatically.

CRITICAL VALIDATION RULES:
1. Generate ONLY mxCell elements - NO wrapper tags (<mxfile>, <mxGraphModel>, <root>)
2. Do NOT include root cells (id="0" or id="1")
3. All mxCell elements must be siblings - NEVER nest them
4. Every mxCell needs a unique id attribute (start from "2")
5. Every mxCell needs a valid parent attribute (use "1" for top-level elements)
6. Every vertex/edge needs a <mxGeometry> child element with x, y, width, height
7. Escape XML special characters in values: &lt; &gt; &amp; &quot;

LAYOUT CONSTRAINTS:
- Viewport: Position elements within x: 0-800, y: 0-600
- Starting position: x=40, y=40 (leave margins)
- Spacing: 120px between elements
- Element sizes: 80-120px wide, 40-60px tall
- No overlapping elements

EXAMPLE (correct format):
<mxCell id="2" value="User" style="ellipse;fillColor=#dae8fc;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="80" height="40" as="geometry"/>
</mxCell>
<mxCell id="3" value="API Server" style="rectangle;fillColor=#d5e8d4;" vertex="1" parent="1">
  <mxGeometry x="160" y="40" width="120" height="60" as="geometry"/>
</mxCell>
<mxCell id="4" value="" style="endArrow=classic;html=1;" edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

COMMON MISTAKES TO AVOID:
❌ Including <mxfile>, <mxGraphModel>, or <root> tags
❌ Nesting mxCell elements inside each other
❌ Missing or duplicate IDs
❌ Missing parent attribute
❌ Missing mxGeometry element for shapes
❌ Overlapping elements""",
                    "parameters": DisplayDiagramInput.model_json_schema()
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_diagram",
                    "description": """Edit the current diagram using ID-based operations.

Use this for incremental changes instead of regenerating the entire diagram.

OPERATIONS:
- 'add': Add a new cell to the diagram
- 'update': Replace an existing cell by its ID
- 'delete': Remove a cell by its ID

⚠️ CRITICAL: When providing new_xml in JSON, all double quotes MUST be escaped as \\"

EXAMPLES:

Add a new shape:
{
  "operations": [{
    "operation": "add",
    "cell_id": "new-shape-5",
    "new_xml": "<mxCell id=\\"new-shape-5\\" value=\\"Cache\\" style=\\"cylinder\\" vertex=\\"1\\" parent=\\"1\\"><mxGeometry x=\\"300\\" y=\\"100\\" width=\\"80\\" height=\\"60\\"/></mxCell>"
  }]
}

Update existing shape:
{
  "operations": [{
    "operation": "update",
    "cell_id": "3",
    "new_xml": "<mxCell id=\\"3\\" value=\\"REST API\\" style=\\"rectangle;fillColor=#ffe6cc;\\" vertex=\\"1\\" parent=\\"1\\"><mxGeometry x=\\"160\\" y=\\"40\\" width=\\"120\\" height=\\"60\\"/></mxCell>"
  }]
}

Delete shape:
{
  "operations": [{
    "operation": "delete",
    "cell_id": "old-shape-4"
  }]
}

Multiple operations:
{
  "operations": [
    {"operation": "delete", "cell_id": "old-1"},
    {"operation": "add", "cell_id": "new-1", "new_xml": "..."},
    {"operation": "update", "cell_id": "existing-2", "new_xml": "..."}
  ]
}""",
                    "parameters": EditDiagramInput.model_json_schema()
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_shape_library",
                    "description": """Get documentation for professional shape libraries.

IMPORTANT: Call this BEFORE generating cloud architecture diagrams!

AVAILABLE LIBRARIES:
- aws4: AWS 2025 icons (EC2, S3, Lambda, RDS, etc.) - 1000+ services
- azure2: Microsoft Azure 2.0 shapes
- gcp2: Google Cloud Platform 2.0 icons
- kubernetes: Kubernetes symbols (Pod, Service, Deployment, etc.)
- cisco19: Cisco networking equipment
- flowchart: Standard flowchart shapes

WORKFLOW:
1. Call get_shape_library("aws4") to get AWS documentation
2. Study the shape names and styles
3. Use exact shape names in your mxCell style attribute
   Example: style="shape=mxgraph.aws4.ec2;fillColor=#FF9900;"

EXAMPLE:
For AWS diagram, first call: get_shape_library("aws4")
Then use shapes like:
- style="shape=mxgraph.aws4.ec2" for EC2 instances
- style="shape=mxgraph.aws4.s3" for S3 buckets
- style="shape=mxgraph.aws4.lambda_function" for Lambda""",
                    "parameters": GetShapeLibraryInput.model_json_schema()
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "append_diagram",
                    "description": """Append additional mxCell elements to the current diagram.

Use this when your response was truncated and you need to continue adding elements.

This tool automatically appends to the existing diagram without requiring you to regenerate everything.

EXAMPLE:
If you generated 5 shapes but got cut off, use this to add the remaining shapes:
{
  "xml": "<mxCell id=\\"6\\" value=\\"Queue\\" vertex=\\"1\\" parent=\\"1\\"><mxGeometry x=\\"400\\" y=\\"200\\" width=\\"80\\" height=\\"40\\"/></mxCell>..."
}

IMPORTANT: Ensure new cell IDs don't conflict with existing ones.""",
                    "parameters": AppendDiagramInput.model_json_schema()
                }
            }
        ]
    
    def execute_display_diagram(self, xml: str) -> Dict:
        """
        Execute display_diagram tool
        
        Args:
            xml: mxCell elements (no wrappers)
            
        Returns:
            Result dictionary with complete XML
        """
        try:
            # Validate and fix the XML
            validated_xml = validate_and_fix_xml(xml)
            
            # Wrap in complete draw.io structure
            complete_xml = wrap_mxfile(validated_xml)
            
            # Store current diagram
            self.current_diagram_xml = complete_xml
            
            return {
                "success": True,
                "xml": complete_xml,
                "message": "Diagram created successfully"
            }
            
        except XMLValidationError as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"XML validation failed: {str(e)}"
            }
    
    def execute_edit_diagram(
        self,
        operations: List[Dict],
        current_xml: Optional[str] = None
    ) -> Dict:
        """
        Execute edit_diagram tool
        
        Args:
            operations: List of edit operations
            current_xml: Current diagram XML (uses stored if None)
            
        Returns:
            Result dictionary with updated XML
        """
        try:
            # Use provided XML or stored diagram
            xml_to_edit = current_xml or self.current_diagram_xml
            
            if not xml_to_edit:
                return {
                    "success": False,
                    "error": "No current diagram to edit",
                    "message": "Use display_diagram first to create a diagram"
                }
            
            # Apply each operation
            result_xml = xml_to_edit
            for op in operations:
                result_xml = apply_edit_operation(
                    current_xml=result_xml,
                    operation=op["operation"],
                    cell_id=op["cell_id"],
                    new_xml=op.get("new_xml")
                )
            
            # Update stored diagram
            self.current_diagram_xml = result_xml
            
            return {
                "success": True,
                "xml": result_xml,
                "message": f"Applied {len(operations)} operation(s) successfully"
            }
            
        except XMLValidationError as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Edit operation failed: {str(e)}"
            }
    
    def execute_get_shape_library(self, library: str) -> Dict:
        """
        Execute get_shape_library tool
        
        Args:
            library: Library name (e.g., "aws4", "kubernetes")
            
        Returns:
            Result dictionary with library documentation
        """
        try:
            # Sanitize library name
            from ai_providers.security import sanitize_library_name
            safe_library = sanitize_library_name(library)
            
            # Construct file path
            library_file = os.path.join(
                self.shape_library_path,
                f"{safe_library}.md"
            )
            
            # Read library documentation
            if not os.path.exists(library_file):
                return {
                    "success": False,
                    "error": f"Library '{library}' not found",
                    "message": f"Available libraries: aws4, azure2, gcp2, kubernetes, cisco19, flowchart",
                    "content": ""
                }
            
            with open(library_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "success": True,
                "library": safe_library,
                "content": content,
                "message": f"Loaded {safe_library} library documentation"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to load library: {str(e)}",
                "content": ""
            }
    
    def execute_append_diagram(
        self,
        xml: str,
        current_xml: Optional[str] = None
    ) -> Dict:
        """
        Execute append_diagram tool
        
        Args:
            xml: Additional mxCell elements to append
            current_xml: Current diagram XML (uses stored if None)
            
        Returns:
            Result dictionary with updated XML
        """
        try:
            # Use provided XML or stored diagram
            base_xml = current_xml or self.current_diagram_xml
            
            if not base_xml:
                return {
                    "success": False,
                    "error": "No current diagram to append to",
                    "message": "Use display_diagram first to create a diagram"
                }
            
            # Validate new XML
            validated_xml = validate_and_fix_xml(xml)
            
            # Extract existing mxCells and append new ones
            from .xml_utils import extract_mxcells
            existing_cells = extract_mxcells(base_xml)
            combined_cells = existing_cells + "\n" + validated_xml
            
            # Wrap in complete structure
            complete_xml = wrap_mxfile(combined_cells)
            
            # Update stored diagram
            self.current_diagram_xml = complete_xml
            
            return {
                "success": True,
                "xml": complete_xml,
                "message": "Successfully appended elements to diagram"
            }
            
        except XMLValidationError as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Append operation failed: {str(e)}"
            }
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """
        Execute a tool by name
        
        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        if tool_name == "display_diagram":
            return self.execute_display_diagram(arguments["xml"])
        
        elif tool_name == "edit_diagram":
            return self.execute_edit_diagram(arguments["operations"])
        
        elif tool_name == "get_shape_library":
            return self.execute_get_shape_library(arguments["library"])
        
        elif tool_name == "append_diagram":
            return self.execute_append_diagram(arguments["xml"])
        
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "message": "Available tools: display_diagram, edit_diagram, get_shape_library, append_diagram"
            }
