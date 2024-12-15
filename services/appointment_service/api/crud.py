from sqlalchemy.orm import Session

from . import models
from . import schemas

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def update_appointment(db: Session, appointment_id: int, appointment: schemas.AppointmentCreate):
    db_app = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_app:
        return None
    for key, value in appointment.model_dump().items():
        setattr(db_app, key, value)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
        return True
    return False
