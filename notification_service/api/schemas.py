from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Pydantic models for request validation
class AppointmentReminder(BaseModel):
    patient_id: int
    appointment_id: int
    patient_email: str
    appointment_time: datetime
    reminder_time: datetime

class NotificationResponse(BaseModel):
    status: int
    message: str