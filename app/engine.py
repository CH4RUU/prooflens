from sympy import sympify, solve, Eq

class MathVerifier:
    """
    Enhanced verifier that checks if the solution set (the value of x) 
    remains consistent across steps.
    """
    @staticmethod
    def verify_equality(original_problem, step_content):
        """
        Verifies if the new step has the same solution as the original problem.
        Example: '3*x - 9 = 0' has solution x=3. '3*x = 9' also has solution x=3.
        """
        try:
            # 1. Parse strings into SymPy Equation components
            orig_lhs, orig_rhs = original_problem.split('=')
            step_lhs, step_rhs = step_content.split('=')
            
            # 2. Create Equation objects
            orig_eq = Eq(sympify(orig_lhs.strip()), sympify(orig_rhs.strip()))
            step_eq = Eq(sympify(step_lhs.strip()), sympify(step_rhs.strip()))
            
            # 3. Solve both equations for 'x'
            # This is the "Gold Standard" of verification. 
            # If the value of x hasn't changed, the logic is sound.
            sol_orig = solve(orig_eq)
            sol_step = solve(step_eq)
            
            # If solutions match, return True
            if sol_orig == sol_step:
                return True, 1.0
            else:
                return False, 0.0
                
        except Exception as e:
            # Catch parsing errors (like syntax errors in the math string)
            return False, 0.0

if __name__ == "__main__":
    verifier = MathVerifier()
    # Test: These should now both solve to {3} and return True
    is_correct, score = verifier.verify_equality("3*x - 9 = 0", "3*x = 9")
    print(f"Verification: {is_correct}, Score: {score}")