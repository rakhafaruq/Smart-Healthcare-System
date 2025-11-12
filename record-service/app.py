# record-service/app.py
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from resources import (
    MedicalRecordResource,
    MedicalRecordListResource,
    MedicalRecordByPatientResource
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # Routes
    api = Api(app, prefix="/v1") 

    api.add_resource(MedicalRecordListResource, "/records")
    api.add_resource(MedicalRecordResource, "/records/<int:record_id>")
    api.add_resource(MedicalRecordByPatientResource, "/records/patient/<int:patient_id>") # endpoint untuk ambil token (opsional)

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok", "service": "record-service"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Membuat tabel jika belum ada
        db.create_all()
    app.run(host="0.0.0.0", port=5004, debug=True)
