from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    reason: Optional[str]

class Appointment(AppointmentCreate):
    id: int

    class Config:
        orm_mode = True
