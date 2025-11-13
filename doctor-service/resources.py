# doctor-service/resources.py

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required
from models import db, DoctorModel
from sqlalchemy.exc import IntegrityError
import datetime

# --- Parser untuk data Dokter ---
doctor_parser = reqparse.RequestParser()
doctor_parser.add_argument('name', type=str, required=True, help="Nama dokter tidak boleh kosong")
doctor_parser.add_argument('specialization', type=str, required=False, help="Spesialisasi dokter (opsional)")
doctor_parser.add_argument('phone', type=str, required=False, help="Nomor telepon dokter (opsional)")

# --- Resource untuk /doctors/<int:doctor_id> ---
class DoctorResource(Resource):
    @jwt_required(optional=True)
    def get(self, doctor_id):
        """GET /doctors/<doctor_id> - Ambil detail 1 dokter"""
        doctor = DoctorModel.query.get(doctor_id)
        if not doctor:
            return {'message': 'Dokter tidak ditemukan'}, 404
        return doctor.to_json(), 200

    @jwt_required()
    def put(self, doctor_id):
        """PUT /doctors/<doctor_id> - Update data dokter"""
        doctor = DoctorModel.query.get(doctor_id)
        if not doctor:
            return {'message': 'Dokter tidak ditemukan'}, 404

        data = doctor_parser.parse_args()
        doctor.name = data['name']
        doctor.specialization = data.get('specialization')
        doctor.phone = data.get('phone')

        try:
            db.session.commit()
            return doctor.to_json(), 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Terjadi kesalahan saat meng-update data dokter'}, 500

    @jwt_required()
    def delete(self, doctor_id):
        """DELETE /doctors/<doctor_id> - Hapus data dokter"""
        doctor = DoctorModel.query.get(doctor_id)
        if not doctor:
            return {'message': 'Dokter tidak ditemukan'}, 404

        try:
            db.session.delete(doctor)
            db.session.commit()
            return {'message': 'Dokter berhasil dihapus'}, 200
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Terjadi kesalahan saat menghapus dokter'}, 500

# --- Resource untuk /doctors ---
class DoctorListResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        """
        GET /doctors - Ambil list semua dokter.
        Opsional: filter by specialization ?specialization=Umum
        """
        parser = reqparse.RequestParser()
        parser.add_argument('specialization', type=str, required=False)
        args = parser.parse_args()

        query = DoctorModel.query
        if args.get('specialization'):
            query = query.filter(DoctorModel.specialization == args['specialization'])

        doctors = query.all()
        return [d.to_json() for d in doctors], 200

    @jwt_required()
    def post(self):
        """POST /doctors - Tambah dokter baru"""
        data = doctor_parser.parse_args()

        new_doctor = DoctorModel(
            name=data['name'],
            specialization=data.get('specialization'),
            phone=data.get('phone')
        )

        try:
            db.session.add(new_doctor)
            db.session.commit()
            return new_doctor.to_json(), 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Terjadi kesalahan saat menyimpan data dokter'}, 500

# --- Parser untuk Auth ---
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str, required=True)
auth_parser.add_argument('password', type=str, required=True)

class AuthResource(Resource):
    def post(self):
        """POST /login - Mendapatkan token JWT untuk testing"""
        data = auth_parser.parse_args()

        # SIMULASI: production seharusnya cek user ke tabel users/staff di DB
        if data['username'] == 'admin' and data['password'] == 'password':
            access_token = create_access_token(
                identity='admin_user',
                expires_delta=datetime.timedelta(hours=1)
            )
            return {'access_token': access_token}, 200

        return {'message': 'Kredensial salah'}, 401
