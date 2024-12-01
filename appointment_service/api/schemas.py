from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    doctor_availability: str
    status: str
    reason: Optional[str]

class Appointment(AppointmentCreate):
    id: int

    class Config:
        orm_mode = True
