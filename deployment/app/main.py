from fastapi import FastAPI, Request
import mlflow.pyfunc
import pandas as pd
import os
from contextlib import asynccontextmanager
import time
import logging
from fastapi.responses import PlainTextResponse
import joblib

metrics = {"total_predictions": 0}

model = None
scaler = None
encoders = None

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, scaler, encoders
    try:
        tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        model_uri = os.getenv("MODEL_URI")

        logging.info(f"Iniciando aplicación")
        logging.info(f"MLFLOW_TRACKING_URI: {tracking_uri}")
        logging.info(f"MODEL_URI: {model_uri}")

        mlflow.set_tracking_uri(tracking_uri)
        logging.info(f"Conectando a MLflow en: {tracking_uri}")

        if not model_uri:
            raise ValueError("MODEL_URI environment variable is not set.")

        logging.info(f"Cargando modelo desde: {model_uri}")
        model = mlflow.pyfunc.load_model(model_uri)
        logging.info(f"Modelo cargado correctamente")

        # Resto del código con logs adicionales...
    except Exception as e:
        logging.error(f"Error durante la inicialización: {str(e)}", exc_info=True)
        raise
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(request: Request):
    global model, scaler, encoders
    start = time.time()
    data = await request.json()
    df = pd.DataFrame([data])

    # Apply label encoders
    for col, le in encoders.items():
        if col in df.columns:
            df[col] = le.transform(df[col])

    # Scale features
    df_scaled = scaler.transform(df)

    # Predict using MLflow model
    prediction = model.predict(df_scaled)
    duration = time.time() - start
    metrics["total_predictions"] += 1
    logging.info(f"Prediction: input={data}, output={prediction.tolist()}, time={duration:.3f}s")
    
    return {"prediction": prediction.tolist()}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics_endpoint():
    return f'total_predictions {metrics["total_predictions"]}\n'
