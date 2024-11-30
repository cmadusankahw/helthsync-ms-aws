from sqlalchemy.orm import Session
from . import models
from . import schemas

def create_doctor(db: Session, doctor: schemas.Doctor):
    dbt_doc = models.Doctor(**doctor.model_dump())
    db.add(dbt_doc)
    db.commit()
    db.refresh(dbt_doc)
    return dbt_doc

def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

def delete_doctor(db: Session, doctor_id: int):
    dbt_doc = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if dbt_doc:
        db.delete(dbt_doc)
        db.commit()
        return True
    return False
