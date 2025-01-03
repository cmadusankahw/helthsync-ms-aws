from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db, engine
from api import schemas, crud, models

# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = APIRouter()

@app.post("/create")
async def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    try:
        patient = crud.create_patient(db, patient)
        return {"status":status.HTTP_200_OK, "message": f"Patient {patient.id} created"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to create patient: {str(e)}"
        }

@app.get("/get/{patient_id}")
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    try:
        db_patient = crud.get_patient(db, patient_id)
        if db_patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return {"status":status.HTTP_200_OK, "message": db_patient}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to create patient: {str(e)}"
        }

@app.put("/update/{patient_id}")
async def update_patient(patient_id: int, patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    try:
        updated_patient = crud.update_patient(db, patient_id, patient)
        if updated_patient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return {"status":status.HTTP_200_OK, "message": f"Patient {patient_id} is updated"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to create patient: {str(e)}"
        }

@app.post("/lab-results/add/{patient_id}")
async def add_lab_result(patient_id: int, lab_result: schemas.LabResultCreate, db: Session = Depends(get_db)):
    try:
        lab = crud.add_lab_result(db, patient_id, lab_result)
        return {"status":status.HTTP_200_OK, "message": f"Lab Result created with ID: {lab.id}"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to unlink doctor: {str(e)}"
        }

@app.post("/prescription/add/{patient_id}")
async def add_prescription(patient_id: int, prescription: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    try:
        pc = crud.add_lab_result(db, patient_id, prescription)
        return {"status":status.HTTP_200_OK, "message": f"Lab Result created with ID: {pc.id}"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to unlink doctor: {str(e)}"
        }
    
@app.get("/health")
async def get_health():
    return {"status": status.HTTP_200_OK, "message": {"status": "ok"}}