from fastapi import FastAPI
from api.routers import app as appointment_app

app = FastAPI(docs_url="/api/v1/appointment/docs")

app.include_router(appointment_app, prefix='/api/v1/appointment', tags=['appointment'])