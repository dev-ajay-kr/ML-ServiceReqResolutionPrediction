import streamlit as st
import pandas as pd
import joblib

# Load the full pipeline
try:
    model_pipeline = joblib.load('incident_resolution_pipeline.pkl')
except Exception as e:
    st.error(f"Error loading model. Please run the notebook to generate 'incident_resolution_pipeline.pkl'. Error: {e}")
    st.stop()

st.set_page_config(page_title="Resolution Time Predictor", layout="centered")

st.title(" IT Incident Resolution Predictor")
st.markdown("Enter incident details below to estimate the time required for resolution.")

with st.form(key='incident_form'):
    
    st.subheader("Incident Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Options must match the training data format exactly (Title Case)
        category = st.selectbox("Category", ['Email', 'Access', 'Network', 'VPN', 'Software', 'System', 'Database', 'Application', 'Hardware', 'Security'])
        priority = st.selectbox("Priority", ['Low', 'Medium', 'High', 'Critical'])
        assignment_group = st.selectbox("Assignment Group", ['Network Team', 'IT Support', 'Security Ops', 'Database Admin', 'Application Support'])
        
    with col2:
        customer_score = st.slider("Customer Historical Score", 1, 5, 3, help="1=Poor, 5=Excellent")
        
    st.subheader("Contextual Information")
    issue_description = st.text_area("Issue Description", placeholder="E.g., User unable to access shared folder X...", height=100)
    work_notes = st.text_area("Work Notes / Steps Taken", placeholder="E.g., Checked permissions, reset password, pinged server...", height=100, help="More complex steps usually indicate longer resolution times.")

    submit_button = st.form_submit_button(label='Predict Resolution Time')

    if submit_button:
        # Create dataframe for prediction
        input_data = pd.DataFrame([{
            'Category': category,
            'Priority': priority,
            'Assignment Group': assignment_group,
            'Customer Score': customer_score,
            'Issue Description': issue_description,
            'Work Notes': work_notes
        }])
        
        try:
            # Predict
            prediction_hours = model_pipeline.predict(input_data)[0]
            
            # Convert to hours and minutes for better readability
            hours = int(prediction_hours)
            minutes = int((prediction_hours - hours) * 60)
            
            st.divider()
            
            # Display as a Card (Metric)
            col_res1, col_res2, col_res3 = st.columns([1, 2, 1])
            with col_res2:
                st.metric(
                    label="Estimated Resolution Time",
                    value=f"{hours}h {minutes}m",
                    delta="AI Prediction",
                    delta_color="off"
                )
                
                # Contextual message based on time
                if prediction_hours > 6:
                    st.warning("⚠️ High complexity detected. Expect > 1 business day.")
                elif prediction_hours < 2:
                    st.success("✅ Quick resolution expected.")
                else:
                    st.info("ℹ️ Standard resolution timeframe.")
                    
        except Exception as e:
            st.error(f"Prediction Error: {e}")