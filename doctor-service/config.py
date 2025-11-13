# doctor-service/config.py
import os
from dotenv import load_dotenv

# Cari file .env di root project (satu level di atas folder service)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class Config:
    # --- Konfigurasi MySQL ---
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')

    # DB untuk doctor/staff
    DB_NAME = os.getenv('DB_NAME_STAFF', 'db_staff')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # --- Konfigurasi JWT ---
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
