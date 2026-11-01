from fastapi import FastAPI, HTTPException
from pathlib import Path
import joblib
import pandas as pd

from app.schemas import CustomerData

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "churn_pipeline.joblib"

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict whether a telecom customer may leave.",
    version="1.0"
)

model = joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return {"message": "Customer Churn Prediction API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: CustomerData):
    try:
        input_data = pd.DataFrame([data.model_dump()])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        return {
            "prediction": "Yes" if prediction == 1 else "No",
            "churn_probability": round(float(probability) * 100, 2),
            "message": (
                "Customer is likely to churn"
                if prediction == 1
                else "Customer is likely to stay"
            )
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))