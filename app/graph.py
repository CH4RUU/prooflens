import re
from typing import List, TypedDict
from langchain_community.llms import Ollama
from app.engine import MathVerifier
from app.utils import get_math_rules, format_error_feedback, extract_math_expression
from langgraph.graph import StateGraph, END
from sympy import solve, sympify, Eq
from langgraph.checkpoint.memory import MemorySaver

# 1. State Definition
class AgentState(TypedDict):
    problem: str
    steps: List[dict]
    current_step: int
    final_answer: str
    is_verified: bool

# 2. Components
llm = Ollama(model="llama3")
verifier = MathVerifier()

# 3. Node: Reasoning with Loop-Prevention Instruction
def reasoning_node(state: AgentState):
    print(f"--- Processing Step {state['current_step'] + 1} ---")
    
    # Baseline is the last verified successful step or the original problem
    valid_steps = [s['cleaned_math'] for s in state['steps'] if s.get('verified')]
    current_eq = valid_steps[-1] if valid_steps else state['problem']

    prompt = f"""
    [STRICT MATH MODE]
    Target: Isolate x on the left side (x = value).
    Current Equation: {current_eq}
    
    TASK: Provide the NEXT SINGLE algebraic step.
    
    RULES:
    1. Output ONLY the equation (Example: x = 10).
    2. Do NOT repeat the current equation: {current_eq}.
    3. If the current equation is '5*x = 50', you MUST divide by 5 to get 'x = 10'.
    4. NO words. Use '*' for multiplication.
    
    Next Equation:
    """
    
    response = llm.invoke(prompt)
    clean_response = extract_math_expression(response)
    
    return {
        "steps": state['steps'] + [{"raw": response, "cleaned_math": clean_response}], 
        "current_step": state['current_step'] + 1
    }

# 4. Node: Verification
def verification_node(state: AgentState):
    last_step = state['steps'][-1]
    cleaned_math = last_step['cleaned_math']
    
    # Check if this new equation has the same solution as the original problem
    is_valid, score = verifier.verify_equality(state['problem'], cleaned_math)

    new_steps = list(state['steps'])
    new_steps[-1]['verified'] = is_valid
    new_steps[-1]['confidence'] = score
    
    if not is_valid:
        new_steps[-1]['error_message'] = format_error_feedback(state['problem'], cleaned_math)
        print(f"❌ Rejected: {cleaned_math}")
    else:
        print(f"✅ Verified: {cleaned_math}")
    
    return {
        "steps": new_steps, 
        "is_verified": is_valid
    }

# 5. Routing Logic (Isolation Check)
def should_continue(state: AgentState):
    if not state["steps"]:
        return "solver"
        
    last_step = state["steps"][-1]
    # Remove all spaces for strict regex matching
    last_math = last_step.get("cleaned_math", "").replace(" ", "")
    
    # NEW: Check if 'x' is perfectly isolated (e.g., x=10 or x=10.5)
    # This ensures we don't stop at '5x=50'
    is_isolated = re.fullmatch(r"x=-?\d+(\.\d+)?", last_math)
    
    if last_step.get("verified") and is_isolated:
        print(f"--- Success: Solution {last_math} Verified ---")
        return END

    # If AI fails or gets stuck in a loop (12 steps max)
    if state["current_step"] >= 12:
        print("--- Invoking Symbolic Fallback Solver ---")
        try:
            lhs, rhs = state['problem'].split('=')
            equation = Eq(sympify(lhs.strip()), sympify(rhs.strip()))
            solution = solve(equation)
            
            val = solution[0]
            state['steps'].append({
                "raw": f"System Override: x = {val}",
                "cleaned_math": f"x = {val}",
                "verified": True,
                "confidence": 1.0
            })
            state['is_verified'] = True
        except Exception as e:
            print(f"Fallback Error: {e}")
        return END
        
    return "solver"

# 6. Workflow Construction
workflow = StateGraph(AgentState)

workflow.add_node("solver", reasoning_node)
workflow.add_node("verifier", verification_node)

workflow.set_entry_point("solver")
workflow.add_edge("solver", "verifier")

workflow.add_conditional_edges(
    "verifier",
    should_continue,
    {
        "solver": "solver",
        END: END
    }
)

memory = MemorySaver()
app_graph = workflow.compile(checkpointer=memory)