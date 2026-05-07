import re

def get_math_rules(topic: str):
    rules = {
        "algebra": "Rule: To solve for x, perform the same operation on both sides of the equation.",
        "geometry": "Rule: Area of a circle = pi * r^2. Pythagorean theorem: a^2 + b^2 = c^2.",
        "calculus": "Rule: The derivative of x^n is n*x^(n-1)."
    }
    return rules.get(topic.lower(), "Ensure steps follow algebraic order of operations (PEMDAS).")

def format_error_feedback(step_input, step_output):
    return (f"Mathematical Error: The step '{step_output}' is not algebraically "
            f"equivalent to the previous state '{step_input}'. "
            f"Please check your signs (+/-) and operations.")

def extract_math_expression(text: str):
    """
    Super-Parser: Extracts only the equation and strips out AI 'chatter'.
    Converts 3x to 3*x for SymPy compatibility.
    """
    # 1. Find the equation pattern (LHS = RHS)
    # This regex is more selective to avoid capturing conversational dashes or arrows
    match = re.search(r"([a-zA-Z0-9\s\+\-\*\/\^\(\)]+\s*=\s*[a-zA-Z0-9\s\+\-\*\/\^\(\)]+)", text)
    
    if match:
        eq = match.group(1).strip()
        
        # 2. Clean out common AI words that might sneak into the regex
        # Removes any words longer than 2 letters that aren't math-related
        words_to_strip = ["Step", "Result", "Equation", "Simplifying", "Next", "Corrected"]
        for word in words_to_strip:
            eq = re.sub(f"(?i){word}", "", eq)
        
        # 3. Standardize multiplication: 3x -> 3*x
        eq = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq)
        
        # 4. Remove lingering arrows or extra symbols
        eq = eq.replace('>', '').replace('-', ' - ').replace('+', ' + ').strip()
        # Clean up double spaces created by the above
        eq = " ".join(eq.split())
        
        return eq
        
    return text.strip()