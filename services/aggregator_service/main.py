from fastapi import FastAPI
from api.routers import app as aggregate_app

app = FastAPI(docs_url="/api/v1/aggregate/docs")

app.include_router(aggregate_app, prefix='/api/v1/aggregate', tags=['aggregate'])