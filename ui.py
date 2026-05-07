import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="ProofLens AI", 
    page_icon="🚀", 
    layout="wide"
)

# 2. Sidebar: RAG Knowledge & Session Control
with st.sidebar:
    st.title("📚 ProofLens Control")
    st.markdown("---")
    st.subheader("Grounded Math Rules")
    st.info("**Algebra:** Balance equations by performing identical operations on both sides.")
    st.info("**Verification:** Symbolic solving via SymPy ensures logical consistency.")
    
    st.markdown("---")
    if st.button("🗑️ Clear Session History"):
        # This resets the UI state
        st.rerun()

# 3. Main Header
st.title("🚀 ProofLens AI")
st.subheader("Verified Multi-Step Reasoning System")
st.markdown("---")

# 4. Input Section
problem = st.text_input("Enter your mathematical equation:", value="2*x + 10 = 20")

if st.button("🔍 Solve & Verify Steps"):
    if not problem:
        st.warning("Please enter a problem first.")
    else:
        with st.spinner("AI is reasoning and checking symbolic truths..."):
            try:
                # API Call to FastAPI Backend
                response = requests.post(
                    "http://127.0.0.1:8000/solve", 
                    json={"problem": problem},
                    timeout=300 # Increased timeout for local LLM loops
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 5. Success Banner
                    if data.get('is_verified'):
                        st.balloons()
                        st.success(f"### 🎉 Solution Verified: {data['steps'][-1].get('cleaned_math', 'Solved')}")
                    else:
                        st.warning("⚠️ System reached step limit without a verified final answer.")

                    st.write("### 📝 Verified Reasoning Path")
                    
                    # 6. Step Display Loop
                    for i, step in enumerate(data['steps']):
                        # Check verification status for color coding
                        is_valid = step.get('verified', False)
                        status_icon = "✅" if is_valid else "❌"
                        
                        with st.container():
                            col1, col2 = st.columns([1, 6])
                            
                            with col1:
                                if is_valid:
                                    st.markdown(f"#### {status_icon} Valid")
                                else:
                                    st.markdown(f"#### {status_icon} Error")
                            
                            with col2:
                                # Show the cleaned math equation clearly
                                st.code(step.get('cleaned_math', 'Parsing error...'), language="python")
                                
                                # If it failed, show the specific error from the engine
                                if not is_valid:
                                    st.error(f"**Verifier Feedback:** {step.get('error_message', 'The logic provided does not match the algebraic requirements.')}")
                                
                                # Expander for the "Raw Brain Output"
                                with st.expander("View LLM Thought Process"):
                                    st.text(step.get('raw', ''))
                            
                            st.markdown("---")
                else:
                    st.error(f"Backend Error: {response.status_code}")

            except Exception as e:
                st.error(f"Connection Failed. Ensure the FastAPI server (uvicorn) is running.\n\nError: {e}")

# 7. Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.caption("ProofLens AI v1.0 | Engine: LangGraph + SymPy | Brain: Ollama Llama 3")