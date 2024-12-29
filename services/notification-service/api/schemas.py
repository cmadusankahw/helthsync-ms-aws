from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Pydantic models for request validation
class AppointmentReminder(BaseModel):
    patient_id: int
    appointment_id: int
    patient_email: str
    appointment_time: str
    reminder_time: str

class NotificationResponse(BaseModel):
    status: int
    message: str