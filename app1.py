import streamlit as st
from App.utils import prompts
from App.models.azure import AzureModel


# -----------------------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------------------

st.set_page_config(page_title="Medical Causal Analysis", layout="centered")
st.title("Medical Causal Analysis Assistant")

# Instantiate your Azure OpenAI GPT-4o model (via LangChain)
llm = AzureModel()

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = "extract"  # first stage: extracting key factors
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# -----------------------------------------------------------------------------
# UI: CASE DETAILS
# -----------------------------------------------------------------------------

st.markdown("### 1. Enter Patient Case Details")
case_details = st.text_area(
    "Paste the patient's case information here.",
    height=150
)

# -----------------------------------------------------------------------------
# HELPER FUNCTION: LLM CALL
# -----------------------------------------------------------------------------

def run_llm(prompt: str, additional_context: str = "") -> str:
    """
    Appends user context to the prompt, calls the Azure GPT-4o LLM,
    returns the generated content.
    """
    full_prompt = f"{prompt}\n\n{additional_context}"
    response = llm.invoke(full_prompt)  # Adapt to your LLM usage
    return response.content

# -----------------------------------------------------------------------------
# MAIN BUTTON: PROCEED
# -----------------------------------------------------------------------------

if st.button("Proceed"):
    # Stage 1: Extract Key Factors
    if st.session_state.stage == "extract":
        with st.spinner("Extracting key factors from the case..."):
            result = run_llm(prompts.NODE_EXTRACTION_PROMPT, f"Case:\n{case_details}")
            st.session_state.conversation.append({
                "stage": "Extracted Key Factors",
                "content": result
            })
            st.session_state.stage = "causal_analysis"

    # Stage 2: Causal Analysis
    elif st.session_state.stage == "causal_analysis":
        with st.spinner("Performing causal analysis..."):
            # Provide the extracted key factors as context
            extracted_factors = st.session_state.conversation[-1]["content"]
            result = run_llm(prompts.CAUSAL_ANALYSIS_PROMPT, extracted_factors)
            st.session_state.conversation.append({
                "stage": "Causal Analysis",
                "content": result
            })
            st.session_state.stage = "missing_info"

    # Stage 3: Check for Missing Information
    elif st.session_state.stage == "missing_info":
        with st.spinner("Checking for missing information..."):
            last_content = st.session_state.conversation[-1]["content"]
            result = run_llm(prompts.VALIDATION_PROMPT, last_content)
            st.session_state.conversation.append({
                "stage": "Missing Information Check",
                "content": result
            })
            # If there's a missing info prompt, the user can fill it in below
            st.session_state.stage = "diagnosis"

    # Stage 4: Final Diagnosis
    elif st.session_state.stage == "diagnosis":
        with st.spinner("Generating final diagnosis..."):
            # The last stage's result has all the combined context
            full_context = st.session_state.conversation[-1]["content"]
            result = run_llm(prompts.COUNTERFACTUAL_PROMPT, full_context)
            st.session_state.conversation.append({
                "stage": "Final Diagnosis",
                "content": result
            })
            st.session_state.stage = "confirm_diagnosis"

    # Stage 5: (Await user confirmation of diagnosis)
    elif st.session_state.stage == "confirm_diagnosis":
        st.warning("Please click 'Confirm Diagnosis' below.")
        # We do not move stage here until user clicks confirm

    # Stage 6: Treatment Plan
    elif st.session_state.stage == "treatment_plan":
        with st.spinner("Formulating treatment plan..."):
            # Use entire conversation as context, or just the final diagnosis
            final_diag = st.session_state.conversation[-1]["content"]
            result = run_llm(prompts.TREATMENT_PROMPT, final_diag)
            st.session_state.conversation.append({
                "stage": "Treatment Plan",
                "content": result
            })
            st.session_state.stage = "confirm_treatment"

    # Stage 7: (Await user confirmation of treatment)
    elif st.session_state.stage == "confirm_treatment":
        st.warning("Please click 'Confirm Treatment Plan' below.")
        # We do not move stage here until user clicks confirm

# -----------------------------------------------------------------------------
# ADDITIONAL INFO ENTRY (IF PROMPTED)
# -----------------------------------------------------------------------------

if st.session_state.stage == "missing_info":
    st.info("If any missing information is requested, provide it below, then click Proceed again.")
    user_missing_input = st.text_input("Additional Data Required:")
    if user_missing_input:
        st.session_state.conversation.append({
            "stage": "User Additional Info",
            "content": user_missing_input
        })

# -----------------------------------------------------------------------------
# CONFIRM DIAGNOSIS BUTTON
# -----------------------------------------------------------------------------

if st.session_state.stage == "confirm_diagnosis":
    st.markdown("### Confirm the Final Diagnosis")
    st.markdown(st.session_state.conversation[-1]["content"])
    if st.button("Confirm Diagnosis"):
        st.success("Diagnosis Confirmed!")
        st.session_state.stage = "treatment_plan"

# -----------------------------------------------------------------------------
# CONFIRM TREATMENT BUTTON
# -----------------------------------------------------------------------------

if st.session_state.stage == "confirm_treatment":
    st.markdown("### Confirm the Final Treatment Plan")
    st.markdown(st.session_state.conversation[-1]["content"])
    if st.button("Confirm Treatment Plan"):
        st.success("Treatment Plan Confirmed!")
        st.session_state.stage = "done"

# -----------------------------------------------------------------------------
# DISPLAY CONVERSATION HISTORY
# -----------------------------------------------------------------------------

st.markdown("## Conversation / Analysis History")
for interaction in st.session_state.conversation:
    st.markdown(f"**{interaction['stage']}**")
    st.write(interaction["content"])

if st.session_state.stage == "done":
    st.balloons()
    st.info("All tasks completed successfully. You may restart or close the app.")
