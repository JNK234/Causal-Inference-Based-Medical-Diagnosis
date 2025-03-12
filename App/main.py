"""
Main Streamlit application for medical diagnosis system.
Handles UI and orchestrates the diagnosis workflow.
"""
import streamlit as st
from typing import Dict, List

from agents.extractor import extract_nodes
from agents.analyzer import analyze_causal_links, analyze_counterfactuals
from agents.validator import check_missing_info, generate_followup_questions
from agents.planner import generate_treatment_options, create_final_plan
from utils.schemas import PatientInfo, MedicalNodes, CausalAnalysis, TreatmentPlan

def initialize_app() -> None:
    """Setup app configuration and state."""
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'patient_info' not in st.session_state:
        st.session_state.patient_info = None
    if 'medical_nodes' not in st.session_state:
        st.session_state.medical_nodes = None
    if 'missing_info_responses' not in st.session_state:
        st.session_state.missing_info_responses = {}
    if 'diagnosis' not in st.session_state:
        st.session_state.diagnosis = None
    if 'treatment_plan' not in st.session_state:
        st.session_state.treatment_plan = None

def next_step():
    st.session_state.step += 1

def main():
    """
    Main streamlit app entry point with doctor intervention points.
    """
    st.title("Medical Diagnosis Assistant")
    initialize_app()
    
    # Progress tracking
    progress_bar = st.progress(st.session_state.progress)
    
    # Step 1: Initial Case Input
    if st.session_state.step == 1:
        st.header("Step 1: Enter Patient Case Details")
        st.info("Please provide detailed patient case information")
        
        with st.form("patient_form"):
            case_text = st.text_area("Enter patient case details:")
            submit_button = st.form_submit_button("Submit Case")
            
            if submit_button and case_text:
                with st.spinner("Processing case details..."):
                    st.session_state.patient_info = PatientInfo(case_text=case_text)
                    st.session_state.progress = 25
                    progress_bar.progress(st.session_state.progress)
                    next_step()
                    st.rerun()
    
    # Step 2: Node Extraction and Analysis
    elif st.session_state.step == 2:
        st.header("Step 2: Medical Factor Analysis")
        
        if not hasattr(st.session_state, 'nodes_extracted'):
            with st.spinner("Extracting medical factors..."):
                st.info("Analyzing case details to identify key medical factors...")
                nodes = extract_nodes(st.session_state.patient_info.case_text)
                st.session_state.nodes = nodes
                st.session_state.nodes_extracted = True
                st.session_state.progress = 50
                progress_bar.progress(st.session_state.progress)
        
        if hasattr(st.session_state, 'nodes_extracted'):
            with st.expander("Extracted Medical Factors", expanded=True):
                st.write(st.session_state.nodes)
            
            if not hasattr(st.session_state, 'causal_analyzed'):
                with st.spinner("Analyzing causal relationships..."):
                    st.info("Establishing relationships between medical factors...")
                    causal_links = analyze_causal_links(st.session_state.nodes)
                    st.session_state.causal_links = causal_links
                    st.session_state.causal_analyzed = True
                    st.session_state.progress = 75
                    progress_bar.progress(st.session_state.progress)
            
            if hasattr(st.session_state, 'causal_analyzed'):
                with st.expander("Causal Analysis Results", expanded=True):
                    st.write(st.session_state.causal_links)
                next_step()
                st.rerun()
    
    # Step 3: Gap Analysis
    elif st.session_state.step == 3:
        st.header("Step 3: Information Validation")
        
        if not hasattr(st.session_state, 'gaps_checked'):
            with st.spinner("Checking for information gaps..."):
                st.info("Validating completeness of medical information...")
                missing_info = check_missing_info(st.session_state.nodes)
                questions = generate_followup_questions(missing_info)
                st.session_state.missing_info = missing_info
                st.session_state.questions = questions
                st.session_state.gaps_checked = True
                st.session_state.progress = 100
                progress_bar.progress(st.session_state.progress)
        
        if st.session_state.missing_info:
            st.warning("Additional information required")
            with st.expander("Information Gaps Identified", expanded=True):
                st.write("Missing Information:")
                for item in st.session_state.missing_info:
                    st.write(f"- {item}")
                
                st.write("\nFollow-up Questions:")
                for q in st.session_state.questions:
                    st.write(f"- {q}")
        else:
            st.success("All necessary information is present")
            if st.button("Proceed to Treatment Planning"):
                next_step()
                st.rerun()
    
    # Add a restart button
    if st.session_state.step > 1:
        if st.sidebar.button("Start New Case"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            initialize_app()
            st.rerun()

if __name__ == "__main__":
    main()
