import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Churn Prediction ANN", page_icon="💡", layout="centered")
st.title("💡 Customer Churn Prediction using ANN")
st.markdown("This app predicts whether a customer will **churn** (leave the bank) using an Artificial Neural Network.")

# ---------------------------
# Load Model
# ---------------------------
@st.cache_resource
def load_ann_model():
    model = load_model("churn_model.h5")  # Make sure file exists in same folder
    return model

model = load_ann_model()

# ---------------------------
# User Inputs
# ---------------------------
st.header("🧾 Enter Customer Details")

col1, col2 = st.columns(2)
with col1:
    credit_score = st.number_input("Credit Score", 300, 900, 600)
    geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.slider("Age", 18, 92, 35)
    tenure = st.slider("Tenure (Years with Bank)", 0, 10, 3)
with col2:
    balance = st.number_input("Account Balance", 0.0, 250000.0, 60000.0)
    num_products = st.slider("Number of Products", 1, 4, 2)
    has_credit_card = st.selectbox("Has Credit Card?", ["Yes", "No"])
    is_active = st.selectbox("Active Member?", ["Yes", "No"])
    salary = st.number_input("Estimated Salary", 1000.0, 200000.0, 50000.0)

# ---------------------------
# Prepare Input Data
# ---------------------------
if st.button("🔍 Predict Churn"):
    # One-hot encode Geography
    geography_dict = {"France": [1,0,0], "Germany": [0,1,0], "Spain": [0,0,1]}
    gender_val = 1 if gender == "Male" else 0
    geography_val = geography_dict[geography]

    # Create input array
    input_data = np.array([
        geography_val[0], geography_val[1], geography_val[2],
        credit_score, gender_val, age, tenure, balance,
        num_products, 1 if has_credit_card == "Yes" else 0,
        1 if is_active == "Yes" else 0, salary
    ])

    # Simple normalization (approximation)
    input_data = input_data.reshape(1, -1)
    input_data = input_data / np.max(input_data)

    # Predict
    prediction = model.predict(input_data)[0][0]

    if prediction > 0.5:
        st.error(f"⚠️ The customer is **likely to CHURN** (Probability: {prediction:.2f})")
    else:
        st.success(f"✅ The customer is **likely to STAY** (Probability: {1 - prediction:.2f})")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and TensorFlow")
