# record-service/resources.py
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token  # , jwt_required
from sqlalchemy.exc import IntegrityError
from models import db, MedicalRecord

# ---------- Parsers ----------
record_parser = reqparse.RequestParser()
record_parser.add_argument("patient_id", type=int, required=True, help="patient_id wajib diisi")
record_parser.add_argument("doctor_id", type=int, required=False)
record_parser.add_argument("appointment_id", type=int, required=False)
record_parser.add_argument("diagnosis", type=str, required=True, help="diagnosis wajib diisi")
record_parser.add_argument("prescriptions", type=str, required=False)
record_parser.add_argument("notes", type=str, required=False)

list_parser = reqparse.RequestParser()
list_parser.add_argument("page", type=int, required=False, default=1)
list_parser.add_argument("per_page", type=int, required=False, default=10)
list_parser.add_argument("patient_id", type=int, required=False)

# ---------- Resources ----------
class MedicalRecordListResource(Resource):
    # @jwt_required()  # aktifkan jika mau proteksi JWT
    def get(self):
        """GET /records?patient_id=&page=&per_page= -> List records (bisa filter by patient_id)"""
        args = list_parser.parse_args()
        q = MedicalRecord.query
        if args["patient_id"]:
            q = q.filter_by(patient_id=args["patient_id"])

        pagination = q.order_by(MedicalRecord.created_at.desc()).paginate(
            page=args["page"], per_page=args["per_page"], error_out=False
        )
        return {
            "items": [r.to_json() for r in pagination.items],
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
        }, 200

    # @jwt_required()
    def post(self):
        """POST /records -> Create medical record"""
        data = record_parser.parse_args()
        rec = MedicalRecord(
            patient_id=data["patient_id"],
            doctor_id=data.get("doctor_id"),
            appointment_id=data.get("appointment_id"),
            diagnosis=data["diagnosis"],
            prescriptions=data.get("prescriptions"),
            notes=data.get("notes"),
        )
        try:
            db.session.add(rec)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "Gagal menambahkan medical record"}, 500
        return {"message": "Medical record berhasil dibuat", "data": rec.to_json()}, 201


class MedicalRecordResource(Resource):
    # @jwt_required()
    def get(self, record_id: int):
        """GET /records/<id> -> Detail"""
        rec = MedicalRecord.query.get(record_id)
        if not rec:
            return {"message": "Medical record tidak ditemukan"}, 404
        return rec.to_json(), 200

    # @jwt_required()
    def put(self, record_id: int):
        """PUT /records/<id> -> Update"""
        rec = MedicalRecord.query.get(record_id)
        if not rec:
            return {"message": "Medical record tidak ditemukan"}, 404

        data = record_parser.parse_args()
        rec.patient_id = data["patient_id"]
        rec.doctor_id = data.get("doctor_id")
        rec.appointment_id = data.get("appointment_id")
        rec.diagnosis = data["diagnosis"]
        rec.prescriptions = data.get("prescriptions")
        rec.notes = data.get("notes")
        db.session.commit()
        return {"message": "Medical record diperbarui", "data": rec.to_json()}, 200

    # @jwt_required()
    def delete(self, record_id: int):
        """DELETE /records/<id> -> Hapus"""
        rec = MedicalRecord.query.get(record_id)
        if not rec:
            return {"message": "Medical record tidak ditemukan"}, 404
        db.session.delete(rec)
        db.session.commit()
        return {"message": "Medical record dihapus"}, 200


class MedicalRecordByPatientResource(Resource):
    # @jwt_required()
    def get(self, patient_id: int):
        """GET /records/patient/<patient_id> -> Semua rekam medis milik pasien"""
        recs = (
            MedicalRecord.query.filter_by(patient_id=patient_id)
            .order_by(MedicalRecord.created_at.desc())
            .all()
        )
        return {"items": [r.to_json() for r in recs], "total": len(recs)}, 200


# ---------- Auth sederhana untuk testing ----------
auth_parser = reqparse.RequestParser()
auth_parser.add_argument("username", type=str, required=True)
auth_parser.add_argument("password", type=str, required=True)

class AuthResource(Resource):
    def post(self):
        """POST /login -> Ambil token JWT (dummy)"""
        data = auth_parser.parse_args()
        if data["username"] == "admin" and data["password"] == "password":
            token = create_access_token(identity="admin_user")
            return {"access_token": token}, 200
        return {"message": "Kredensial salah"}, 401
