#  ProofLens AI: Verified Math Reasoning System

ProofLens AI is an agentic mathematical solver that bridges the gap between **Large Language Models (LLMs)** and **Symbolic Mathematics**. Unlike standard AI chat, ProofLens verifies every algebraic step using a formal math engine to eliminate hallucinations.



---

##  The Problem & The Solution

**The Problem:** LLMs like Llama 3 are "probabilistic," meaning they predict the next word but don't actually "calculate." This leads to frequent hallucinations in multi-step algebra.

**The Solution:** ProofLens uses a **"Verifier-in-the-Loop"** architecture.
1. **The Brain (Ollama/Llama 3):** Proposes a logical step.
2. **The Logic (LangGraph):** Manages the workflow and state.
3. **The Truth (SymPy):** A symbolic math engine that verifies if the step is mathematically sound.

---

##  Project Setup

### 1. Prerequisites
* **macOS/Linux/Windows** (Tested on MacBook Air)
* **Python 3.10+**
* **Ollama** (Download from [ollama.com](https://ollama.com))

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/prooflens-ai.git](https://github.com/YOUR_USERNAME/prooflens-ai.git)
cd prooflens-ai

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
