"""
Tool-based architecture for Arcgen AI diagram generation
Inspired by next-ai-draw-io's sophisticated tool system
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class ToolParameter(BaseModel):
    """Base class for tool parameters"""
    pass


class DisplayDiagramParams(ToolParameter):
    """Parameters for display_diagram tool"""
    xml: str


class DiagramOperation(BaseModel):
    """Single diagram edit operation"""
    operation: str  # "update", "add", or "delete"
    cell_id: str
    new_xml: Optional[str] = None  # Required for update/add, optional for delete


class EditDiagramParams(ToolParameter):
    """Parameters for edit_diagram tool"""
    operations: List[DiagramOperation]


class AppendDiagramParams(ToolParameter):
    """Parameters for append_diagram tool"""
    xml: str


class GetShapeLibraryParams(ToolParameter):
    """Parameters for get_shape_library tool"""
    library: str


class Tool:
    """Represents a tool that the AI can call"""

    def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }


# Available tools
TOOLS = [
    Tool(
        name="display_diagram",
        description="Display a NEW diagram on draw.io. Use this when creating a diagram from scratch or when major structural changes are needed.",
        parameters={
            "type": "object",
            "properties": {
                "xml": {
                    "type": "string",
                    "description": "The complete draw.io XML for the diagram"
                }
            },
            "required": ["xml"]
        }
    ),
    Tool(
        name="edit_diagram",
        description="""Edit the current diagram by ID-based operations (update/add/delete cells).

Operations:
- update: Replace an existing cell by its id. Provide cell_id and complete new_xml.
- add: Add a new cell. Provide cell_id (new unique id) and new_xml.
- delete: Remove a cell by its id. Only cell_id is needed.

For update/add, new_xml must be a complete mxCell element including mxGeometry.

⚠️ JSON ESCAPING: Every " inside new_xml MUST be escaped as \\". Example: id=\\"5\\" value=\\"Label\\"

Example - Add a rectangle:
{"operations": [{"operation": "add", "cell_id": "rect-1", "new_xml": "<mxCell id=\\"rect-1\\" value=\\"Hello\\" style=\\"rounded=0;\\" vertex=\\"1\\" parent=\\"1\\"><mxGeometry x=\\"100\\" y=\\"100\\" width=\\"120\\" height=\\"60\\" as=\\"geometry\\"/></mxCell>"}]}

Example - Delete a cell:
{"operations": [{"operation": "delete", "cell_id": "rect-1"}]}""",
        parameters={
            "type": "object",
            "properties": {
                "operations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["update", "add", "delete"],
                                "description": "Operation to perform: add, update, or delete"
                            },
                            "cell_id": {
                                "type": "string",
                                "description": "The id of the mxCell. Must match the id attribute in new_xml."
                            },
                            "new_xml": {
                                "type": "string",
                                "description": "Complete mxCell XML element (required for update/add)"
                            }
                        },
                        "required": ["operation", "cell_id"]
                    },
                    "description": "Array of operations to apply to the diagram"
                }
            },
            "required": ["operations"]
        }
    ),
    Tool(
        name="append_diagram",
        description="Continue generating diagram XML when display_diagram was truncated due to output length limits. Only use this after display_diagram truncation.",
        parameters={
            "type": "object",
            "properties": {
                "xml": {
                    "type": "string",
                    "description": "Continuation fragment of XML (NO wrapper tags like <mxGraphModel> or <root>)"
                }
            },
            "required": ["xml"]
        }
    ),
    Tool(
        name="get_shape_library",
        description="Get shape/icon library documentation. Use this to discover available icon shapes (AWS, Azure, GCP, Kubernetes, etc.) before creating diagrams with cloud/tech icons.",
        parameters={
            "type": "object",
            "properties": {
                "library": {
                    "type": "string",
                    "description": "Library name: aws4, azure2, gcp2, kubernetes, cisco19, flowchart, bpmn, etc."
                }
            },
            "required": ["library"]
        }
    )
]


def get_tools() -> List[Tool]:
    """Get all available tools"""
    return TOOLS


def get_tools_for_ai(provider: str = "openai") -> List[Dict[str, Any]]:
    """Get tools formatted for AI consumption"""
    if provider in ["openai", "nvidia", "azure"]:
        # OpenAI-style tool format
        return [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        } for tool in TOOLS]
    elif provider == "anthropic":
        # Anthropic-style tool format
        return [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.parameters
        } for tool in TOOLS]
    else:
        # Default to OpenAI format
        return [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        } for tool in TOOLS]


def validate_tool_call(tool_name: str, tool_args: Dict[str, Any]) -> Optional[ToolParameter]:
    """Validate and parse tool call arguments"""
    tool = next((t for t in TOOLS if t.name == tool_name), None)
    if not tool:
        return None

    try:
        if tool_name == "display_diagram":
            return DisplayDiagramParams(**tool_args)
        elif tool_name == "edit_diagram":
            return EditDiagramParams(**tool_args)
        elif tool_name == "append_diagram":
            return AppendDiagramParams(**tool_args)
        elif tool_name == "get_shape_library":
            return GetShapeLibraryParams(**tool_args)
    except Exception:
        return None

    return None


class ShapeLibraryManager:
    """Manages access to draw.io shape libraries"""

    # Shape libraries with their available shapes and usage syntax
    LIBRARIES = {
        "aws4": {
            "name": "AWS 4.0",
            "description": "Amazon Web Services icons and shapes (1000+ services)",
            "prefix": "mxgraph.aws4",
            "usage": """For resource icons:
<mxCell value="label" style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{shape};fillColor=#ED7100;strokeColor=#ffffff;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry" />
</mxCell>

For simple shapes:
<mxCell value="label" style="shape=mxgraph.aws4.{shape};fillColor=#232F3D;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry" />
</mxCell>""",
            "common_shapes": [
                "ec2", "s3", "lambda_function", "rds", "vpc", "cloudfront",
                "api_gateway", "dynamodb", "sns", "sqs", "kinesis", "redshift",
                "emr", "glue", "athena", "sagemaker", "cloudwatch", "iam",
                "route_53", "elb", "cloudformation", "elastic_beanstalk"
            ],
            "categories": ["compute", "storage", "database", "networking", "security", "analytics", "ml", "integration"]
        },
        "azure2": {
            "name": "Azure 2.0",
            "description": "Microsoft Azure cloud services",
            "prefix": "mxgraph.azure2",
            "usage": """Use shape='mxgraph.azure2.{service_name}' in your XML

Example:
<mxCell value="VM" style="shape=mxgraph.azure2.virtual_machine;fillColor=#0078D4;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry" />
</mxCell>""",
            "common_shapes": [
                "virtual_machine", "storage_account", "function_app", "cosmos_db",
                "sql_database", "app_service", "kubernetes_service", "service_bus",
                "event_grid", "key_vault", "monitor", "api_management",
                "logic_apps", "data_factory", "cognitive_services"
            ],
            "categories": ["compute", "storage", "database", "ai", "integration", "security", "networking"]
        },
        "gcp2": {
            "name": "Google Cloud Platform 2.0",
            "description": "Google Cloud Platform services",
            "prefix": "mxgraph.gcp2",
            "usage": """Use shape='mxgraph.gcp2.{service_name}' in your XML

Example:
<mxCell value="Cloud Storage" style="shape=mxgraph.gcp2.cloud_storage;fillColor=#4285F4;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry" />
</mxCell>""",
            "common_shapes": [
                "compute_engine", "cloud_storage", "cloud_functions", "cloud_sql",
                "bigquery", "pubsub", "dataflow", "dataproc", "kubernetes_engine",
                "cloud_run", "app_engine", "cloud_build", "vertex_ai", "cloud_spanner"
            ],
            "categories": ["compute", "storage", "database", "analytics", "ml", "containers", "networking"]
        },
        "kubernetes": {
            "name": "Kubernetes",
            "description": "Kubernetes orchestration components",
            "prefix": "mxgraph.kubernetes",
            "usage": """Use shape='mxgraph.kubernetes.{component}' in your XML

Example:
<mxCell value="Pod" style="shape=mxgraph.kubernetes.pod;fillColor=#326CE5;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry" />
</mxCell>""",
            "common_shapes": [
                "pod", "service", "deployment", "configmap", "secret", "ingress",
                "persistent_volume", "persistent_volume_claim", "node", "cluster",
                "namespace", "job", "cronjob", "daemonset", "statefulset"
            ],
            "categories": ["workloads", "networking", "storage", "config", "cluster"]
        },
        "cisco19": {
            "name": "Cisco 19",
            "description": "Cisco networking equipment and icons",
            "prefix": "mxgraph.cisco19",
            "usage": """Use shape='mxgraph.cisco19.{device}' in your XML

Example:
<mxCell value="Router" style="shape=mxgraph.cisco19.router;fillColor=#1BA1E2;" vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="60" height="60" as="geometry" />
</mxCell>""",
            "common_shapes": [
                "router", "switch", "firewall", "load_balancer", "vpn_gateway",
                "wireless_access_point", "server", "workstation", "laptop",
                "cloud", "internet", "network_segment", "hub", "bridge"
            ],
            "categories": ["networking", "security", "servers", "endpoints"]
        },
        "flowchart": {
            "name": "Flowchart",
            "description": "Standard flowchart symbols",
            "prefix": "flowchart",
            "usage": """Use standard shape names. No prefix needed.

Examples:
- shape=rectangle (process)
- shape=diamond (decision)
- shape=ellipse (start/end)
- shape=parallelogram (input/output)""",
            "common_shapes": [
                "process", "decision", "start", "end", "input", "output",
                "document", "database", "connector", "delay", "display", "manual_operation"
            ],
            "categories": ["basic", "input_output", "decisions", "connectors"]
        }
    }

    @staticmethod
    def get_library_info(library: str) -> Optional[Dict[str, Any]]:
        """Get information about a shape library"""
        return ShapeLibraryManager.LIBRARIES.get(library.lower())

    @staticmethod
    def list_available_libraries() -> List[str]:
        """List all available shape libraries"""
        return list(ShapeLibraryManager.LIBRARIES.keys())


# Global shape library manager
shape_library_manager = ShapeLibraryManager()
