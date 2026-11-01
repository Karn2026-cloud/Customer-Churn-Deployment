
import os
import streamlit as st
import requests


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. API CONFIGURATION
# ==================================================

# Local default:
# http://127.0.0.1:8000/predict
#
# Render environment variable can be either:
# https://your-backend.onrender.com
# OR
# https://your-backend.onrender.com/predict

raw_api_url = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
).strip().rstrip("/")


def normalize_api_url(url):
    """
    Ensure that the API URL always points to POST /predict.
    """

    url = url.strip().rstrip("/")

    if not url:
        raise ValueError("API_URL environment variable is empty.")

    if url.endswith("/predict"):
        return url

    return url + "/predict"


try:
    API_URL = normalize_api_url(raw_api_url)
    API_CONFIG_ERROR = None

except ValueError as error:
    API_URL = None
    API_CONFIG_ERROR = str(error)


def get_health_url():
    """
    Convert prediction URL into health endpoint URL.
    """

    if not API_URL:
        return None

    return API_URL.rsplit("/predict", 1)[0] + "/health"


# ==================================================
# 3. CUSTOM CSS
# ==================================================

st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)


# ==================================================
# 4. SIDEBAR
# ==================================================

with st.sidebar:

    st.title("📊 Churn Predictor")

    st.write("Machine Learning Based Prediction")

    st.divider()

    st.subheader("API Configuration")

    st.caption("Prediction endpoint:")

    if API_URL:
        st.code(API_URL, language="text")
    else:
        st.error(API_CONFIG_ERROR)

    if st.button(
        "Check Backend Connection",
        use_container_width=True
    ):

        health_url = get_health_url()

        try:

            with st.spinner("Checking backend..."):

                health_response = requests.get(
                    health_url,
                    timeout=30
                )

            if health_response.status_code == 200:

                health_data = health_response.json()

                if health_data.get("model_loaded") is True:

                    st.success("Backend and ML model are ready!")

                else:

                    st.warning(
                        "Backend is running, but the model is unavailable."
                    )

            elif health_response.status_code == 503:

                st.error("Backend is running, but the ML model is not loaded.")

                st.code(health_response.text)

            else:

                st.error(
                    f"Backend returned status "
                    f"{health_response.status_code}"
                )

                st.code(health_response.text)

        except requests.exceptions.RequestException as error:

            st.error(f"Connection failed: {error}")

    st.divider()

    st.subheader("About Project")

    st.write(
        "This application uses a Machine Learning model "
        "to predict whether a telecom customer may leave "
        "the company."
    )

    st.caption(
        "Developed using Python, Streamlit, FastAPI and Scikit-learn."
    )


# ==================================================
# 5. MAIN HEADER
# ==================================================

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


# ==================================================
# 6. CUSTOMER INPUT FORM
# ==================================================

st.subheader("👤 Customer Information")

with st.form("customer_form"):

    col1, col2, col3 = st.columns(3)

    # ----------------------------------------------
    # COLUMN 1: PERSONAL INFORMATION
    # ----------------------------------------------

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

    # ----------------------------------------------
    # COLUMN 2: INTERNET AND SERVICES
    # ----------------------------------------------

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

    # ----------------------------------------------
    # COLUMN 3: BILLING INFORMATION
    # ----------------------------------------------

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


# ==================================================
# 7. PREDICTION
# ==================================================

if submitted:

    # ----------------------------------------------
    # CREATE CUSTOMER DATA
    # ----------------------------------------------

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

    # ----------------------------------------------
    # INPUT VALIDATION
    # ----------------------------------------------

    if tenure == 0 and total > 0:

        st.warning(
            "Please check the tenure and total charges values."
        )

    elif not API_URL:

        st.error(
            API_CONFIG_ERROR or "API URL is not configured."
        )

    else:

        try:

            # --------------------------------------
            # SEND POST REQUEST TO /predict
            # --------------------------------------

            with st.spinner(
                "Analyzing customer information..."
            ):

                response = requests.post(
                    API_URL,
                    json=customer,
                    headers={
                        "Content-Type": "application/json"
                    },
                    timeout=60
                )

            # --------------------------------------
            # SUCCESSFUL PREDICTION
            # --------------------------------------

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
                    max(
                        0,
                        min(
                            100,
                            int(round(probability))
                        )
                    )
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

            # --------------------------------------
            # API ERROR HANDLING
            # --------------------------------------

            elif response.status_code == 405:

                st.error(
                    "HTTP 405: Method Not Allowed. "
                    "Check that API_URL ends with /predict "
                    "and that FastAPI defines POST /predict."
                )

                st.code(
                    f"Request URL: {API_URL}\n"
                    f"Response: {response.text}"
                )

            elif response.status_code == 422:

                st.error(
                    "HTTP 422: Customer data does not match "
                    "the backend input schema."
                )

                st.code(response.text)

            elif response.status_code == 503:

                st.error(
                    "HTTP 503: The prediction model is unavailable. "
                    "Check the FastAPI /health endpoint and Render logs."
                )

                st.code(response.text)

            elif response.status_code == 500:

                st.error(
                    "HTTP 500: Prediction failed inside the backend."
                )

                st.code(response.text)

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.code(response.text)

        # ------------------------------------------
        # CONNECTION ERRORS
        # ------------------------------------------

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

        except requests.exceptions.RequestException as error:

            st.error(
                f"Request failed: {error}"
            )

        except (ValueError, KeyError, TypeError) as error:

            st.error(
                f"Invalid API response: {error}"
            )

        except Exception as error:

            st.error(
                f"Unexpected error: {error}"
            )


# ==================================================
# 8. FOOTER
# ==================================================

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
