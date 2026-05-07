# 🚀 ProofLens AI
### Verified Math Reasoning System

ProofLens AI is a multi-step mathematical solver that uses **LangGraph** for agentic logic, **Ollama (Llama 3)** for reasoning, and **SymPy** for symbolic verification.

## Features
- **Step-by-Step Verification:** Every algebraic step is checked for mathematical truth.
- **Agentic Correction:** If the AI makes a mistake, the system forces a correction.
- **Modern UI:** Built with Tailwind CSS and FastAPI.

## How to Run
1. Start Ollama with Llama 3.
2. Run the backend: `uvicorn app.main:app --reload`
3. Open `http://127.0.0.1:8000` in your browser.
