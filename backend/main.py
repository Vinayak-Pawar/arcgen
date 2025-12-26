import os
from typing import Optional
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import asyncio
import json
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from ai_providers import get_ai_provider_manager, ClientOverrides, Provider
from diagram_history import get_history_manager
from file_processor import get_file_processor
from datetime import datetime
from typing import List, Dict
from fastapi import UploadFile, File
import json
from fastapi import UploadFile, File
import os

# Global diagram history storage (in production, use database)
diagram_history: Dict[str, List[Dict]] = {}

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_csv_format(csv_content: str) -> bool:
    """
    Validate that the CSV content has the proper draw.io format
    """
    if not csv_content or not csv_content.strip():
        return False

    lines = csv_content.strip().split('\n')

    # Need at least headers + one data row
    if len(lines) < 5:
        return False

    # Check for required headers
    required_headers = [
        "## Label:",
        "## Style:",
        "## Connect:",
        "id,label,shape,edge_target"
    ]

    header_count = 0
    for line in lines[:4]:  # Check first 4 lines for headers
        line = line.strip()
        if any(header in line for header in required_headers):
            header_count += 1

    # Should have at least 3 of the 4 required headers
    if header_count < 3:
        return False

    # Check for data rows (should have at least one row with comma-separated values)
    data_rows = [line for line in lines if line.strip() and not line.startswith('##') and ',' in line]
    if len(data_rows) < 1:
        return False

    # Validate that data rows have proper format (id should be numeric)
    for row in data_rows[:3]:  # Check first few data rows
        parts = row.split(',')
        if len(parts) >= 4:  # Should have at least 4 columns
            try:
                int(parts[0].strip())  # First column should be numeric ID
                return True
            except ValueError:
                continue

    return False

async def generate_diagram_with_tools(prompt: str, config) -> str:
    """
    Generate diagrams using a tool-based architecture inspired by next-ai-draw-io.
    Allows incremental editing, shape library access, and professional diagram creation.
    """
    # Initialize current diagram state
    current_xml = ""

    # Tool definitions for the AI
    tool_prompt = f"""
You are an expert diagram creation assistant specializing in draw.io XML generation.
Your primary function is to create clear, well-organized visual diagrams through precise XML specifications.

## Available Tools

### display_diagram
**Purpose**: Display a NEW diagram on draw.io. Use this when creating a diagram from scratch or when major structural changes are needed.
**Parameters**: xml (string) - Complete draw.io XML for the diagram
**Usage**: Call this tool to show a new diagram to the user.

### edit_diagram
**Purpose**: Edit specific parts of the EXISTING diagram. Use this when making small targeted changes like adding/removing elements, changing labels, or adjusting properties. This is more efficient than regenerating the entire diagram.
**Parameters**: edits (Array of objects) - Each edit has: operation ("update", "add", "delete"), cell_id (string), new_xml (string for update/add)
**Usage**: Use this for incremental changes to existing diagrams.

### get_shape_library
**Purpose**: Get shape/icon library documentation. Use this to discover available icon shapes (AWS, Azure, GCP, Kubernetes, etc.) before creating diagrams with cloud/tech icons.
**Parameters**: library (string) - Library name: aws4, azure2, gcp2, kubernetes, cisco19, flowchart, bpmn, etc.
**Usage**: Call this FIRST when creating cloud architecture or technical diagrams.

## Critical Rules
1. **Choose the right tool**: Use display_diagram for new diagrams, edit_diagram for modifications
2. **Shape libraries**: Always call get_shape_library first for cloud/tech diagrams
3. **Incremental editing**: Prefer edit_diagram over regenerating entire diagrams
4. **Layout constraints**: Keep all elements within viewport (x: 0-800, y: 0-600)
5. **XML only via tools**: Never return raw XML in responses - always use tool calls

## Current Diagram State
{current_xml if current_xml else "No diagram currently exists - use display_diagram to create one"}

## User Request
{prompt}

Generate the diagram using the appropriate tools. Start by planning your approach, then use the tools to create or modify the diagram.
"""

    try:
        # For now, use the existing approach but with enhanced prompting
        # TODO: Implement full tool calling architecture with proper tool execution
        xml_prompt = f"""You are a draw.io diagram expert. Generate a diagram in draw.io XML format.

CRITICAL: Generate ONLY the mxCell elements - NO wrapper tags, NO explanations, NO markdown.

XML STRUCTURE:
- Generate ONLY mxCell elements (shapes and connectors)
- Do NOT include <mxfile>, <mxGraphModel>, <root>, or any wrapper tags
- Start IDs from "2" (1 is reserved for root)
- Use parent="1" for all elements
- Use vertex="1" for shapes, edge="1" for connectors

SHAPE EXAMPLES:
<mxCell id="2" value="User" style="ellipse;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="80" height="40" as="geometry"/>
</mxCell>

<mxCell id="3" value="Web Server" style="rectangle;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="160" y="40" width="120" height="60" as="geometry"/>
</mxCell>

CONNECTOR EXAMPLE:
<mxCell id="4" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

PROFESSIONAL SHAPES (use these for better diagrams):
- AWS: style="shape=mxgraph.aws4.ec2;..." (EC2 instances)
- Azure: style="shape=mxgraph.azure2.vm;..." (Virtual Machines)
- GCP: style="shape=mxgraph.gcp2.compute_engine;..." (Compute Engine)
- Database: style="shape=cylinder;..." or style="shape=mxgraph.azure2.database;..."
- Cloud: style="shape=cloud;..."

POSITIONING RULES:
- Start shapes at x=40, y=40, spacing 120px apart
- Width=80-120, Height=40-60 for shapes
- Use relative="1" for connector geometry
- Keep within viewport bounds (x: 0-800, y: 0-600)

Generate diagram XML for: {prompt}"""

        # Generate XML using AI provider
        xml_content = await get_ai_provider_manager().generate_diagram(xml_prompt, config)

        # Clean up the response to extract only XML
        xml_content = extract_xml_from_response(xml_content)

        # Save to history before returning
        save_diagram_version("default", xml_content, f"Generated diagram for: {prompt[:50]}...")

        return xml_content

    except Exception as e:
        print(f"Tool-based generation failed: {e}")
        # Fallback to direct generation
        fallback_prompt = f"""Generate a simple draw.io XML diagram for: {prompt}

Return ONLY the XML content without any explanations or markdown.

Example format:
<mxCell id="2" value="Component" style="rectangle;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="80" height="40" as="geometry"/>
</mxCell>"""

        xml_content = await get_ai_provider_manager().generate_diagram(fallback_prompt, config)

        # Save fallback result to history
        save_diagram_version("default", xml_content, f"Fallback generation for: {prompt[:50]}...")

        return extract_xml_from_response(xml_content)

def save_diagram_version(session_id: str, xml_content: str, description: str):
    """Save a diagram version to history"""
    if session_id not in diagram_history:
        diagram_history[session_id] = []

    diagram_history[session_id].append({
        "timestamp": datetime.now().isoformat(),
        "xml": xml_content,
        "description": description,
        "version": len(diagram_history[session_id]) + 1
    })

    # Keep only last 20 versions to prevent memory issues
    if len(diagram_history[session_id]) > 20:
        diagram_history[session_id] = diagram_history[session_id][-20:]

def extract_xml_from_response(response: str) -> str:
    """Extract XML content from AI response, handling various formats"""
    # Remove markdown code blocks if present
    if "```xml" in response:
        start = response.find("```xml") + 6
        end = response.find("```", start)
        if end > start:
            return response[start:end].strip()

    if "```" in response:
        start = response.find("```") + 3
        end = response.find("```", start)
        if end > start:
            return response[start:end].strip()

    # If no code blocks, try to find XML tags
    if "<mxCell" in response:
        # Extract from first mxCell to last
        start = response.find("<mxCell")
        # Find the last </mxCell> or </mxCell> tag
        last_cell_end = response.rfind("</mxCell>")
        if last_cell_end > start:
            return response[start:last_cell_end + 9].strip()

    # Fallback: return the whole response if it looks like XML
    if response.strip().startswith("<") and ">" in response:
        return response.strip()

    # Last resort: return as-is
    return response.strip()

def get_shape_library_docs(library_name: str) -> str:
    """
    Get documentation for professional shape libraries (AWS, Azure, GCP, etc.)
    """
    libraries = {
        "aws4": """
AWS4 Shape Library - Professional AWS Icons:

CORE SERVICES:
- EC2: style="shape=mxgraph.aws4.ec2;fillColor=#F58536;strokeColor=#232F3E;"
- S3: style="shape=mxgraph.aws4.s3;fillColor=#F58536;strokeColor=#232F3E;"
- Lambda: style="shape=mxgraph.aws4.lambda;fillColor=#F58536;strokeColor=#232F3E;"
- RDS: style="shape=mxgraph.aws4.rds;fillColor=#F58536;strokeColor=#232F3E;"
- VPC: style="shape=mxgraph.aws4.vpc;fillColor=#F58536;strokeColor=#232F3E;"
- API Gateway: style="shape=mxgraph.aws4.api_gateway;fillColor=#F58536;strokeColor=#232F3E;"

COMPUTE & CONTAINERS:
- ECS: style="shape=mxgraph.aws4.ecs;fillColor=#F58536;strokeColor=#232F3E;"
- EKS: style="shape=mxgraph.aws4.eks;fillColor=#F58536;strokeColor=#232F3E;"
- Fargate: style="shape=mxgraph.aws4.fargate;fillColor=#F58536;strokeColor=#232F3E;"

ANALYTICS:
- Kinesis: style="shape=mxgraph.aws4.kinesis;fillColor=#F58536;strokeColor=#232F3E;"
- Glue: style="shape=mxgraph.aws4.glue;fillColor=#F58536;strokeColor=#232F3E;"

Example: <mxCell value="EC2 Instance" style="shape=mxgraph.aws4.ec2;fillColor=#F58536;strokeColor=#232F3E;" vertex="1" parent="1">
""",

        "azure2": """
Azure2 Shape Library - Professional Azure Icons:

COMPUTE:
- VM: style="shape=mxgraph.azure2.vm;fillColor=#0078D4;strokeColor=#005BA1;"
- App Service: style="shape=mxgraph.azure2.app_service;fillColor=#0078D4;strokeColor=#005BA1;"
- Functions: style="shape=mxgraph.azure2.functions;fillColor=#0078D4;strokeColor=#005BA1;"
- Container Instances: style="shape=mxgraph.azure2.container_instances;fillColor=#0078D4;strokeColor=#005BA1;"

STORAGE:
- Storage Account: style="shape=mxgraph.azure2.storage_account;fillColor=#0078D4;strokeColor=#005BA1;"
- Blob Storage: style="shape=mxgraph.azure2.blob_storage;fillColor=#0078D4;strokeColor=#005BA1;"

DATABASES:
- SQL Database: style="shape=mxgraph.azure2.sql_database;fillColor=#0078D4;strokeColor=#005BA1;"
- Cosmos DB: style="shape=mxgraph.azure2.cosmos_db;fillColor=#0078D4;strokeColor=#005BA1;"

NETWORKING:
- Virtual Network: style="shape=mxgraph.azure2.virtual_network;fillColor=#0078D4;strokeColor=#005BA1;"
- Load Balancer: style="shape=mxgraph.azure2.load_balancer;fillColor=#0078D4;strokeColor=#005BA1;"

Example: <mxCell value="Azure VM" style="shape=mxgraph.azure2.vm;fillColor=#0078D4;strokeColor=#005BA1;" vertex="1" parent="1">
""",

        "gcp2": """
GCP2 Shape Library - Professional Google Cloud Icons:

COMPUTE:
- Compute Engine: style="shape=mxgraph.gcp2.compute_engine;fillColor=#4285F4;strokeColor=#3367D6;"
- App Engine: style="shape=mxgraph.gcp2.app_engine;fillColor=#4285F4;strokeColor=#3367D6;"
- Cloud Functions: style="shape=mxgraph.gcp2.cloud_functions;fillColor=#4285F4;strokeColor=#3367D6;"

STORAGE:
- Cloud Storage: style="shape=mxgraph.gcp2.cloud_storage;fillColor=#4285F4;strokeColor=#3367D6;"
- BigQuery: style="shape=mxgraph.gcp2.bigquery;fillColor=#4285F4;strokeColor=#3367D6;"

CONTAINERS:
- Kubernetes Engine: style="shape=mxgraph.gcp2.kubernetes_engine;fillColor=#4285F4;strokeColor=#3367D6;"
- Cloud Run: style="shape=mxgraph.gcp2.cloud_run;fillColor=#4285F4;strokeColor=#3367D6;"

AI/ML:
- AI Platform: style="shape=mxgraph.gcp2.ai_platform;fillColor=#4285F4;strokeColor=#3367D6;"
- Vertex AI: style="shape=mxgraph.gcp2.vertex_ai;fillColor=#4285F4;strokeColor=#3367D6;"

Example: <mxCell value="GCE Instance" style="shape=mxgraph.gcp2.compute_engine;fillColor=#4285F4;strokeColor=#3367D6;" vertex="1" parent="1">
""",

        "kubernetes": """
Kubernetes Shape Library - Professional K8s Icons:

CORE COMPONENTS:
- Pod: style="shape=mxgraph.kubernetes.pod;fillColor=#326CE5;strokeColor=#1E4BB8;"
- Deployment: style="shape=mxgraph.kubernetes.deployment;fillColor=#326CE5;strokeColor=#1E4BB8;"
- Service: style="shape=mxgraph.kubernetes.service;fillColor=#326CE5;strokeColor=#1E4BB8;"
- ConfigMap: style="shape=mxgraph.kubernetes.config_map;fillColor=#326CE5;strokeColor=#1E4BB8;"

INFRASTRUCTURE:
- Node: style="shape=mxgraph.kubernetes.node;fillColor=#326CE5;strokeColor=#1E4BB8;"
- Cluster: style="shape=mxgraph.kubernetes.cluster;fillColor=#326CE5;strokeColor=#1E4BB8;"
- Ingress: style="shape=mxgraph.kubernetes.ingress;fillColor=#326CE5;strokeColor=#1E4BB8;"

STORAGE:
- Persistent Volume: style="shape=mxgraph.kubernetes.persistent_volume;fillColor=#326CE5;strokeColor=#1E4BB8;"
- PVC: style="shape=mxgraph.kubernetes.persistent_volume_claim;fillColor=#326CE5;strokeColor=#1E4BB8;"

Example: <mxCell value="Pod" style="shape=mxgraph.kubernetes.pod;fillColor=#326CE5;strokeColor=#1E4BB8;" vertex="1" parent="1">
""",

        "cisco19": """
Cisco19 Shape Library - Professional Networking Icons:

ROUTERS & SWITCHES:
- Router: style="shape=mxgraph.cisco19.router;fillColor=#1BA1E2;strokeColor=#0F7BB4;"
- Switch: style="shape=mxgraph.cisco19.switch;fillColor=#1BA1E2;strokeColor=#0F7BB4;"
- Firewall: style="shape=mxgraph.cisco19.firewall;fillColor=#1BA1E2;strokeColor=#0F7BB4;"

SERVERS:
- Server: style="shape=mxgraph.cisco19.server;fillColor=#1BA1E2;strokeColor=#0F7BB4;"
- Blade Server: style="shape=mxgraph.cisco19.blade_server;fillColor=#1BA1E2;strokeColor=#0F7BB4;"

NETWORK DEVICES:
- Access Point: style="shape=mxgraph.cisco19.access_point;fillColor=#1BA1E2;strokeColor=#0F7BB4;"
- VPN Concentrator: style="shape=mxgraph.cisco19.vpn_concentrator;fillColor=#1BA1E2;strokeColor=#0F7BB4;"

Example: <mxCell value="Cisco Router" style="shape=mxgraph.cisco19.router;fillColor=#1BA1E2;strokeColor=#0F7BB4;" vertex="1" parent="1">
""",

        "flowchart": """
Flowchart Shapes - Standard Flowchart Symbols:

BASIC SHAPES:
- Process: style="shape=process;whiteSpace=wrap;html=1;" (rectangle)
- Decision: style="shape=rhombus;whiteSpace=wrap;html=1;" (diamond)
- Data: style="shape=parallelogram;whiteSpace=wrap;html=1;" (parallelogram)
- Document: style="shape=document;whiteSpace=wrap;html=1;" (document)
- Start/End: style="shape=ellipse;whiteSpace=wrap;html=1;" (circle/oval)

CONNECTORS:
- Arrow: style="endArrow=classic;html=1;"

Example: <mxCell value="Process Step" style="shape=process;whiteSpace=wrap;html=1;" vertex="1" parent="1">
""",

        "bpmn": """
BPMN 2.0 Shape Library - Business Process Modeling:

EVENTS:
- Start Event: style="shape=mxgraph.bpmn.start;fillColor=#48A447;strokeColor=#2D5A2D;"
- End Event: style="shape=mxgraph.bpmn.end;fillColor=#E53E3E;strokeColor=#B91C1C;"
- Timer Event: style="shape=mxgraph.bpmn.timer_start;fillColor=#48A447;strokeColor=#2D5A2D;"

ACTIVITIES:
- Task: style="shape=mxgraph.bpmn.task;fillColor=#FFFFFF;strokeColor=#000000;"
- Subprocess: style="shape=mxgraph.bpmn.subprocess;fillColor=#FFFFFF;strokeColor=#000000;"

GATEWAYS:
- Exclusive Gateway: style="shape=mxgraph.bpmn.gateway;fillColor=#FFFFFF;strokeColor=#000000;"

Example: <mxCell value="Start Process" style="shape=mxgraph.bpmn.start;fillColor=#48A447;strokeColor=#2D5A2D;" vertex="1" parent="1">
"""
    }

    return libraries.get(library_name.lower(), f"Library '{library_name}' not found. Available libraries: {', '.join(libraries.keys())}")

# File processing utilities
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
MAX_EXTRACTED_CHARS = 150000  # 150k chars

async def extract_pdf_text(file: UploadFile) -> str:
    """Extract text content from PDF file"""
    try:
        import PyPDF2
        import io

        content = await file.read()
        pdf_buffer = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_buffer)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        # Limit extracted text length
        if len(text) > MAX_EXTRACTED_CHARS:
            text = text[:MAX_EXTRACTED_CHARS] + "...[truncated]"

        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract PDF text: {str(e)}")

async def extract_text_file_content(file: UploadFile) -> str:
    """Extract content from text-based files"""
    try:
        content = await file.read()
        text = content.decode('utf-8')

        # Limit extracted text length
        if len(text) > MAX_EXTRACTED_CHARS:
            text = text[:MAX_EXTRACTED_CHARS] + "...[truncated]"

        return text
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding not supported. Please use UTF-8 encoded files.")

def is_pdf_file(filename: str) -> bool:
    return filename.lower().endswith('.pdf')

def is_text_file(filename: str) -> bool:
    text_extensions = ['.txt', '.md', '.markdown', '.json', '.csv', '.xml', '.html', '.css', '.js', '.ts', '.py', '.java', '.c', '.cpp', '.yaml', '.yml']
    return any(filename.lower().endswith(ext) for ext in text_extensions)

def validate_xml_format(xml_content: str) -> bool:
    """
    Validate that the XML content has the proper draw.io format
    """
    if not xml_content or not xml_content.strip():
        return False

    content = xml_content.strip()

    # Should not contain wrapper tags (these are added by the frontend)
    if any(tag in content.lower() for tag in ['<mxfile', '<mxgraphmodel', '<root']):
        return False

    # Should contain mxCell elements
    if '<mxcell' not in content.lower():
        return False

    # Should have at least one shape (vertex) and optionally connections
    if 'vertex="1"' not in content:
        return False

    # Check for basic XML structure
    if not content.startswith('<mxCell') and not content.startswith('<mxcell'):
        return False

    return True

class DesignRequest(BaseModel):
    prompt: str
    llm_provider: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_model: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Arcgen Backend is running"}

@app.post("/generate")
async def generate_diagram(request: DesignRequest):
    try:
        # Get AI provider manager
        ai_manager = get_ai_provider_manager()

        # Create client overrides from request (if user specified provider)
        overrides = None
        if hasattr(request, 'llm_provider') and hasattr(request, 'llm_api_key') and hasattr(request, 'llm_model'):
            if request.llm_provider and request.llm_api_key:
                overrides = ClientOverrides(
                    provider=request.llm_provider,
                    api_key=request.llm_api_key,
                    model_id=request.llm_model
                )

        # Get model configuration
        config = ai_manager.get_model_config(overrides)

        # Build XML generation prompt based on next-ai-draw-io approach
        xml_prompt = f"""You are a draw.io diagram expert. Generate a diagram in draw.io XML format.

CRITICAL: Generate ONLY the mxCell elements - NO wrapper tags, NO explanations, NO markdown.

XML STRUCTURE:
- Generate ONLY mxCell elements (shapes and connectors)
- Do NOT include <mxfile>, <mxGraphModel>, <root>, or any wrapper tags
- Start IDs from "2" (1 is reserved for root)
- Use parent="1" for all elements
- Use vertex="1" for shapes, edge="1" for connectors

SHAPE EXAMPLE:
<mxCell id="2" value="User" style="ellipse;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="80" height="40" as="geometry"/>
</mxCell>

CONNECTOR EXAMPLE:
<mxCell id="3" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

POSITIONING:
- Start shapes at x=40, y=40, spacing 120px apart
- Width=80-120, Height=40-60 for shapes
- Use relative="1" for connector geometry

Generate diagram XML for: {request.prompt}"""

        # Use tool-based architecture for diagram generation
        result = await ai_manager.generate_diagram(xml_prompt, config)

        # Handle different result types from tool-based architecture
        if result["type"] == "display_diagram":
            xml_content = result["xml"]
            # Validate XML format
            if not validate_xml_format(xml_content):
                print(f"Invalid XML format generated: {xml_content[:200]}...")
                raise HTTPException(
                    status_code=500,
                    detail="AI model generated invalid diagram format. Please try rephrasing your description."
                )

            return {
                "xml": xml_content.strip(),
                "provider": config.provider.value,
                "model": config.model_id,
                "tool_used": "display_diagram"
            }

        elif result["type"] == "edit_diagram":
            # For now, return the edits - frontend will need to handle this later
            return {
                "edits": result["edits"],
                "provider": config.provider.value,
                "model": config.model_id,
                "tool_used": "edit_diagram",
                "message": "Diagram edits generated - incremental editing not yet implemented"
            }

        elif result["type"] == "shape_library":
            return {
                "library_info": result["info"],
                "library": result["library"],
                "provider": config.provider.value,
                "model": config.model_id,
                "tool_used": "get_shape_library"
            }

        elif result["type"] == "text":
            # Fallback to text response
            return {
                "text_response": result["content"],
                "provider": config.provider.value,
                "model": config.model_id,
                "tool_used": "text_fallback"
            }

        else:
            raise HTTPException(
                status_code=500,
                detail=f"Unknown result type from AI: {result['type']}"
            )

    except Exception as e:

@app.post("/generate-stream")
async def generate_diagram_stream(request: DesignRequest):
    """Generate diagram with streaming response for real-time updates"""
    try:
        # Get AI provider manager
        ai_manager = get_ai_provider_manager()

        # Create client overrides from request (if user specified provider)
        overrides = None
        if hasattr(request, 'llm_provider') and hasattr(request, 'llm_api_key') and hasattr(request, 'llm_model'):
            if request.llm_provider and request.llm_api_key:
                overrides = ClientOverrides(
                    provider=request.llm_provider,
                    api_key=request.llm_api_key,
                    model_id=request.llm_model
                )

        # Get model configuration
        config = ai_manager.get_model_config(overrides)

        # Build XML generation prompt (same as regular endpoint)
        xml_prompt = f"""You are a draw.io diagram expert. Generate a diagram in draw.io XML format.

CRITICAL: Generate ONLY the mxCell elements - NO wrapper tags, NO explanations, NO markdown.

XML STRUCTURE:
- Generate ONLY mxCell elements (shapes and connectors)
- Do NOT include <mxfile>, <mxGraphModel>, <root>, or any wrapper tags
- Start IDs from "2" (1 is reserved for root)
- Use parent="1" for all elements
- Use vertex="1" for shapes, edge="1" for connectors

SHAPE EXAMPLE:
<mxCell id="2" value="User" style="ellipse;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="80" height="40" as="geometry"/>
</mxCell>

CONNECTOR EXAMPLE:
<mxCell id="3" style="endArrow=classic;html=1;rounded=0;" edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

POSITIONING:
- Start shapes at x=40, y=40, spacing 120px apart
- Width=80-120, Height=40-60 for shapes
- Use relative="1" for connector geometry

Generate diagram XML for: {request.prompt}"""

        async def generate_stream():
            try:
                # Send initial status
                yield f"data: {json.dumps({'type': 'status', 'message': 'Starting AI generation...', 'progress': 10})}\n\n"

                # Generate diagram (this might take some time)
                result = await ai_manager.generate_diagram(xml_prompt, config)

                # Send progress update
                yield f"data: {json.dumps({'type': 'status', 'message': 'Processing AI response...', 'progress': 50})}\n\n"

                # Handle different result types
                if result["type"] == "display_diagram":
                    xml_content = result["xml"]
                    # Validate XML format
                    if not validate_xml_format(xml_content):
                        yield f"data: {json.dumps({'type': 'error', 'message': 'AI generated invalid diagram format', 'progress': 100})}\n\n"
                        return

                    # Send final result
                    yield f"data: {json.dumps({\n                        'type': 'complete',\n                        'xml': xml_content.strip(),\n                        'provider': config.provider.value,\n                        'model': config.model_id,\n                        'tool_used': 'display_diagram',\n                        'progress': 100\n                    })}\n\n"

                elif result["type"] == "edit_diagram":
                    yield f"data: {json.dumps({\n                        'type': 'complete',\n                        'edits': result['edits'],\n                        'provider': config.provider.value,\n                        'model': config.model_id,\n                        'tool_used': 'edit_diagram',\n                        'message': 'Diagram edits generated - incremental editing not yet implemented',\n                        'progress': 100\n                    })}\n\n"

                elif result["type"] == "shape_library":
                    yield f"data: {json.dumps({\n                        'type': 'complete',\n                        'library_info': result['info'],\n                        'library': result['library'],\n                        'provider': config.provider.value,\n                        'model': config.model_id,\n                        'tool_used': 'get_shape_library',\n                        'progress': 100\n                    })}\n\n"

                elif result["type"] == "text":
                    yield f"data: {json.dumps({\n                        'type': 'complete',\n                        'text_response': result['content'],\n                        'provider': config.provider.value,\n                        'model': config.model_id,\n                        'tool_used': 'text_fallback',\n                        'progress': 100\n                    })}\n\n"

                else:
                    yield f"data: {json.dumps({'type': 'error', 'message': f'Unknown result type: {result[\"type\"]}', 'progress': 100})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': f'Generation failed: {str(e)}', 'progress': 100})}\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control",
            }
        )

    except Exception as e:
        # Log the error (you might want to add proper logging later)
        print(f"Error generating diagram: {str(e)}")

        # Return user-friendly error
        error_msg = str(e)
        provider_name = config.provider.value.title() if 'config' in locals() else "AI Provider"

        if "API key" in error_msg.lower() or "401" in error_msg or "unauthorized" in error_msg.lower():
            raise HTTPException(
                status_code=401,
                detail=f"Invalid or missing API key for {provider_name}. Please check your API key configuration."
            )
        elif "rate limit" in error_msg.lower() or "429" in error_msg:
            raise HTTPException(status_code=429, detail="API rate limit exceeded. Please wait a moment and try again.")
        elif "timeout" in error_msg.lower():
            raise HTTPException(status_code=408, detail="Request timed out. Please try again.")
        elif "connection" in error_msg.lower():
            raise HTTPException(status_code=503, detail=f"Connection error with {provider_name}. Please check your internet connection and try again.")
        else:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/test-shape-libraries")
async def test_get_shape_libraries():
    """Test endpoint for shape libraries"""
    from tools import shape_library_manager
    libraries = shape_library_manager.list_available_libraries()
    return {"libraries": libraries, "test": True}

@app.get("/shape-libraries")
async def get_shape_libraries():
    """Get available shape libraries for diagram creation"""
    from tools import shape_library_manager
    libraries = shape_library_manager.list_available_libraries()
    return {"libraries": libraries}

@app.get("/shape-libraries/{library_name}")
async def get_shape_library_info(library_name: str):
    """Get detailed information about a specific shape library"""
    from tools import shape_library_manager
    info = shape_library_manager.get_library_info(library_name)
    if not info:
        raise HTTPException(status_code=404, detail=f"Shape library '{library_name}' not found")

    return {
        "library": library_name,
        "info": info
    }

@app.get("/providers")
async def get_providers():
    """Get available LLM providers for frontend configuration"""
    ai_manager = get_ai_provider_manager()
    available_providers = ai_manager.get_available_providers()

    # Convert to the format expected by frontend
    providers_dict = {}
    for p in available_providers:
        providers_dict[p["name"]] = {
            "name": p["name"],
            "default_model": p["default_model"],
            "requires_api_key": p["requires_key"],
            "api_key_env": f"{p['name'].upper()}_API_KEY",
            "description": f"{p['name'].title()} AI provider"
        }

    # Get current configuration
    current_config = ai_manager.get_model_config()

    return {
        "providers": providers_dict,
        "current_provider": current_config.provider.value,
        "current_model": current_config.model_id
    }


@app.get("/shape-library/{library_name}")
async def get_shape_library(library_name: str):
    """Get documentation for professional shape libraries (AWS, Azure, GCP, etc.)"""
    try:
        docs = get_shape_library_docs(library_name)
        return {
            "library": library_name,
            "documentation": docs
        }
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Shape library '{library_name}' not found"
        )

@app.get("/diagram-history/{session_id}")
async def get_diagram_history(session_id: str = "default"):
    """Get diagram history for a session"""
    history = diagram_history.get(session_id, [])
    return {
        "session_id": session_id,
        "versions": history,
        "total_versions": len(history)
    }

@app.post("/diagram-history/{session_id}/restore")
async def restore_diagram_version(session_id: str, request: dict):
    """Restore a specific diagram version"""
    version = request.get("version")
    history = diagram_history.get(session_id, [])

    if not version or not isinstance(version, int):
        raise HTTPException(status_code=400, detail="Version number required")

    # Find the version
    version_data = None
    for item in history:
        if item["version"] == version:
            version_data = item
            break

    if not version_data:
        raise HTTPException(status_code=404, detail=f"Version {version} not found")

    return {
        "xml": version_data["xml"],
        "description": version_data["description"],
        "timestamp": version_data["timestamp"],
        "version": version_data["version"]
    }

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process files (PDFs, text files, images)"""
    try:
        # Validate file size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB")

        # Reset file pointer
        await file.seek(0)

        filename = file.filename or "uploaded_file"

        if is_pdf_file(filename):
            # Extract text from PDF
            extracted_text = await extract_pdf_text(file)
            return {
                "filename": filename,
                "file_type": "pdf",
                "extracted_text": extracted_text,
                "char_count": len(extracted_text),
                "message": f"Successfully extracted {len(extracted_text)} characters from PDF"
            }

        elif is_text_file(filename):
            # Extract content from text file
            extracted_text = await extract_text_file_content(file)
            return {
                "filename": filename,
                "file_type": "text",
                "extracted_text": extracted_text,
                "char_count": len(extracted_text),
                "message": f"Successfully loaded {len(extracted_text)} characters from text file"
            }

        else:
            # For images and other files, return basic info
            return {
                "filename": filename,
                "file_type": "other",
                "file_size": len(file_content),
                "message": f"File uploaded successfully. Size: {len(file_content)} bytes"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@app.post("/analyze-file")
async def analyze_file_with_ai(
    file: UploadFile = File(...),
    prompt: str = "Analyze this file and generate a system architecture diagram based on its content."
):
    """Upload a file and generate a diagram based on its content"""
    try:
        # First upload and extract content
        upload_result = await upload_file(file)

        if "extracted_text" not in upload_result:
            raise HTTPException(status_code=400, detail="File type not supported for AI analysis")

        # Combine user prompt with extracted content
        full_prompt = f"{prompt}\n\nFile Content:\n{upload_result['extracted_text']}\n\nFilename: {upload_result['filename']}"

        # Generate diagram using the combined content
        ai_manager = get_ai_provider_manager()
        config = ai_manager.get_model_config()

        xml_content = await generate_diagram_with_tools(full_prompt, config)

        # Validate XML format
        if not validate_xml_format(xml_content):
            raise HTTPException(status_code=500, detail="AI generated invalid diagram format")

        return {
            "xml": xml_content,
            "provider": config.provider.value,
            "model": config.model_id,
            "file_info": upload_result,
            "analysis_prompt": prompt
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")

@app.post("/test-provider")
async def test_provider(request: dict):
    """Test LLM provider configuration"""
    try:
        ai_manager = get_ai_provider_manager()

        # Use current configuration for testing (no overrides for now)
        config = ai_manager.get_model_config()

        # Test with a simple prompt
        test_prompt = "Create a simple diagram with a user connecting to a server."
        result = await ai_manager.generate_diagram(test_prompt, config)

        # Check if we got a valid diagram result
        if result["type"] == "display_diagram" and validate_xml_format(result["xml"]):
            return {
                "success": True,
                "provider": config.provider.value,
                "model": config.model_id,
                "message": "LLM provider is working correctly",
                "sample_output": result["xml"][:200],
                "tool_used": result["type"]
            }
        elif result["type"] in ["edit_diagram", "shape_library", "text"]:
            return {
                "success": True,
                "provider": config.provider.value,
                "model": config.model_id,
                "message": f"LLM provider responded with {result['type']} tool",
                "tool_used": result["type"]
            }
        else:
            return {
                "success": False,
                "provider": config.provider.value,
                "model": config.model_id,
                "error": f"Unexpected result type: {result['type']}",
                "message": "LLM provider returned an unexpected response format."
            }

    except Exception as e:
        config = ai_manager.get_model_config()
        return {
            "success": False,
            "provider": config.provider.value,
            "model": config.model_id,
            "error": str(e),
            "message": f"Failed to connect to {config.provider.value}: {str(e)}"
        }


@app.get("/llm-config")
async def get_llm_config():
    """Get current LLM configuration"""
    ai_manager = get_ai_provider_manager()
    config = ai_manager.get_model_config()

    return {
        "provider": config.provider.value,
        "model": config.model_id,
        "api_key_configured": bool(config.api_key),
        "base_url": config.base_url
    }


@app.post("/llm-config")
async def update_llm_config(request: dict):
    """Update LLM configuration (for future use with persistent storage)"""
    # For now, this just validates the configuration
    # In the future, this could save to a database
    provider = request.get("provider")
    api_key = request.get("api_key")
    model = request.get("model")

    if not provider or not api_key:
        raise HTTPException(status_code=400, detail="Provider and API key are required")

    # Validate the provider
    try:
        provider_enum = Provider(provider)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}")

    # Test the configuration
    ai_manager = get_ai_provider_manager()
    overrides = ClientOverrides(
        provider=provider,
        api_key=api_key,
        model_id=model
    )

    try:
        config = ai_manager.get_model_config(overrides)
        # Test with a simple prompt
        test_prompt = "Test connection."
        await ai_manager.generate_diagram(test_prompt, config)

        return {
            "success": True,
            "message": f"Configuration updated for {provider}",
            "provider": provider,
            "model": model
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Configuration test failed: {str(e)}")


# File Upload Endpoints
@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a file (PDF or image) for diagram generation"""
    try:
        file_processor = get_file_processor()

        # Read file content
        file_content = await file.read()

        # Process the file
        processed_data = file_processor.process_file(file_content, file.filename)

        return {
            "filename": file.filename,
            "content_type": processed_data["content_type"],
            "metadata": processed_data["metadata"],
            "summary": processed_data["summary"],
            "processed": True
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File processing failed: {str(e)}")


@app.post("/generate-from-file")
async def generate_from_file(
    file: UploadFile = File(...),
    llm_provider: Optional[str] = None,
    llm_api_key: Optional[str] = None,
    llm_model: Optional[str] = None
):
    """Upload a file and generate a diagram based on its content"""
    try:
        # Get managers
        file_processor = get_file_processor()
        ai_manager = get_ai_provider_manager()

        # Read and process file
        file_content = await file.read()
        processed_data = file_processor.process_file(file_content, file.filename)

        # Create client overrides if specified
        overrides = None
        if llm_provider and llm_api_key:
            overrides = ClientOverrides(
                provider=llm_provider,
                api_key=llm_api_key,
                model_id=llm_model
            )

        # Get AI configuration
        config = ai_manager.get_model_config(overrides)

        # Create specialized prompt based on file content
        prompt = file_processor.create_file_analysis_prompt(processed_data)

        # Generate XML using AI
        xml_content = await ai_manager.generate_diagram(prompt, config)

        # Validate XML format
        if not validate_xml_format(xml_content):
            print(f"Invalid XML format generated: {xml_content[:200]}...")
            raise HTTPException(
                status_code=500,
                detail="AI model generated invalid diagram format."
            )

        return {
            "xml": xml_content.strip(),
            "filename": file.filename,
            "content_type": processed_data["content_type"],
            "metadata": processed_data["metadata"],
            "provider": config.provider.value,
            "model": config.model_id,
            "prompt_used": prompt[:200] + "..." if len(prompt) > 200 else prompt
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File-based generation failed: {str(e)}")


# Diagram History Endpoints
@app.post("/history/save")
async def save_diagram_version(request: dict):
    """Save a diagram version to history"""
    try:
        history_manager = get_history_manager()

        diagram_id = request.get("diagram_id")
        prompt = request.get("prompt", "")
        xml_content = request.get("xml", "")
        provider = request.get("provider", "unknown")
        model = request.get("model", "unknown")

        if not diagram_id:
            # Create new diagram
            diagram_id = history_manager.create_diagram(prompt, xml_content, provider, model)
        else:
            # Add version to existing diagram
            success = history_manager.add_version(diagram_id, prompt, xml_content, provider, model)
            if not success:
                raise HTTPException(status_code=404, detail="Diagram not found")

        return {"diagram_id": diagram_id, "message": "Diagram saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save diagram: {str(e)}")


@app.get("/history/list")
async def list_diagrams():
    """List all saved diagrams"""
    try:
        history_manager = get_history_manager()
        diagrams = history_manager.list_diagrams()
        return {"diagrams": diagrams}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list diagrams: {str(e)}")


@app.get("/history/{diagram_id}")
async def get_diagram_history(diagram_id: str):
    """Get history for a specific diagram"""
    try:
        history_manager = get_history_manager()
        history = history_manager.get_history(diagram_id)

        if not history:
            raise HTTPException(status_code=404, detail="Diagram not found")

        return {
            "diagram_id": history.diagram_id,
            "created_at": history.created_at.isoformat(),
            "updated_at": history.updated_at.isoformat(),
            "versions": [
                {
                    "id": v.id,
                    "timestamp": v.timestamp.isoformat(),
                    "prompt": v.prompt,
                    "provider": v.provider,
                    "model": v.model,
                    "metadata": v.metadata
                }
                for v in history.versions
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get diagram history: {str(e)}")


@app.get("/history/{diagram_id}/{version_id}")
async def get_diagram_version(diagram_id: str, version_id: str):
    """Get a specific version of a diagram"""
    try:
        history_manager = get_history_manager()
        version = history_manager.get_version(diagram_id, version_id)

        if not version:
            raise HTTPException(status_code=404, detail="Version not found")

        return {
            "version_id": version.id,
            "timestamp": version.timestamp.isoformat(),
            "prompt": version.prompt,
            "xml_content": version.xml_content,
            "provider": version.provider,
            "model": version.model,
            "metadata": version.metadata
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get diagram version: {str(e)}")


@app.delete("/history/{diagram_id}")
async def delete_diagram(diagram_id: str):
    """Delete a diagram and all its versions"""
    try:
        history_manager = get_history_manager()
        success = history_manager.delete_diagram(diagram_id)

        if not success:
            raise HTTPException(status_code=404, detail="Diagram not found")

        return {"message": "Diagram deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete diagram: {str(e)}")


@app.get("/history/stats")
async def get_history_stats():
    """Get diagram history statistics"""
    try:
        history_manager = get_history_manager()
        stats = history_manager.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
