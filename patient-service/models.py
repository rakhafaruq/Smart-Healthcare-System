# patient-service/models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inisialisasi SQLAlchemy
db = SQLAlchemy()

class PatientModel(db.Model):
    __tablename__ = 'patients'

    # Definisikan kolom-kolom
    patient_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Patient {self.patient_id} - {self.name}>"

    # Helper function untuk mengubah object ke format JSON
    def to_json(self):
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'birth_date': self.birth_date.isoformat(), 
            'phone': self.phone,
            'created_at': self.created_at.isoformat()
        }
