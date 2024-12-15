from sqlalchemy.orm import Session
from api.models import Doctor, Patient, Appointment
from api.schemas import AggregateReport
from collections import defaultdict

def generate_aggregate_report(db: Session):
    appointments = db.query(Appointment).all()
    doctors = db.query(Doctor).all()

    appointments_per_doctor = defaultdict(int)
    frequency_of_appointments = defaultdict(int)
    common_conditions_by_specialty = defaultdict(list)

    for appointment in appointments:
        appointments_per_doctor[appointment.doctor.name] += 1
        date_key = appointment.appointment_time.strftime("%Y-%m-%d")
        frequency_of_appointments[date_key] += 1

        specialty = appointment.doctor.specialty
        common_conditions_by_specialty[specialty].append(appointment.reason)

    return AggregateReport(
        appointments_per_doctor=dict(appointments_per_doctor),
        frequency_of_appointments=dict(frequency_of_appointments),
        common_conditions_by_specialty={k: list(set(v)) for k, v in common_conditions_by_specialty.items()},
    )
