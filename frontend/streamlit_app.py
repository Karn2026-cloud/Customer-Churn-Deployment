
import streamlit as st
import requests

st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"

st.title("📊 Customer Churn Prediction")
st.write("Predict whether a telecom customer is likely to leave.")

st.divider()

st.subheader("Customer Information")

with st.form("customer_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.number_input(
            "Tenure (months)", 0, 100, 12
        )
        phone = st.selectbox("Phone Service", ["Yes", "No"])

    with col2:
        multiple = st.selectbox(
            "Multiple Lines", ["Yes", "No", "No phone service"]
        )
        internet = st.selectbox(
            "Internet Service", ["DSL", "Fiber optic", "No"]
        )
        security = st.selectbox(
            "Online Security", ["Yes", "No", "No internet service"]
        )
        backup = st.selectbox(
            "Online Backup", ["Yes", "No", "No internet service"]
        )
        protection = st.selectbox(
            "Device Protection", ["Yes", "No", "No internet service"]
        )
        support = st.selectbox(
            "Tech Support", ["Yes", "No", "No internet service"]
        )

    with col3:
        tv = st.selectbox(
            "Streaming TV", ["Yes", "No", "No internet service"]
        )
        movies = st.selectbox(
            "Streaming Movies", ["Yes", "No", "No internet service"]
        )
        contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )
        monthly = st.number_input(
            "Monthly Charges", min_value=0.0, value=75.5
        )
        total = st.number_input(
            "Total Charges", min_value=0.0, value=377.5
        )

    submitted = st.form_submit_button(
        "Predict Customer Churn",
        use_container_width=True
    )

if submitted:

    customer = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": protection,
        "TechSupport": support,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    try:
        with st.spinner("Predicting customer churn..."):

            response = requests.post(
                API_URL,
                json=customer,
                timeout=30
            )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]
            probability = result["churn_probability"]

            st.divider()
            st.subheader("Prediction Results")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Churn Prediction",
                    prediction
                )

            with col2:
                st.metric(
                    "Churn Probability",
                    f"{probability}%"
                )

            st.progress(
                max(0, min(100, int(probability))) 
            )

            if prediction == "Yes":
                st.error("⚠️ Customer is likely to churn.")
            else:
                st.success("✅ Customer is likely to stay.")

        else:
            st.error(
                f"API Error {response.status_code}: {response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI. Make sure the backend is running."
        )

    except Exception as e:
        st.error(f"Unexpected error: {e}")
