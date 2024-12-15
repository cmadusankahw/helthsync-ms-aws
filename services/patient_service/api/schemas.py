from pydantic import BaseModel
from typing import List, Optional

class PatientCreate(BaseModel):
    name: str
    dob: str
    age: int
    medical_history: Optional[str]
    doctor_id: int

class Patient(PatientCreate):
    id: int

    class Config:
        orm_mode = True

class LabResultCreate(BaseModel):
    patennt_id: int
    lab_name: str
    result: str

class LabResult(LabResultCreate):
    id: int

    class Config:
        orm_mode = True

class PrescriptionCreate(BaseModel):
    patent_id: int
    medicines: str
    cost: float

class Prescription(PrescriptionCreate):
    id: int

    class Config:
        orm_mode = True

