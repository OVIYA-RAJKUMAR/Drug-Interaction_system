import streamlit as st
import requests
import json
from typing import List, Dict
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# API Configuration
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="MediSafe - Drug Interaction Analysis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #f39c12;
    }
    
    .danger-card {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #e74c3c;
    }
    
    .success-card {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #27ae60;
    }
    
    .drug-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def call_api(endpoint: str, data: dict) -> dict:
    """Make API calls to the backend"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 API Connection Error: {str(e)}")
        return {}

def create_severity_chart(interactions):
    """Create severity distribution chart"""
    if not interactions:
        return None
    
    severity_counts = {}
    for interaction in interactions:
        severity = interaction['severity']
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    fig = px.pie(
        values=list(severity_counts.values()),
        names=list(severity_counts.keys()),
        title="Drug Interaction Severity Distribution",
        color_discrete_map={'HIGH': '#e74c3c', 'MEDIUM': '#f39c12', 'LOW': '#27ae60'}
    )
    fig.update_layout(height=300)
    return fig

def create_dosage_chart(recommendations):
    """Create dosage comparison chart"""
    if not recommendations:
        return None
    
    drugs = [rec['drug_name'] for rec in recommendations]
    current_doses = []
    recommended_doses = []
    
    for rec in recommendations:
        current_doses.append(1)  # Placeholder
        recommended_doses.append(1)  # Placeholder
    
    fig = go.Figure(data=[
        go.Bar(name='Current', x=drugs, y=current_doses, marker_color='#e74c3c'),
        go.Bar(name='Recommended', x=drugs, y=recommended_doses, marker_color='#27ae60')
    ])
    fig.update_layout(barmode='group', title="Dosage Comparison", height=300)
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 MediSafe - Drug Interaction Analysis System</h1>
        <p>Advanced AI-Powered Medication Safety & Drug Interaction Detection Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for patient information
    with st.sidebar:
        st.markdown("### 👤 Patient Information")
        patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=30, help="Enter patient's age for age-specific recommendations")
        
        st.markdown("### 🏥 Medical History")
        conditions = st.text_area("Medical Conditions", placeholder="Enter conditions (one per line)\ne.g., Diabetes, Hypertension")
        medical_conditions = [c.strip() for c in conditions.split('\n') if c.strip()]
        
        st.markdown("### 📊 System Status")
        if st.button("🔄 Check API Status"):
            try:
                response = requests.get(f"{API_BASE_URL}/")
                st.success("✅ API Connected")
            except:
                st.error("❌ API Disconnected")
    
    # Initialize session state for drugs
    if 'drugs' not in st.session_state:
        st.session_state.drugs = []
    
    # Main content tabs with icons
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💊 Drug Management", "⚠️ Interactions", "📋 Dosage Analysis", 
        "🔄 Alternatives", "📝 Text Extraction"
    ])
    
    with tab1:
        st.markdown("### 💊 Drug Information Management")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### ➕ Add New Medication")
            with st.container():
                drug_name = st.text_input("🏷️ Drug Name", placeholder="e.g., Paracetamol")
                drug_dosage = st.text_input("💉 Dosage", placeholder="e.g., 500mg")
                drug_frequency = st.text_input("⏰ Frequency", placeholder="e.g., every 8 hours")
                
                if st.button("➕ Add Medication", type="primary"):
                    if drug_name:
                        # Auto-format dosage and frequency
                        formatted_dosage = drug_dosage
                        if drug_dosage and not any(unit in drug_dosage.lower() for unit in ['mg', 'g', 'ml']):
                            formatted_dosage = f"{drug_dosage}mg"
                        
                        formatted_frequency = drug_frequency
                        if drug_frequency and drug_frequency.isdigit():
                            formatted_frequency = f"every {drug_frequency} hours"
                        elif drug_frequency and "every" not in drug_frequency.lower():
                            formatted_frequency = f"every {drug_frequency} hours"
                        
                        st.session_state.drugs.append({
                            "name": drug_name,
                            "dosage": formatted_dosage,
                            "frequency": formatted_frequency
                        })
                        st.success(f"✅ Added {drug_name}")
                        st.rerun()
        
        with col2:
            st.markdown("#### 📋 Current Medication List")
            if st.session_state.drugs:
                for i, drug in enumerate(st.session_state.drugs):
                    st.markdown(f"""
                    <div class="drug-card">
                        <h4>💊 {drug['name'].title()}</h4>
                        <p><strong>Dosage:</strong> {drug['dosage']}</p>
                        <p><strong>Frequency:</strong> {drug['frequency']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🗑️ Remove {drug['name']}", key=f"remove_{i}"):
                        st.session_state.drugs.pop(i)
                        st.rerun()
            else:
                st.info("📝 No medications added yet")
            
            if st.session_state.drugs and st.button("🗑️ Clear All Medications"):
                st.session_state.drugs = []
                st.rerun()
    
    with tab2:
        st.markdown("### ⚠️ Drug Interaction Analysis")
        
        if st.button("🔍 Analyze Interactions", type="primary"):
            if st.session_state.drugs:
                patient_data = {
                    "age": patient_age,
                    "drugs": st.session_state.drugs,
                    "medical_conditions": medical_conditions
                }
                
                interactions = call_api("analyze-interactions", patient_data)
                
                if interactions:
                    st.markdown(f"### 🚨 Found {len(interactions)} Drug Interactions")
                    
                    # Create severity chart
                    chart = create_severity_chart(interactions)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    
                    for interaction in interactions:
                        severity_color = {
                            "HIGH": "danger-card",
                            "MEDIUM": "warning-card", 
                            "LOW": "success-card"
                        }.get(interaction["severity"], "warning-card")
                        
                        st.markdown(f"""
                        <div class="{severity_color}">
                            <h4>🚨 {interaction['severity']} SEVERITY INTERACTION</h4>
                            <p><strong>Drugs Involved:</strong> {', '.join(interaction['drugs_involved'])}</p>
                            <p><strong>Risk:</strong> {interaction['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="success-card">
                        <h4>✅ No Drug Interactions Detected</h4>
                        <p>Your current medication combination appears safe.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please add medications first")
    
    with tab3:
        st.markdown("### 📋 Age-Specific Dosage Analysis")
        
        if st.button("📊 Get Dosage Recommendations", type="primary"):
            if st.session_state.drugs:
                patient_data = {
                    "age": patient_age,
                    "drugs": st.session_state.drugs,
                    "medical_conditions": medical_conditions
                }
                
                recommendations = call_api("dosage-recommendations", patient_data)
                
                if recommendations:
                    st.markdown(f"### 📋 Dosage Analysis for Age Group: {recommendations[0]['age_group']}")
                    
                    for rec in recommendations:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>💊 {rec['drug_name'].title()}</h4>
                            <p><strong>Recommended Dosage:</strong> {rec['recommended_dosage']}</p>
                            <p><strong>Age Group:</strong> {rec['age_group']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if rec['warnings']:
                            for warning in rec['warnings']:
                                if "OVERDOSE" in warning or "REDUCE DOSAGE" in warning:
                                    st.markdown(f"""
                                    <div class="danger-card">
                                        <h4>🚨 CRITICAL WARNING</h4>
                                        <p>{warning}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div class="warning-card">
                                        <h4>⚠️ Caution</h4>
                                        <p>{warning}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                else:
                    st.info("📝 No specific dosage recommendations available")
            else:
                st.warning("⚠️ Please add medications first")
    
    with tab4:
        st.markdown("### 🔄 Alternative Medication Suggestions")
        
        if st.button("🔍 Find Safer Alternatives", type="primary"):
            if st.session_state.drugs:
                patient_data = {
                    "age": patient_age,
                    "drugs": st.session_state.drugs,
                    "medical_conditions": medical_conditions
                }
                
                alternatives = call_api("alternative-medications", patient_data)
                
                if alternatives:
                    st.markdown("### 💡 Recommended Alternative Medications")
                    for alt in alternatives:
                        if "OVERDOSE DETECTED" in alt['reason']:
                            st.markdown(f"""
                            <div class="danger-card">
                                <h4>🚨 {alt['name'].title()} (SAFER ALTERNATIVE)</h4>
                                <p><strong>Reason:</strong> {alt['reason']}</p>
                                <p><strong>Safe Dosage:</strong> {alt['dosage']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="success-card">
                                <h4>💊 {alt['name'].title()}</h4>
                                <p><strong>Reason:</strong> {alt['reason']}</p>
                                <p><strong>Dosage:</strong> {alt['dosage']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("📝 No alternative medications found")
            else:
                st.warning("⚠️ Please add medications first")
    
    with tab5:
        st.markdown("### 📝 AI-Powered Text Extraction")
        
        medical_text = st.text_area(
            "📄 Enter Medical Prescription Text:",
            placeholder="Example: Patient is prescribed paracetamol 500mg every 6 hours and ibuprofen 200mg every 8 hours for pain management",
            height=150
        )
        
        if st.button("🤖 Extract Drug Information", type="primary"):
            if medical_text:
                extracted_drugs = call_api("extract-drugs", {"text": medical_text})
                
                if extracted_drugs:
                    st.markdown("### ✅ Extracted Drug Information")
                    for drug in extracted_drugs:
                        st.markdown(f"""
                        <div class="success-card">
                            <h4>💊 {drug['name'].title()}</h4>
                            <p><strong>Dosage:</strong> {drug['dosage']}</p>
                            <p><strong>Frequency:</strong> {drug['frequency']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if st.button("➕ Add Extracted Drugs to Analysis"):
                        st.session_state.drugs.extend(extracted_drugs)
                        st.success("✅ Drugs added to analysis!")
                        st.rerun()
                else:
                    st.warning("⚠️ No drug information could be extracted")
            else:
                st.warning("⚠️ Please enter medical text")
    
    # Comprehensive Analysis Section
    st.markdown("---")
    st.markdown("### 🔍 Comprehensive Medical Analysis")
    
    if st.button("🚀 Run Complete Analysis", type="primary", use_container_width=True):
        if st.session_state.drugs:
            patient_data = {
                "age": patient_age,
                "drugs": st.session_state.drugs,
                "medical_conditions": medical_conditions
            }
            
            analysis = call_api("comprehensive-analysis", patient_data)
            
            if analysis:
                st.markdown("### 📊 Analysis Dashboard")
                
                # Metrics Dashboard
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("👤 Patient Age", analysis["patient_age"])
                with col2:
                    st.metric("💊 Drugs Analyzed", analysis["analyzed_drugs"])
                with col3:
                    st.metric("⚠️ Interactions", len(analysis["interactions"]))
                with col4:
                    overdose_count = len(analysis.get("overdose_warnings", []))
                    if overdose_count > 0:
                        st.metric("🚨 Overdoses", overdose_count, delta="CRITICAL")
                    else:
                        st.metric("✅ Overdoses", 0)
                
                # Detailed Results
                if analysis.get("overdose_warnings"):
                    st.markdown("### 🚨 CRITICAL: Overdose Warnings")
                    for warning in analysis["overdose_warnings"]:
                        st.markdown(f"""
                        <div class="danger-card">
                            <h4>🚨 {warning['drug'].upper()} OVERDOSE DETECTED</h4>
                            <p><strong>Warning:</strong> {warning['warning']}</p>
                            <p><strong>Current Daily Dose:</strong> {warning['estimated_daily']}mg</p>
                            <p><strong>Maximum Safe Dose:</strong> {warning['max_safe']}mg</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Interactions
                with st.expander("⚠️ Drug Interactions Analysis", expanded=True):
                    if analysis["interactions"]:
                        for interaction in analysis["interactions"]:
                            severity_class = {
                                "HIGH": "danger-card",
                                "MEDIUM": "warning-card",
                                "LOW": "success-card"
                            }.get(interaction["severity"], "warning-card")
                            
                            st.markdown(f"""
                            <div class="{severity_class}">
                                <h4>{interaction['severity']} SEVERITY</h4>
                                <p>{interaction['description']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("✅ No drug interactions found")
                
                # Dosage Recommendations
                with st.expander("📋 Dosage Recommendations", expanded=True):
                    for rec in analysis["dosage_recommendations"]:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>💊 {rec['drug_name'].title()}</h4>
                            <p><strong>Recommended:</strong> {rec['recommended_dosage']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for warning in rec.get('warnings', []):
                            if "OVERDOSE" in warning:
                                st.error(f"🚨 {warning}")
                            else:
                                st.warning(f"⚠️ {warning}")
                
                # Alternative Medications
                with st.expander("🔄 Alternative Medications", expanded=True):
                    for alt in analysis["alternative_medications"]:
                        if "OVERDOSE DETECTED" in alt['reason']:
                            st.markdown(f"""
                            <div class="danger-card">
                                <h4>🚨 {alt['name'].title()} (CRITICAL ALTERNATIVE)</h4>
                                <p><strong>Reason:</strong> {alt['reason']}</p>
                                <p><strong>Safe Dosage:</strong> {alt['dosage']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="success-card">
                                <h4>💊 {alt['name'].title()}</h4>
                                <p><strong>Reason:</strong> {alt['reason']}</p>
                                <p><strong>Dosage:</strong> {alt['dosage']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.caption(f"📅 Analysis completed: {analysis['analysis_timestamp']}")
        else:
            st.warning("⚠️ Please add medications first")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🏥 <strong>MediSafe</strong> - Advanced Drug Interaction Analysis System</p>
        <p>⚠️ <em>For educational purposes only. Always consult healthcare professionals.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()