import os
from dotenv import load_dotenv

# Mengambil file .env dari root folder (satu level di atas)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class Config:
    # --- Konfigurasi MySQL ---
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    # PENTING: Menggunakan database yang berbeda untuk service ini
    DB_NAME = os.getenv('DB_NAME_APPOINTMENT') 

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False # Set True jika ingin lihat query SQL

    # Mengatur port untuk service ini, default ke 5003 jika tidak ada di .env
    PORT = int(os.getenv('APPOINTMENT_SERVICE_PORT', 5003))