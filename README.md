# Proyek UTS EAI: Smart Healthcare System

## 1. Deskripsi Singkat Proyek

Proyek ini adalah implementasi arsitektur *microservices* sederhana untuk sistem manajemen rumah sakit (Smart Healthcare System). Proyek ini terdiri dari 4 layanan *backend* independen (Patient, Staff, Appointment, Record), 1 API Gateway untuk autentikasi dan *routing*, dan 1 *frontend* web sederhana sebagai *consumer*.

Sistem ini memenuhi *requirement* untuk integrasi layanan, di mana *backend service* dapat saling memanggil untuk validasi data, dan *frontend* mengonsumsi semua data melalui *gateway* yang aman (JWT).

* **Topik:** Smart Healthcare System
* **Teknologi:** Python Flask, MySQL, Flask-JWT-Extended, HTML/CSS/JavaScript

---

## 2. Arsitektur Sistem

Arsitektur mengikuti pola `Client → API Gateway → Services → Database` yang diwajibkan.

* **Client (Frontend):** Aplikasi web statis (`login.html`, `dashboard.html`) yang hanya berkomunikasi dengan API Gateway.
* **API Gateway:** Bertindak sebagai pintu masuk tunggal (Port 5000). Bertanggung jawab untuk autentikasi (membuat token JWT di `/auth/login`) dan me-routing permintaan ke *service* yang sesuai.
* **Services:** 4 layanan independen yang masing-masing memiliki *database*-nya sendiri:
    * `patient-service` (Port 5001)
    * `staff-service` (Port 5002)
    * `appointment-service` (Port 5003)
    * `medical-record-service` (Port 5004)
* **Database:** 4 *database* MySQL logis terpisah (`db_patient`, `db_staff`, `db_appointment`, `db_record`).

### Diagram Alur

```mermaid
graph TD
    A[Frontend (Browser)] --> B(API Gateway :5000);
    
    B --> C[Patient Service :5001];
    B --> D[Staff Service :5002];
    B --> E[Appointment Service :5003];
    B --> F[Medical Record Service :5004];
    
    C --> G[(DB: db_patient)];
    D --> H[(DB: db_staff)];
    E --> I[(DB: db_appointment)];
    F --> J[(DB: db_record)];

    %% Integrasi Backend-to-Backend
    E -.->|Validasi ID| C;
    E -.->|Validasi ID| D;
    F -.->|Validasi ID| C;
