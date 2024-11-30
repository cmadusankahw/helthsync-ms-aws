from fastapi import FastAPI
from api.routers import app as doctor_app

app = FastAPI(docs_url="/api/v1/doctor/docs")

app.include_router(doctor_app, prefix='/api/v1/doctor', tags=['doctor'])