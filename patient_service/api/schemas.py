from pydantic import BaseModel
from typing import List, Optional

class LabResultCreate(BaseModel):
    result: str

class PatientCreate(BaseModel):
    name: str
    dob: str
    medical_history: Optional[str]

class Patient(BaseModel):
    id: int
    name: str
    dob: str
    medical_history: Optional[str]

    class Config:
        orm_mode = True

class PatientDetail(Patient):
    lab_results: List[LabResultCreate] = []
