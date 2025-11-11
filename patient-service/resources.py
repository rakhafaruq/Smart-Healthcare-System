# patient-service/resources.py

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required
from models import db, PatientModel
from sqlalchemy.exc import IntegrityError
import datetime

# --- Parser untuk Data Pasien (Validasi Input) ---
patient_parser = reqparse.RequestParser()
patient_parser.add_argument('name', type=str, required=True, help="Nama tidak boleh kosong")
patient_parser.add_argument('birth_date', type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(), required=True, help="Format tanggal lahir YYYY-MM-DD")
patient_parser.add_argument('phone', type=str, required=False)

# --- Resource untuk /patients/<string:patient_id> ---
class PatientResource(Resource):
    
    def get(self, patient_id):
        """ GET /patients/<id> - Mendapatkan data pasien spesifik """
        patient = PatientModel.query.get(patient_id)
        if not patient:
            return {'message': 'Pasien tidak ditemukan'}, 404
        return patient.to_json(), 200

    def put(self, patient_id):
        """ PUT /patients/<id> - Memperbarui data pasien """
        patient = PatientModel.query.get(patient_id)
        if not patient:
            return {'message': 'Pasien tidak ditemukan'}, 404
            
        data = patient_parser.parse_args()
        patient.name = data['name']
        patient.birth_date = data['birth_date']
        patient.phone = data['phone']
        
        db.session.commit()
        return {'message': 'Data pasien berhasil diperbarui', 'data': patient.to_json()}, 200

    def delete(self, patient_id):
        """ DELETE /patients/<id> - Menghapus data pasien """
        patient = PatientModel.query.get(patient_id)
        if not patient:
            return {'message': 'Pasien tidak ditemukan'}, 404
            
        db.session.delete(patient)
        db.session.commit()
        return {'message': 'Pasien berhasil dihapus'}, 200

# --- Resource untuk /patients ---
class PatientListResource(Resource):

    def get(self):
        """ GET /patients - Mendapatkan semua data pasien """
        patients = PatientModel.query.all()
        return [p.to_json() for p in patients], 200


    def post(self):
        """ POST /patients - Membuat data pasien baru """
        data = patient_parser.parse_args()
        

        new_patient = PatientModel(
            name=data['name'],
            birth_date=data['birth_date'],
            phone=data['phone']
        )
        
        try:
            db.session.add(new_patient)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Gagal menambahkan pasien'}, 500
            
        return {'message': 'Pasien baru berhasil ditambahkan', 'data': new_patient.to_json()}, 201

# --- Resource untuk /login (Mendapatkan Token) ---
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str, required=True)
auth_parser.add_argument('password', type=str, required=True)

class AuthResource(Resource):
    def post(self):
        """ POST /login - Mendapatkan token JWT untuk testing """
        data = auth_parser.parse_args()
        # SIMULASI: Dalam aplikasi nyata, cek username/password ke DB
        if data['username'] == 'admin' and data['password'] == 'password':
            # Buat token untuk identitas 'admin'
            access_token = create_access_token(identity='admin_user', expires_delta=datetime.timedelta(hours=1))
            return {'access_token': access_token}, 200
        
        return {'message': 'Kredensial salah'}, 401