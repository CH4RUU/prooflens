
---

#  ProofLens AI

##  The Problem & The Solution

**The Problem:** LLMs like Llama 3 are "probabilistic," meaning they predict the next word but don't actually "calculate." This leads to frequent hallucinations in multi-step algebra.

**The Solution:** ProofLens uses a **"Verifier-in-the-Loop"** architecture.
1. **The Brain (Ollama/Llama 3):** Proposes a logical step based on natural language understanding.
2. **The Logic (LangGraph):** Manages the state machine and ensures the workflow follows a strict path.
3. **The Truth (SymPy):** A symbolic math engine that verifies if the proposed step is algebraically equivalent to the original problem.

---

##  Project Setup

### 1. Prerequisites
* **OS:** macOS (Optimized for Apple Silicon), Linux, or Windows.
* **Python:** 3.10 or higher.
* **Ollama:** Required to run the Llama 3 model locally.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/prooflens-ai.git
cd prooflens-ai

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Project
1. **Launch Ollama:** Open your terminal and ensure the model is available:
   ```bash
   ollama run llama3
   ```
2. **Start the FastAPI Backend:**
   ```bash
   uvicorn app.main:app --reload
   ```
3. **Open the Dashboard:** Navigate to `[http://127.0.0.1:8000](http://127.0.0.1:8000)` in your web browser.

---

##  Dependencies & Why They Are Needed

| Dependency | Why it's critical |
| :--- | :--- |
| **FastAPI** | Acts as the "web-server" to handle API requests and serve the modern HTML interface. |
| **LangGraph** | Provides the "Agentic Framework" to create nodes (Solver/Verifier) and manage loops. |
| **SymPy** | The "Mathematical Judge" that performs formal symbolic computation to verify equality. |
| **Ollama (LangChain)** | The bridge that allows the Python code to communicate with the local Llama 3 model. |
| **Pydantic** | Used for strict data validation and schema definition for API requests. |

---

##  The Workflow (Agentic Logic)

The system operates on a state-based cyclic graph to ensure accuracy:

1. **Solver Node:** The LLM receives the current state of the equation and suggests exactly *one* algebraic operation.
2. **Verifier Node:** The suggested step is extracted via Regex and passed to SymPy. SymPy solves the original problem and the new step; if the solution sets match, the step is marked **Verified ✅**.
3. **Router Logic:** 
   - If verified, the graph proceeds to check if $x$ is isolated.
   - If rejected, the error feedback is sent back to the Solver to "try again" with better logic.
4. **Fallback:** If the AI fails to find a verified path within 12 steps, the system invokes the **Symbolic Solver** to provide the correct answer directly.

---

##  Interface & Documentation

### User Interface (Dashboard)
The UI is built with **Tailwind CSS**, offering a clean, professional "SaaS" aesthetic. It features a real-time progress tracker for the reasoning path.

<img width="1600" height="1040" alt="PHOTO-2026-05-07-13-34-39" src="https://github.com/user-attachments/assets/7253670b-6c02-4825-b97c-66580560bc51" />

<img width="758" height="505" alt="Screenshot 2026-05-07 at 2 11 58 PM" src="https://github.com/user-attachments/assets/9174ea1f-5ad8-4102-a81a-b11f95643fb8" />


<img width="725" height="503" alt="Screenshot 2026-05-07 at 2 12 24 PM" src="https://github.com/user-attachments/assets/6c858bc9-f4c6-4546-a196-8ff0d54dc0ad" />

<img width="792" height="503" alt="Screenshot 2026-05-07 at 2 12 44 PM" src="https://github.com/user-attachments/assets/2822544e-7ad1-49bd-b485-d27bc91b9db8" />


<img width="782" height="479" alt="Screenshot 2026-05-07 at 2 13 58 PM" src="https://github.com/user-attachments/assets/b149d372-6ee1-494c-85d6-510239eef979" />

### API Documentation
ProofLens features an interactive documentation page where you can test the `/solve` endpoint and view the JSON schema.

**URL:** `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`


<img width="761" height="443" alt="Screenshot 2026-05-07 at 2 15 01 PM" src="https://github.com/user-attachments/assets/7fe71c70-f5dd-48d8-8400-ab16e2a56403" />

<img width="789" height="470" alt="Screenshot 2026-05-07 at 2 14 42 PM" src="https://github.com/user-attachments/assets/fb79b69b-f246-42bb-b72e-fc21bba00a87" />


---

##  Key Features
- **Zero Hallucination:** Every step is mathematically proven before being shown to the user.
- **Local & Private:** No data leaves your machine; everything runs on Ollama.
- **Agentic Recovery:** The AI learns from the Verifier's error messages to correct its own mistakes.

---
**Developed by Charu Jagguka**  
Built for the intersection of AI Engineering and Mathematical Rigor.

```
