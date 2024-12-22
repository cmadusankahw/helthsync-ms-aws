from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from api import crud, models, schemas
from api.database import get_db, engine

# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = APIRouter()

@app.post("/create")
async def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        app = crud.create_appointment(db, appointment)
        return {"status": status.HTTP_200_OK, "message": f"Appointment {app.id} Created"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to create appointment: {str(e)}"
        }

@app.get("/get/{appointment_id}")
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    try:
        db_appointment = crud.get_appointment(db, appointment_id)
        if not db_appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return {"status": status.HTTP_200_OK, "message": db_appointment}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to retrieve appointment: {str(e)}"
        }
    
@app.post("/update/{appointment_id}")
async def update_appointment(appointment_id: int, appointment:schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        db_appointment = crud.update_appointment(db, appointment_id, appointment)
        if not db_appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return {"status": status.HTTP_200_OK, "message": f"Appointment {db_appointment.id} Updated"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to retrieve appointment: {str(e)}"
        }


@app.delete("/delete/{appointment_id}")
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    try:
        if not crud.delete_appointment(db, appointment_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return {"status": status.HTTP_200_OK, "message": f"Appointment {appointment_id} deleted"}
    except HTTPException as e:
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Failed to remove appointment: {str(e)}"
        }


@app.get("/health")
async def get_health():
    return {"status": status.HTTP_200_OK, "message": {"status": "ok"}}
