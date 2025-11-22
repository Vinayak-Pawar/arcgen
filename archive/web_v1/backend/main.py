from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from llm_engine import LLMEngine

load_dotenv()

app = FastAPI(title="Arcgen Backend")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

llm_engine = LLMEngine()

@app.post("/generate")
async def generate_diagram(request: PromptRequest):
    try:
        xml_data = llm_engine.generate_xml(request.prompt)
        return {"xml": xml_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
