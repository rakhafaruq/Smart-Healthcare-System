# api-gateway/app.py

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from config import Config
import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi CORS dan JWT
CORS(app)
jwt = JWTManager(app)

# === 1. ENDPOINT AUTENTIKASI (LOGIN) ===
# Endpoint ini TIDAK memerlukan token
@app.route('/auth/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # --- Validasi Pengguna ---
    # !! PENTING !!
    # Dalam proyek nyata, Anda akan memvalidasi ini ke 'staff-service'
    # atau 'patient-service' untuk memeriksa username/password di DB.
    # Untuk saat ini, kita hardcode 'admin'/'password' untuk testing.
    if username != 'admin' or password != 'password':
        return jsonify({"message": "Username atau password salah"}), 401

    # Buat token jika kredensial benar
    access_token = create_access_token(
        identity=username, 
        expires_delta=datetime.timedelta(hours=1)
    )
    return jsonify(access_token=access_token), 200

# === 2. PROXY KE PATIENT-SERVICE ===
# Endpoint ini dan semua endpoint /api/ lainnya WAJIB menggunakan token
@app.route('/api/patients', methods=['GET', 'POST'])
@app.route('/api/patients/<path:path>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required() # <--- INI KUNCINYA
def proxy_patient(path=""):
    # Dapatkan URL service dari config
    service_url = app.config['SERVICES']['patient']
    
    # Gabungkan URL
    url = f"{service_url}/v1/patients"

    if path: 
        url = f"{url}/{path}"

    # Teruskan request ke patient-service
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            json=request.get_json(silent=True),
            params=request.args
        )
        # Kembalikan respons dari service
        return (response.content, response.status_code, response.headers.items())
    
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Patient Service tidak dapat dihubungi"}), 503

# === 3. PROXY KE STAFF-SERVICE (Placeholder) ===
@app.route('/api/staff', methods=['GET', 'POST'])
@app.route('/api/staff/<path:path>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def proxy_staff(path=""):
    service_url = app.config['SERVICES']['staff']   
    url = f"{service_url}/v1/staff" 
    
    if path:
        url = f"{url}/{path}"

    # (Kode proxy sama seperti di atas...)
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            json=request.get_json(silent=True),
            params=request.args
        )
        return (response.content, response.status_code, response.headers.items())
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Staff Service tidak dapat dihubungi"}), 503

# === 4. PROXY KE APPOINTMENT-SERVICE ===
@app.route('/api/appointments', methods=['GET', 'POST'])
@app.route('/api/appointments/<path:path>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def proxy_appointment(path=""):
    service_url = app.config['SERVICES']['appointment']    
    url = f"{service_url}/v1/appointments" 
    
    if path:
        url = f"{url}/{path}"

    try:
        response = requests.request(
            method=request.method,
            url=url,
            # Meneruskan semua header kecuali header Host, agar tidak ada konflik
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            json=request.get_json(silent=True),
            params=request.args
        )
        # Kembalikan respons dari service
        return (response.content, response.status_code, response.headers.items())
    
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Appointment Service tidak dapat dihubungi"}), 503


# === 5. PROXY KE MEDICAL-RECORD-SERVICE ===
@app.route('/api/records', methods=['GET', 'POST'])
@app.route('/api/records/<path:path>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def proxy_record(path=""):
    service_url = app.config['SERVICES']['record']
    url = f"{service_url}/v1/records" 
    
    if path:
        url = f"{url}/{path}"
    print(f"Redirecting request to: {url}")
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            json=request.get_json(silent=True),
            params=request.args
        )
        return (response.content, response.status_code, response.headers.items())
    
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Medical Record Service tidak dapat dihubungi"}), 503

# === Entry Point ===
if __name__ == '__main__':
    # Jalankan API Gateway di port 5000
    app.run(port=5000, debug=True, host='0.0.0.0')