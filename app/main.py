from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.graph import app_graph
import os

app = FastAPI(title="ProofLens AI")

# --- 1. CORS Configuration ---
# This allows your index.html to make requests to the backend without security blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MathRequest(BaseModel):
    problem: str

# --- 2. Solve Endpoint ---
@app.post("/solve")
async def solve_math(request: MathRequest):
    # Configuration for memory persistence (Thread ID keeps the session unique)
    config = {"configurable": {"thread_id": "session_1"}} 
    
    initial_state = {
        "problem": request.problem,
        "steps": [],
        "current_step": 0,
        "final_answer": "",
        "is_verified": False
    }
    
    # Run the LangGraph workflow
    result = app_graph.invoke(initial_state, config=config)
    return result

# --- 3. Frontend Serving ---
# This serves the 'frontend' folder you created earlier
@app.get("/")
async def read_index():
    # Ensure index.html is located at frontend/index.html
    return FileResponse('frontend/index.html')

# Optional: Serve other static assets (CSS/JS) if you add them later
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")