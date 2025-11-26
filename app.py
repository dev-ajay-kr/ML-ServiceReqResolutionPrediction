import streamlit as st
import pandas as pd
import joblib

# Load assets
try:
    preprocessor = joblib.load('data_preprocessor.pkl')
    resolution_model = joblib.load('resolution_time_predictor.pkl')
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.title("Service Request Resolution Time Predictor")

with st.form(key='incident_form'):
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", ['email', 'access', 'network', 'vpn', 'software'])
        priority = st.selectbox("Priority", ['low', 'medium', 'high', 'critical'])
        assignment_group = st.selectbox("Assignment Group", ['network', 'support', 'security'])
        assignee = st.text_input("Assignee Name", "Alice")
    with col2:
        customer_score = st.slider("Customer Score", 1, 5, 3)

    submit_button = st.form_submit_button(label='Predict')

    if submit_button:
        # Create dataframe from inputs (ensure columns match training data exactly)
        input_data = pd.DataFrame([{
            'Category': category, 'Priority': priority, 'Assignment Group': assignment_group, 
            'Assignee': assignee, 'Customer Score': customer_score
        }])
        
        # Add missing columns with defaults if necessary to match pipeline expectations
        # (This depends on your specific X_train columns)
        
        try:
            processed_input = preprocessor.transform(input_data)
            prediction = resolution_model.predict(processed_input)[0]
            st.success(f"Estimated Resolution Time: {prediction:.2f} minutes")
        except Exception as e:
            st.error(f"Prediction Error: {e}")