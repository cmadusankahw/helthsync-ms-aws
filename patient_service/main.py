from fastapi import FastAPI
from api.routers import app as patient_app

app = FastAPI(docs_url="/api/v1/patient/docs")

app.include_router(patient_app, prefix='/api/v1/patient', tags=['patient'])