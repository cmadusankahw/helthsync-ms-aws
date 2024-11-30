from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Doctor(BaseModel):
    id: int
    name: str
    speciality: str

class DoctorPatient(BaseModel):
    doctor_id: int
    patient_id: int