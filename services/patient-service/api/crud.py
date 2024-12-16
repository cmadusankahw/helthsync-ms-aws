from sqlalchemy.orm import Session
from . import models
from . import schemas

def create_patient(db: Session, patient: schemas.Patient):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def update_patient(db: Session, patient_id: int, patient: schemas.PatientCreate):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return None
    for key, value in patient.model_dump().items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def add_lab_result(db: Session, patient_id: int, lab_result: schemas.LabResultCreate):
    db_result = models.LabResult(patient_id=patient_id, lab_name=lab_result.lab_name, result=lab_result.result)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def add_prescription(db: Session, patient_id: int, prescription: schemas.PrescriptionCreate):
    db_result = models.Prescription(patient_id=patient_id, medicines=prescription.medicines, cost = prescription.cost)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
