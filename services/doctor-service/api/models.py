from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from api.database import Base


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialty = Column(String)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dob = Column(Date)
    age = Column(Integer)
    medical_history = Column(Text)
    doctor_id = Column(Integer)

class DoctorPatient(Base):
    __tablename__ = "doctor_patient"
    doctor_id = Column(Integer, ForeignKey("doctors.id"), primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), primary_key=True)
