from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class AppointmentSummary(BaseModel):
    doctor_name: str
    patient_name: str
    appointment_time: datetime
    reason: str

class AggregateReport(BaseModel):
    appointments_per_doctor: Dict[str, int]
    frequency_of_appointments: Dict[str, int]  # e.g., daily, weekly counts
    common_conditions_by_specialty: Dict[str, List[str]]
