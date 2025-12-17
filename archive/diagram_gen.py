import sys
import io
import os
from contextlib import redirect_stdout

def execute_diagram_code(code_str):
    """
    Executes the provided Python code string to generate a diagram.
    Returns the path to the generated image or raises an error.
    """
    try:
        # Execute the code
        # The code is expected to generate 'generated_diagram.png'
        exec(code_str, globals())
        
        # Check if file exists
        if os.path.exists("generated_diagram.png"):
            return "generated_diagram.png"
        else:
            raise FileNotFoundError("Diagram image was not generated. Check the code logic.")
            
    except Exception as e:
        # Log the failing code for debugging
        numbered_code = "\n".join([f"{i+1}: {line}" for i, line in enumerate(code_str.splitlines())])
        print(f"FAILED CODE:\n{'-'*20}\n{numbered_code}\n{'-'*20}")
        raise RuntimeError(f"Failed to execute diagram code: {e}")