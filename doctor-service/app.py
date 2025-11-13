# doctor-service/app.py

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from resources import DoctorResource, DoctorListResource, AuthResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    api = Api(app, prefix="/v1") 

    # Buat tabel kalau belum ada
    with app.app_context():
        # db.drop_all()  # Hati-hati, hanya untuk reset saat development
        db.create_all()

    # --- Daftarkan Endpoints ---
    api.add_resource(AuthResource, '/login')
    api.add_resource(DoctorListResource, '/staff')
    api.add_resource(DoctorResource, '/staff/<int:doctor_id>')

    return app

if __name__ == '__main__':
    app = create_app()
    # Jalankan di port 5002 untuk doctor-service
    app.run(port=5002, debug=True, host='0.0.0.0')
