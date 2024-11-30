from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    dob = Column(Date)
    medical_history = Column(Text)
    doctors = relationship("DoctorPatient", back_populates="patient")

class LabResult(Base):
    __tablename__ = "lab_results"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    result = Column(Text)
    patient = relationship("Patient", back_populates="lab_results")

Patient.lab_results = relationship("LabResult", back_populates="patient", cascade="all, delete")
