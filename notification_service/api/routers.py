from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import redis
from apscheduler.schedulers.background import BackgroundScheduler
import json
from . import schemas
from contextlib import asynccontextmanager

# Connect to Redis (use AWS Elasticache in production)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Utility: Schedule notification in Redis
def schedule_notification(reminder: schemas.AppointmentReminder):
    delay = (reminder.reminder_time - datetime.now()).total_seconds()
    if delay <= 0:
        raise HTTPException(status_code=400, detail="Reminder time must be in the future")

    # Store the notification in Redis
    redis_key = f"notification:{reminder.appointment_id}"
    redis_client.setex(redis_key, timedelta(seconds=delay), json.dumps(reminder.dict()))
    return redis_key

# Utility: Mock sending email (can integrate AWS SES for production)
def send_email(to_email: str, subject: str, body: str):
    print(f"Sending email to {to_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")

# Background notification worker
def notification_worker():
    keys = redis_client.keys("notification:*")
    for key in keys:
        reminder = json.loads(redis_client.get(key))
        if datetime.now() >= datetime.fromisoformat(reminder['reminder_time']):
            send_email(
                to_email=reminder['patient_email'],
                subject="Appointment Reminder",
                body=f"Dear Patient, you have an upcoming appointment on {reminder['appointment_time']}."
            )
            redis_client.delete(key)

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
app = FastAPI(lifespan=lifespan)

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
@app.get("/scheduled-list", response_model=List[schemas.AppointmentReminder])
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
