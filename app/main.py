
from fastapi import FastAPI, HTTPException
from pathlib import Path
import joblib
import pandas as pd
import logging
import traceback

from app.schemas import CustomerData


# --------------------------------
# 1. Configure logging
# --------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------
# 2. Project paths
# --------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "model" / "churn_pipeline.joblib"


# --------------------------------
# 3. Create FastAPI application
# --------------------------------

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict whether a telecom customer may leave.",
    version="1.0.2"
)


# --------------------------------
# 4. Load trained ML model
# --------------------------------

model = None
model_error = None

def load_model():

    global model, model_error

    try:

        logger.info("Starting customer churn model loading...")
        logger.info("Model path: %s", MODEL_PATH)

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}"
            )

        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Model path is not a file: {MODEL_PATH}"
            )

        loaded_model = joblib.load(MODEL_PATH)

        model = loaded_model
        model_error = None

        logger.info(
            "Customer churn model loaded successfully!"
        )

        return True

    except Exception as error:

        model = None
        model_error = str(error)

        logger.exception(
            "Failed to load the customer churn model."
        )

        return False


# Load model when application starts
load_model()


# --------------------------------
# 5. Home endpoint
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "Customer Churn Prediction API is running",
        "status": "success",
        "model_loaded": model is not None,
        "docs": "/docs",
        "health": "/health"
    }


# --------------------------------
# 6. Health check endpoint
# --------------------------------

@app.get("/health")
def health():

    if model is None:

        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "model_loaded": False,
                "error": model_error
            }
        )

    return {
        "status": "healthy",
        "model_loaded": True,
        "model_path": str(MODEL_PATH)
    }


# --------------------------------
# 7. Model status endpoint
# --------------------------------

@app.get("/model-status")
def model_status():

    return {
        "model_loaded": model is not None,
        "model_exists": MODEL_PATH.exists(),
        "model_path": str(MODEL_PATH),
        "error": model_error
    }


# --------------------------------
# 8. Prediction endpoint
# --------------------------------

@app.post("/predict")
def predict(data: CustomerData):

    # Check model availability
    if model is None:

        logger.error(
            "Prediction requested but model is unavailable."
        )

        raise HTTPException(
            status_code=503,
            detail="Prediction model is unavailable. Check /model-status and Render logs."
        )

    try:

        logger.info("Received prediction request.")

        # Convert customer input into DataFrame
        input_data = pd.DataFrame(
            [data.model_dump()]
        )

        logger.info(
            "Input data prepared successfully."
        )

        # Generate prediction
        prediction = model.predict(input_data)[0]

        # Generate churn probability
        probability = model.predict_proba(input_data)[0][1]

        churn_probability = round(
            float(probability) * 100,
            2
        )

        # Prepare response
        result = {

            "prediction": (
                "Yes" if prediction == 1 else "No"
            ),

            "churn_probability": churn_probability,

            "message": (
                "Customer is likely to churn"
                if prediction == 1
                else "Customer is likely to stay"
            )
        }

        logger.info(
            "Prediction completed successfully: %s",
            result
        )

        return result

    except HTTPException:
        raise

    except Exception:

        logger.exception(
            "Prediction failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check the API logs."
        )


# --------------------------------
# 9. Root-level API information
# --------------------------------

@app.get("/api-info")
def api_info():

    return {
        "project": "Customer Churn Prediction",
        "framework": "FastAPI",
        "model": "Machine Learning Pipeline",
        "version": "1.0.2",
        "endpoints": {
            "home": "/",
            "health": "/health",
            "model_status": "/model-status",
            "prediction": "/predict",
            "documentation": "/docs"
        }
    }
