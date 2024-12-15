from fastapi import FastAPI
from api.routers import app as notification_App

app = FastAPI(docs_url="/api/v1/notification/docs")

app.include_router(notification_App, prefix='/api/v1/notification', tags=['notification'])