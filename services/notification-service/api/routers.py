from fastapi import APIRouter, HTTPException, Depends, status, FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta, timezone
import redis
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import json
from api import schemas
from api.utils import send_email

# Connect to Redis (use AWS Elasticache in production)
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Utility: Schedule notification in Redis
def schedule_notification(reminder: schemas.AppointmentReminder):
    reminder_time = datetime.strptime(reminder.reminder_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    delay = (reminder_time - datetime.now()).total_seconds()
    if delay <= 0:
        raise HTTPException(status_code=400, detail="Reminder time must be in the future")

    # Store the notification in Redis
    redis_key = f"notification:{reminder.appointment_id}"
    redis_client.setex(redis_key, timedelta(seconds=delay), json.dumps(reminder.model_dump()))
    return redis_key


# Background notification worker
def notification_worker():
    keys = redis_client.keys("notification:*")
    for key in keys:
        reminder = json.loads(redis_client.get(key))
        if datetime.now() >= datetime.strptime(reminder['reminder_time'], "%Y-%m-%dT%H:%M:%S.%fZ"):
            send_email(
                to_email=reminder['patient_email'],
                subject="Appointment Reminder",
                body=f"Dear Patient, you have an upcoming appointment on {reminder['appointment_time']}."
            )
            print("email sent")
            redis_client.delete(key)
        print(f"Appointment reminder time is: {reminder['reminder_time']}")

# Lifespan management for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(notification_worker, 'interval', seconds=30)
    scheduler.start()
    
    print("Scheduler started.")
    
    try:
        yield
    finally:
        scheduler.shutdown()
        print("Scheduler stopped.")

# FastAPI application
app = APIRouter(lifespan=lifespan)

# Endpoint: Schedule a reminder
@app.post("/schedule", response_model=schemas.NotificationResponse)
async def schedule_appointment_reminder(reminder: schemas.AppointmentReminder):
    try:
        redis_key = schedule_notification(reminder)
        return {
            "status": status.HTTP_200_OK,
            "message": f"Notification scheduled with key {redis_key}"
        }
    except HTTPException as e:
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": f"Failed to schedule notification: {e.detail}"
        }

# Endpoint: List all scheduled reminders
@app.get("/scheduled-list")
async def list_scheduled_notifications():
    try:
        keys = redis_client.keys("notification:*")
        notifications = [json.loads(redis_client.get(key)) for key in keys]
        return {
            "status": status.HTTP_200_OK,
            "message": notifications
        }
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to schedule notification: {e.detail}"
        }

@app.get("/health")
async def get_health():
    return {"status": status.HTTP_200_OK, "message": {"status": "ok"}}