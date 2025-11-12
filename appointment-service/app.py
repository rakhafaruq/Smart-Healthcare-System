from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from models import db
from resources import AppointmentResource, AppointmentListResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi extensions
    db.init_app(app)
    CORS(app)
    
    # PENTING: Tidak ada JWTManager di sini
    
    api = Api(app, prefix="/v1") 

    # --- Otomatis membuat tabel ---
    with app.app_context():
        # db.drop_all() # Hati-hati: akan menghapus semua data
        db.create_all()

    # --- Daftarkan Endpoints (Resources) ---
    api.add_resource(AppointmentListResource, '/appointments')
    api.add_resource(AppointmentResource, '/appointments/<int:appointment_id>')

    return app

# --- Entry point untuk menjalankan server ---
if __name__ == '__main__':
    app = create_app()
    # Jalankan di port yang diambil dari config
    app.run(port=app.config['PORT'], debug=True, host='0.0.0.0')