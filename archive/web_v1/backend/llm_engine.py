import os
from openai import OpenAI
import re

class LLMEngine:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )

    def generate_xml(self, prompt: str) -> str:
        print(f"DEBUG: Generating XML for prompt: {prompt}")
        system_prompt = self._get_system_prompt()
        
        try:
            print("DEBUG: Calling NVIDIA NIM API...")
            response = self.client.chat.completions.create(
                model="meta/llama-3.1-70b-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                top_p=0.7,
                max_tokens=4096,
            )
            print("DEBUG: API Response received.")
        except Exception as e:
            print(f"ERROR: API Call failed: {e}")
            raise e
        
        content = response.choices[0].message.content
        print(f"DEBUG: Raw content length: {len(content)}")
        return self._extract_xml(content)

    def _extract_xml(self, content: str) -> str:
        # Extract XML block
        match = re.search(r'```xml\n(.*?)\n```', content, re.DOTALL)
        if match:
            return match.group(1)
        
        # Fallback: try to find <mxGraphModel>...</mxGraphModel>
        match = re.search(r'(<mxGraphModel.*?</mxGraphModel>)', content, re.DOTALL)
        if match:
            return match.group(1)
            
        return content

    def _get_system_prompt(self) -> str:
        return """You are an expert System Design Architect.
Your goal is to generate a Draw.io XML diagram (mxGraphModel) based on the user's description.

### Output Format
Return ONLY the raw XML string inside a ```xml block.
The root element must be `<mxGraphModel>`.
Do NOT include the `<?xml ...?>` header or `<mxfile>` wrapper.

### XML Structure
```xml
<mxGraphModel dx="1000" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" background="#ffffff">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    
    <!-- Nodes -->
    <mxCell id="unique_id_1" value="Label" style="style_string" parent="1" vertex="1">
      <mxGeometry x="100" y="100" width="60" height="60" as="geometry"/>
    </mxCell>
    
    <!-- Edges -->
    <mxCell id="edge_1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" parent="1" source="unique_id_1" target="unique_id_2" edge="1">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

### Style Library (AWS)
Use these exact style strings for components:

1. **Generic Server / Compute**: 
   `style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"`

2. **Database**: 
   `style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.database;fillColor=none;strokeColor=#3334B9;fontColor=#3334B9;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"`

3. **S3 Bucket / Storage**:
   `style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;fillColor=none;strokeColor=#248814;fontColor=#248814;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"`

4. **User / Client**:
   `style="shape=mxgraph.aws4.users;fillColor=#232F3E;strokeColor=none;fontColor=#232F3E;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"`

5. **Load Balancer / ELB**:
   `style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;fillColor=none;strokeColor=#D86613;fontColor=#D86613;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"`

6. **Internet Gateway**:
   `style="shape=mxgraph.aws4.internet_alt2;fillColor=#232F3E;strokeColor=none;fontColor=#232F3E;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"`

7. **ECS / Container**:
   `style="shape=mxgraph.aws4.ecs_service;fillColor=#D05C17;strokeColor=none;fontColor=#D05C17;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"`

8. **Lambda / Function**:
   `style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;fillColor=none;strokeColor=#D86613;fontColor=#D86613;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"`

### Layout Rules
- Place nodes in a logical flow (e.g., Left -> Right or Top -> Bottom).
- Use `x` and `y` coordinates to space them out.
- Start at x=100, y=100. Increment x by 200 for each step in the flow.
- If there are parallel components (e.g., 3 servers), stack them vertically (increment y by 100).
- **CRITICAL**: Ensure `width` and `height` are set (usually 60x60 or 40x40).

### Example Prompt: "A user connects to a Load Balancer which distributes traffic to 2 Web Servers."
### Example Output:
```xml
<mxGraphModel dx="1000" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" background="#ffffff">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    
    <mxCell id="user" value="User" style="shape=mxgraph.aws4.users;fillColor=#232F3E;strokeColor=none;fontColor=#232F3E;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;" parent="1" vertex="1">
      <mxGeometry x="100" y="200" width="40" height="40" as="geometry"/>
    </mxCell>
    
    <mxCell id="lb" value="Load Balancer" style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elastic_load_balancing;fillColor=none;strokeColor=#D86613;fontColor=#D86613;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;" parent="1" vertex="1">
      <mxGeometry x="300" y="200" width="60" height="60" as="geometry"/>
    </mxCell>
    
    <mxCell id="web1" value="Web Server 1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" parent="1" vertex="1">
      <mxGeometry x="500" y="150" width="80" height="40" as="geometry"/>
    </mxCell>
    
    <mxCell id="web2" value="Web Server 2" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" parent="1" vertex="1">
      <mxGeometry x="500" y="250" width="80" height="40" as="geometry"/>
    </mxCell>
    
    <mxCell id="e1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" parent="1" source="user" target="lb" edge="1">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    
    <mxCell id="e2" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" parent="1" source="lb" target="web1" edge="1">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    
    <mxCell id="e3" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" parent="1" source="lb" target="web2" edge="1">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```
"""
