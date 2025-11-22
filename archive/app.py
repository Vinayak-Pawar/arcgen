import streamlit as st
import os
from dotenv import load_dotenv
from llm_engine import LLMEngine
from diagram_gen import execute_diagram_code

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Arcgen - NL to System Design", layout="wide")

st.title("Arcgen: Natural Language to System Design Architecture")
st.markdown("Describe your system architecture, and Arcgen will visualize it for you.")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    api_key = os.getenv("NVIDIA_API_KEY")
    if api_key:
        st.success("NVIDIA API Key detected")
    else:
        st.error("NVIDIA API Key not found in .env")
        st.info("Please add your NVIDIA_API_KEY to the .env file.")

# Main input area
user_input = st.text_area("Describe your system:", height=150, placeholder="E.g., A scalable web application with a load balancer distributing traffic to 3 EC2 instances, connected to an RDS database.")

if st.button("Generate Architecture", type="primary"):
    if not user_input:
        st.warning("Please enter a description first.")
    elif not api_key:
        st.error("API Key missing. Cannot generate.")
    else:
        with st.spinner("Generating architecture..."):
            try:
                # 1. Initialize LLM
                llm = LLMEngine()
                
                # 2. Generate Code
                st.info("Consulting the Architect (LLM)...")
                code = llm.generate_code(user_input)
                
                # DEBUG: Show raw code for troubleshooting
                print(f"DEBUG: Extracted Code:\n{code}")
                with st.expander("Debug: Raw LLM Output"):
                    st.text(code)
                
                if not code:
                    st.error("Failed to generate code. Please try again.")
                else:
                    # 3. Execute Code
                    st.info("Drawing the Blueprint...")
                    image_path = execute_diagram_code(code)
                    
                    # 4. Display Result
                    st.success("Architecture Generated Successfully!")
                    st.image(image_path, caption="Generated Architecture", use_column_width=True)
                    
                    # 5. Show Code
                    with st.expander("View Generated Python Code"):
                        st.code(code, language="python")
                        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

