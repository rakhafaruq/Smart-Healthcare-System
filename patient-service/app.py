# patient-service/app.py
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from resources import PatientResource, PatientListResource, AuthResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    api = Api(app, prefix="/v1") 

    # --- Otomatis membuat tabel ---
    with app.app_context():
        # db.drop_all() # Hati-hati: akan menghapus semua data
        db.create_all()

    # --- Daftarkan Endpoints (Resources) ---
    api.add_resource(AuthResource, '/login')
    api.add_resource(PatientListResource, '/patients')
    api.add_resource(PatientResource, '/patients/<int:patient_id>')

    return app

# --- Entry point untuk menjalankan server ---
if __name__ == '__main__':
    app = create_app()
    # Jalankan di port 5001
    app.run(port=5001, debug=True, host='0.0.0.0')