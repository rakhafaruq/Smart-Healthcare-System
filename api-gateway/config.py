# api-gateway/config.py

import os
from dotenv import load_dotenv

# Temukan file .env di folder root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY tidak ditemukan di .env")

    # Definisikan alamat semua backend service Anda
    SERVICES = {
        'patient': os.getenv('PATIENT_SERVICE_URL'),
        'staff': os.getenv('STAFF_SERVICE_URL'),
        'appointment': os.getenv('APPOINTMENT_SERVICE_URL'),
        'record': os.getenv('MEDICAL_RECORD_SERVICE_URL')
    }