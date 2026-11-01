
from fastapi import FastAPI, HTTPException
from pathlib import Path
import joblib
import pandas as pd
import logging

from app.schemas import CustomerData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "churn_pipeline.joblib"

# Create FastAPI app
app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict whether a telecom customer may leave.",
    version="1.0.1"
)

# Load trained model safely
model = None

try:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    logger.info("Customer churn model loaded successfully.")

except Exception:
    logger.exception("Failed to load the customer churn model.")


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is running",
        "status": "success",
        "docs": "/docs"
    }


# Health endpoint
@app.get("/health")
def health():
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded"
        )

    return {
        "status": "healthy",
        "model_loaded": True
    }


# Prediction endpoint
@app.post("/predict")
def predict(data: CustomerData):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Prediction model is unavailable"
        )

    try:
        # Convert customer input into DataFrame
        input_data = pd.DataFrame([data.model_dump()])

        # Generate prediction
        prediction = model.predict(input_data)[0]

        # Generate churn probability
        probability = model.predict_proba(input_data)[0][1]

        churn_probability = round(
            float(probability) * 100, 2
        )

        # Prepare response
        result = {
            "prediction": "Yes" if prediction == 1 else "No",
            "churn_probability": churn_probability,
            "message": (
                "Customer is likely to churn"
                if prediction == 1
                else "Customer is likely to stay"
            )
        }

        return result

    except Exception:
        logger.exception("Prediction failed.")

        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check the API logs."
        )
