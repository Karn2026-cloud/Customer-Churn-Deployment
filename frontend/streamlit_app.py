
import os
import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

# Local API is used by default.
# On Render, configure API_URL as an environment variable.
API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/predict"
).strip().rstrip("/")

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .main {
        background-color: #f5f7fb;
    }

    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #17365d;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 16px;
        color: #64748b;
        margin-bottom: 25px;
    }

    .result-card {
        padding: 22px;
        border-radius: 12px;
        background-color: white;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }

    .small-text {
        color: #64748b;
        font-size: 13px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #1769aa;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        min-height: 45px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #0e4f87;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("📊 Churn Predictor")

    st.write("Machine Learning Based Prediction")

    st.divider()

    st.subheader("API Configuration")

    st.caption("Backend endpoint:")
    st.code(API_URL, language="text")

    if st.button("Check Backend Connection", use_container_width=True):

        health_url = API_URL.rsplit("/predict", 1)[0] + "/health"

        try:
            health_response = requests.get(
                health_url,
                timeout=15
            )

            if health_response.status_code == 200:
                st.success("Backend is connected!")
            else:
                st.error(
                    f"Backend returned status {health_response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Connection failed: {e}")

    st.divider()

    st.subheader("About Project")

    st.write(
        "This application uses a Machine Learning model "
        "to predict whether a telecom customer may leave "
        "the company."
    )

    st.caption("Developed using Python, Streamlit, FastAPI and Scikit-learn.")

# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">Customer Churn Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Analyze customer information and estimate the possibility of churn.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# CUSTOMER INPUT FORM
# --------------------------------------------------

st.subheader("👤 Customer Information")

with st.form("customer_form"):

    col1, col2, col3 = st.columns(3)

    # COLUMN 1
    with col1:

        st.markdown("#### Personal Information")

        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        senior = st.selectbox(
            "Senior Citizen",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        partner = st.selectbox(
            "Partner",
            ["Yes", "No"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"]
        )

        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=100,
            value=12
        )

        phone = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

    # COLUMN 2
    with col2:

        st.markdown("#### Internet and Services")

        multiple = st.selectbox(
            "Multiple Lines",
            ["Yes", "No", "No phone service"]
        )

        internet = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

        security = st.selectbox(
            "Online Security",
            ["Yes", "No", "No internet service"]
        )

        backup = st.selectbox(
            "Online Backup",
            ["Yes", "No", "No internet service"]
        )

        protection = st.selectbox(
            "Device Protection",
            ["Yes", "No", "No internet service"]
        )

        support = st.selectbox(
            "Tech Support",
            ["Yes", "No", "No internet service"]
        )

    # COLUMN 3
    with col3:

        st.markdown("#### Billing Information")

        tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No", "No internet service"]
        )

        movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No", "No internet service"]
        )

        contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )

        paperless = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

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
            "Monthly Charges",
            min_value=0.0,
            value=75.5,
            step=0.5
        )

        total = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=377.5,
            step=1.0
        )

    st.divider()

    submitted = st.form_submit_button(
        "🔍 Predict Customer Churn",
        use_container_width=True
    )

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

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

    # Basic input validation
    if tenure == 0 and total > 0:
        st.warning(
            "Please check the tenure and total charges values."
        )

    else:

        try:

            with st.spinner("Analyzing customer information..."):

                response = requests.post(
                    API_URL,
                    json=customer,
                    timeout=30
                )

            # Successful prediction
            if response.status_code == 200:

                result = response.json()

                prediction = result.get("prediction")
                probability = float(
                    result.get("churn_probability", 0)
                )

                message = result.get(
                    "message",
                    "Prediction completed."
                )

                st.divider()

                st.subheader("📈 Prediction Results")

                result_col1, result_col2 = st.columns(2)

                with result_col1:

                    st.metric(
                        label="Churn Prediction",
                        value=prediction
                    )

                with result_col2:

                    st.metric(
                        label="Churn Probability",
                        value=f"{probability:.2f}%"
                    )

                st.markdown("### Churn Probability")

                st.progress(
                    max(0, min(100, int(round(probability))))
                )

                st.caption(
                    "This percentage is the model's estimated "
                    "probability of churn, not a guarantee."
                )

                if prediction == "Yes":

                    st.error(
                        "⚠️ Customer is predicted to churn."
                    )

                    st.info(
                        "Suggested action: Review customer feedback, "
                        "service experience and available retention offers."
                    )

                elif prediction == "No":

                    st.success(
                        "✅ Customer is predicted to stay."
                    )

                    st.info(
                        "Continue providing good service and monitor "
                        "customer satisfaction."
                    )

                else:

                    st.warning(
                        "The API returned an unexpected prediction value."
                    )

                st.write("**API Message:**", message)

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.code(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to the FastAPI backend. "
                "Check the API_URL environment variable and "
                "make sure your backend service is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The backend took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.RequestException as e:

            st.error(f"Request failed: {e}")

        except (ValueError, KeyError, TypeError) as e:

            st.error(f"Invalid API response: {e}")

        except Exception as e:

            st.error(f"Unexpected error: {e}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#64748b; padding:15px;">
        <b>Customer Churn Prediction System</b><br>
        Built with Python | Machine Learning | FastAPI | Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
