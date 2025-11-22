import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DesignRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Arcgen Backend is running"}

@app.post("/generate")
async def generate_diagram(request: DesignRequest):
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing NVIDIA_API_KEY. Please provide your API key.")

    # Mock response for now
    csv_data = """## Label: %label%
## Style: shape=%shape%;whiteSpace=wrap;html=1;
## Connect: {"from": "edge_target", "to": "id", "style": "curved=1;endArrow=blockThin;endFill=1;"}
id,label,shape,edge_target
1,User,actor,2
2,Login,rounded=1,3
3,Dashboard,rectangle,"""
    
    return {
        "csv": csv_data
    }
