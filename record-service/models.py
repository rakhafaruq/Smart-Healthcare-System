# record-service/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, nullable=False, index=True)
    doctor_id = db.Column(db.Integer, nullable=True, index=True)
    appointment_id = db.Column(db.Integer, nullable=True, index=True)

    diagnosis = db.Column(db.String(255), nullable=False)
    prescriptions = db.Column(db.Text, nullable=True)  # bisa JSON string / free text
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def to_json(self):
        return {
            "record_id": self.record_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_id": self.appointment_id,
            "diagnosis": self.diagnosis,
            "prescriptions": self.prescriptions,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
