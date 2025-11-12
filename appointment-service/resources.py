from flask_restful import Resource, reqparse
from models import db, AppointmentModel
from sqlalchemy.exc import IntegrityError
import datetime

# --- Parser untuk Data Appointment (Validasi Input) ---
appointment_parser = reqparse.RequestParser()
appointment_parser.add_argument('patient_id', type=int, required=True, help="patient_id tidak boleh kosong")
appointment_parser.add_argument('doctor_id', type=int, required=True, help="doctor_id tidak boleh kosong")
appointment_parser.add_argument('appointment_datetime', 
                                type=lambda x: datetime.datetime.fromisoformat(x), 
                                required=True, 
                                help="Format ISO Datetime (YYYY-MM-DDTHH:MM:SS)")
appointment_parser.add_argument('status', type=str, required=False, default='Scheduled')
appointment_parser.add_argument('reason', type=str, required=False)

# --- Resource untuk /appointments/<int:appointment_id> ---
class AppointmentResource(Resource):
    
    def get(self, appointment_id):
        """ GET /appointments/<id> - Mendapatkan data appointment spesifik """
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment tidak ditemukan'}, 404
        return appointment.to_json(), 200

    def put(self, appointment_id):
        """ PUT /appointments/<id> - Memperbarui data (misal: status atau jadwal) """
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment tidak ditemukan'}, 404
            
        data = appointment_parser.parse_args()
        
        # Hanya update field yang relevan
        appointment.patient_id = data['patient_id']
        appointment.doctor_id = data['doctor_id']
        appointment.appointment_datetime = data['appointment_datetime']
        appointment.status = data['status']
        appointment.reason = data['reason']
        
        db.session.commit()
        return {'message': 'Data appointment berhasil diperbarui', 'data': appointment.to_json()}, 200

    def delete(self, appointment_id):
        """ DELETE /appointments/<id> - Menghapus (membatalkan) appointment """
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment tidak ditemukan'}, 404
            
        db.session.delete(appointment)
        db.session.commit()
        return {'message': 'Appointment berhasil dihapus'}, 200

# --- Resource untuk /appointments ---
class AppointmentListResource(Resource):

    def get(self):
        """ GET /appointments - Mendapatkan semua data appointment """
        appointments = AppointmentModel.query.all()
        return [a.to_json() for a in appointments], 200


    def post(self):
        """ POST /appointments - Membuat data appointment baru """
        data = appointment_parser.parse_args()
        
        new_appointment = AppointmentModel(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_datetime=data['appointment_datetime'],
            status=data['status'],
            reason=data['reason']
        )
        
        try:
            db.session.add(new_appointment)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Gagal menambahkan appointment'}, 500
            
        return {'message': 'Appointment baru berhasil ditambahkan', 'data': new_appointment.to_json()}, 201