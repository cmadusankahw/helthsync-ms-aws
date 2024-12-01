from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DoctorCreate(BaseModel):
    name: str
    speciality: str

class Doctor(DoctorCreate):
    id: int

    class Config:
        orm_mode = True

class DoctorPatient(BaseModel):
    doctor_id: int
    patient_id: int