from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dob = Column(Date)
    age = Column(Integer)
    medical_history = Column(Text)
    doctor_id = Column(Integer)

class LabResult(Base):
    __tablename__ = "lab_results"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    lab_name = Column(String)
    result = Column(Text)

class Prescription(Base):
    __tablename__ = "lab_results"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    medicines = Column(Text)
    cost = Column(float)

LabResult.patient_id = relationship("Patient", back_populates="id", cascade="all, delete")

Prescription.patient_id = relationship("Patient", back_populates="id", cascade="all, delete")