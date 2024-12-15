from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from api.database import Base


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialty = Column(String)

class DoctorPatient(Base):
    __tablename__ = "doctor_patient"
    doctor_id = Column(Integer, ForeignKey("doctors.id"), primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), primary_key=True)

DoctorPatient.doctor_id = relationship("Doctor", back_populates="id", cascade="all, delete")