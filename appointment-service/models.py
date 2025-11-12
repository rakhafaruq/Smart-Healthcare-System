from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inisialisasi SQLAlchemy
db = SQLAlchemy()

class AppointmentModel(db.Model):
    __tablename__ = 'appointments'

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # ID ini merujuk ke service lain (patient-service & doctor-service)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    
    appointment_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Scheduled') # Contoh: Scheduled, Completed, Canceled
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Appointment {self.appointment_id} - Patient: {self.patient_id}>"

    # Helper function untuk mengubah object ke format JSON
    def to_json(self):
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_datetime': self.appointment_datetime.isoformat(),
            'status': self.status,
            'reason': self.reason,
            'created_at': self.created_at.isoformat()
        }