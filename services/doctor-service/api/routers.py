from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db, engine
from api import schemas, crud, models

# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = APIRouter()

@app.post("/create")
async def create_doctor(doctor: schemas.Doctor, db: Session = Depends(get_db)):
    try:
        doc = crud.create_doctor(db, doctor)
        return {"status":status.HTTP_200_OK, "message": f"Doctor {doc.id} Created"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to create doctor: {str(e)}"
        }

@app.get("/get/{doctor_id}")
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    try:
        db_doc = crud.get_doctor(db, doctor_id)
        if not db_doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return {"status":status.HTTP_200_OK, "message": db_doc}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to retrieve doctor: {str(e)}"
        }
    
@app.post("/update/{doctor_id}")
async def update_doctor(doctor_id: int, doctor:schemas.DoctorCreate, db: Session = Depends(get_db)):
    try:
        db_doc = crud.update_doctor(db, doctor_id, doctor)
        if not db_doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return {"status": status.HTTP_200_OK, "message": f"Doctor {db_doc.id} Updated"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to retrieve Doctor: {str(e)}"
        }

@app.delete("/delete/{doctor_id}")
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    try:
        if not crud.delete_doctor(db, doctor_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return {"status":status.HTTP_200_OK, "message": f"Doctor {doctor_id} removed"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to remove doctor: {str(e)}"
        }

@app.post("/link/{doctor_id}/patient/{patient_id}")
async def link_patient(doctor_id: int, patient_id: int, db: Session = Depends(get_db)):
    try:
        db.add(models.DoctorPatient(doctor_id=doctor_id, patient_id=patient_id))
        db.commit()
        return {"status":status.HTTP_200_OK, "message": f"Patient {patient_id} linked to Doctor {doctor_id}"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to link doctor: {str(e)}"
        }

@app.delete("/unlink/{doctor_id}/patient/{patient_id}")
async def unlink_patient(doctor_id: int, patient_id: int, db: Session = Depends(get_db)):
    try:
        db.query(models.DoctorPatient).filter_by(doctor_id=doctor_id, patient_id=patient_id).delete()
        db.commit()
        return {"status":status.HTTP_200_OK, "message": f"Patient {patient_id} unlinked from Doctor {doctor_id}"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to unlink doctor: {str(e)}"
        }

@app.get("/health")
async def get_health():
    return {"status": status.HTTP_200_OK, "message": {"status": "ok"}}