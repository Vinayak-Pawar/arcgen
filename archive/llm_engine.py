import os
# pyrefly: ignore [missing-import]
from openai import OpenAI

class LLMEngine:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")
            
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        # Using Standard Llama 3.1 70B
        self.model = "meta/llama-3.1-70b-instruct"

    def generate_code(self, user_prompt):
        """
        Generates Python code using the diagrams library based on the user prompt.
        """
        system_prompt = """Core Rules
Library Constraint
Use only the diagrams library (https://diagrams.mingrammer.com/).
Do not use any other libraries or modules.
Output Format
Return valid Python code enclosed in markdown backticks.
Example:
```python
... code ...
```
Do not include explanations or comments outside the code block.
The response must be a single, runnable Python script.
Basic Structure
Always define:
from diagrams import Diagram, Cluster

graph_attr = {"rankdir": "LR", "splines": "ortho"}

with Diagram("Architecture", show=False, filename="generated_diagram", graph_attr=graph_attr):
    ...
show=False is mandatory.
filename="generated_diagram" is mandatory.
Imports and Providers
Import only what you actually use.
Common providers and modules:
AWS: diagrams.aws.compute, diagrams.aws.database, diagrams.aws.network, etc.
Azure: diagrams.azure.compute, diagrams.azure.database, etc.
GCP: diagrams.gcp.compute, diagrams.gcp.database, etc.
On-prem:
diagrams.onprem.compute (e.g., Server, Nomad)
diagrams.onprem.database
diagrams.onprem.network (e.g., Nginx, Apache, HAProxy)
diagrams.onprem.monitoring (e.g., Prometheus, Grafana)
diagrams.onprem.client (e.g., User, Client)
Generic:
diagrams.generic.compute (only Rack)
diagrams.generic.database (SQL is HERE. Use: from diagrams.generic.database import SQL)
diagrams.generic.network
diagrams.generic.storage
diagrams.generic.os
diagrams.generic.place
diagrams.generic.device
Programming:
diagrams.programming.language (e.g., Python, NodeJS, Go)
diagrams.programming.framework (e.g., Django, React, Spring)
Negative Constraints (CRITICAL)
When using the diagrams library:
Do NOT import SQL from diagrams.onprem.database (it does not exist).
Use from diagrams.generic.database import SQL.
Do NOT import from diagrams.generic.programming.
Use diagrams.programming.language or diagrams.programming.framework.
Do NOT import from diagrams.generic.monitoring.
Use diagrams.onprem.monitoring instead.
Do NOT import from diagrams.generic.software.
Use diagrams.programming.language or diagrams.programming.framework.
Do NOT import Nginx from diagrams.generic.network.
Use from diagrams.onprem.network import Nginx.
Do NOT import Database from diagrams.generic.database (it does not exist).
Use from diagrams.generic.database import SQL.
Do NOT import Server from diagrams.generic.compute (it does not exist).
Use from diagrams.onprem.compute import Server.
Do NOT import Server from diagrams.generic.compute (it does not exist).
Use from diagrams.onprem.compute import Server.
Do NOT import Client or User from diagrams.generic.network (they do not exist).
Use from diagrams.onprem.client import Client or User.
Do NOT import SQL from diagrams.onprem.database (it does not exist).
Use from diagrams.generic.database import SQL.
AWS naming (case-sensitive):
Use Dynamodb (NOT DynamoDB).
Use Elasticache (NOT ElastiCache).
DocumentDB is correct.
Redshift is correct.
Graph Layout and Grouping
Always define graph_attr = {"rankdir": "LR", "splines": "ortho"}.
Use Cluster to group related components, for example:
"VPC", "Services", "Data Layer", "Messaging", "Monitoring", "CDN Layer", etc.
Prefer a professional, readable structure:
Group databases into a "Data Layer" cluster.
Group microservices into a "Services" or "Microservices" cluster.
Group external users/clients at the left, downstream systems toward the right.
Connections
Use >> to represent data flow or request flow between nodes.
You may chain connections:
user >> api >> service >> db
Ensure all referenced nodes are defined before using them.
Verify variable names match exactly (e.g., if you define `auth_service = ...`, do not use `auth >> ...`).
Do NOT truncate variable names. Use full names or simple, consistent abbreviations.
Inference Rules
If the user does not specify a cloud provider, default to:
AWS for cloud resources (EC2, RDS, ALB, etc.), and
Generic or OnPrem for abstract or non-cloud-specific components.
Infer reasonable groupings (clusters) based on the description even if not explicitly asked:
Example: request handling layer, business logic layer, data layer, caching layer, monitoring/observability.
Map vague terms to reasonable diagrams components:
“Web server” → EC2 (or Nginx in on-prem)
“Database” → RDS (AWS) or SQL (generic)
“Cache” → Elasticache (AWS) or a suitable cache node in another provider.
Example Behavior
For the input:
"Web server connected to database in a VPC"
A valid response should look like:
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
graph_attr = {"rankdir": "LR", "splines": "ortho"}
with Diagram("Architecture", show=False, filename="generated_diagram", graph_attr=graph_attr):
    with Cluster("VPC"):
        web = EC2("Web Server")
        db = RDS("Database")
        web >> db

Example 2 (Generic SQL):
Input: "Python app with SQL database"
Output:
from diagrams import Diagram
from diagrams.programming.language import Python
from diagrams.generic.database import SQL

graph_attr = {"rankdir": "LR", "splines": "ortho"}

with Diagram("Architecture", show=False, filename="generated_diagram", graph_attr=graph_attr):
    app = Python("App")
    db = SQL("Database")
    app >> db

CRITICAL FINAL REMINDERS:
- Use `from diagrams.generic.database import SQL` (NOT onprem).
- Use `from diagrams.onprem.client import Client` (NOT generic).
- Use `Dynamodb` (lowercase 'db').
- Follow these rules strictly. Do not add any text outside the Python code."""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                top_p=1,
                max_tokens=1024,
                stream=False
            )
            
            code = completion.choices[0].message.content
            
            # Robust code extraction using regex
            import re
            
            # 1. Look for ```python ... ```
            match = re.search(r'```python\s*(.*?)```', code, re.DOTALL)
            if match:
                code = match.group(1).strip()
            else:
                # 2. Look for ``` ... ```
                match = re.search(r'```\s*(.*?)```', code, re.DOTALL)
                if match:
                    code = match.group(1).strip()
                # 3. Fallback: Look for the first occurrence of "from diagrams" or "import diagrams"
                # This handles cases like "Here is the code:\nfrom diagrams import..."
                import_match = re.search(r'(from diagrams|import diagrams)', code)
                if import_match:
                    start_index = import_match.start()
                    code = code[start_index:].strip()
            
            # 4. Post-process code to fix common LLM hallucinations
            code = self._post_process_code(code)
            
            return code

        except Exception as e:
            print(f"Error generating code: {e}")
            return None

    def _post_process_code(self, code):
        """
        Fixes common import errors that the LLM tends to make despite prompt instructions.
        """
        replacements = [
            ("from diagrams.onprem.database import SQL", "from diagrams.generic.database import SQL"),
            ("from diagrams.generic.network import Client", "from diagrams.onprem.client import Client"),
            ("from diagrams.generic.network import User", "from diagrams.onprem.client import User"),
            ("from diagrams.generic.compute import Server", "from diagrams.onprem.compute import Server"),
            ("from diagrams.aws.database import PostgreSQL", "from diagrams.aws.database import RDS"),
            ("from diagrams.generic.network import Nginx", "from diagrams.onprem.network import Nginx"),
            ("from diagrams.generic.network import CDN", "from diagrams.aws.network import CloudFront as CDN"),
            ("from diagrams.generic.programming import React", "from diagrams.programming.framework import React"),
            ("from diagrams.generic.programming", "from diagrams.programming.language"),
            ("from diagrams.onprem.storage import HDFS", "from diagrams.onprem.analytics import Hadoop as HDFS"),
            ("from diagrams.generic.place import Region", "from diagrams.generic.place import Datacenter as Region"),
        ]
        
        for bad, good in replacements:
            code = code.replace(bad, good)
            
        # Remove trailing connection operators (e.g., "a >> b >>")
        import re
        code = re.sub(r'\s*(>>|<<)\s*$', '', code, flags=re.MULTILINE)

        # Fix unterminated string/parentheses at the very end of code (truncation)
        stripped_code = code.strip()
        if stripped_code.endswith('("'):
             code += 'Unknown")'
        elif stripped_code.endswith('="'):
             code += 'Unknown"'
        elif stripped_code.endswith('"'):
             # Check if it's a closing quote or opening quote that got cut off?
             # Hard to tell without context, but usually if it ends in " it might be okay or missing )
             # Let's count quotes.
             if stripped_code.count('"') % 2 != 0:
                 code += '")' # Assume it was inside a function call like Server("...
        elif stripped_code.endswith('('):
             code += '"Unknown")'

        # Fix truncated variable names
        # 1. Extract all defined variables (lhs = ...)
        defined_vars = set(re.findall(r'^\s*(\w+)\s*=', code, re.MULTILINE))
        
        # 2. Find all used variables in connections (>> var or var >>)
        used_vars = set(re.findall(r'(\w+)\s*(?:>>|<<)', code)) | \
                    set(re.findall(r'(?:>>|<<)\s*(\w+)', code)) | \
                    set(re.findall(r'^\s*(\w+)\s*$', code, re.MULTILINE))
        
        # 3. Identify undefined variables
        undefined_vars = used_vars - defined_vars
        
        # 4. Attempt to match undefined vars to defined vars (prefix match)
        for undefined in undefined_vars:
            # Find a defined var that starts with the undefined var (e.g. 'licensing' matches 'licensing_drm_service')
            # We prefer the shortest defined var that matches, or just the first one found.
            match = next((v for v in defined_vars if v.startswith(undefined)), None)
            
            # If not found, try the other way around (undefined starts with defined - less likely for truncation but possible)
            if not match:
                match = next((v for v in defined_vars if undefined.startswith(v)), None)
                
            if match:
                # Replace the undefined var with the match in the code
                # Use word boundary to avoid partial replacements of other words
                code = re.sub(r'\b' + re.escape(undefined) + r'\b', match, code)
            
        return code

