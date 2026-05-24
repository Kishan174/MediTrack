from datetime import date, datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="Receptionist")
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(140), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    blood_group = db.Column(db.String(8))
    contact = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(160))
    address = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    prescriptions = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    admission_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointments = db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    records = db.relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan")


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    specialization = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(160))
    availability = db.Column(db.String(180), nullable=False)
    room = db.Column(db.String(40))
    bio = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    appointments = db.relationship("Appointment", back_populates="doctor")


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(220), nullable=False)
    status = db.Column(db.String(30), default="Scheduled")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")


class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text)
    report_file = db.Column(db.String(220))
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship("Patient", back_populates="records")


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    action = db.Column(db.String(220), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def seed_data():
    if User.query.first():
        return

    users = [
        User(name="Aarav Admin", email="admin@meditrack.com", password_hash=generate_password_hash("admin123"), role="Admin"),
        User(name="Dr. Meera Shah", email="doctor@meditrack.com", password_hash=generate_password_hash("doctor123"), role="Doctor"),
        User(name="Riya Frontdesk", email="reception@meditrack.com", password_hash=generate_password_hash("reception123"), role="Receptionist"),
    ]
    doctors = [
        Doctor(name="Dr. Meera Shah", specialization="Cardiology", phone="+91 90000 10001", email="meera@meditrack.com", availability="Mon-Fri, 09:00-15:00", room="C-204", bio="Interventional cardiologist focused on preventive cardiac care."),
        Doctor(name="Dr. Kabir Rao", specialization="Neurology", phone="+91 90000 10002", email="kabir@meditrack.com", availability="Tue-Sat, 10:00-16:00", room="N-118", bio="Neurology consultant with expertise in migraine and stroke care."),
        Doctor(name="Dr. Anika Menon", specialization="Pediatrics", phone="+91 90000 10003", email="anika@meditrack.com", availability="Mon-Sat, 08:30-14:30", room="P-022", bio="Pediatrician with a family-centered care approach."),
    ]
    patients = [
        Patient(full_name="Nisha Patel", age=34, gender="Female", blood_group="B+", contact="+91 98888 11111", email="nisha@example.com", address="42 Lake View Road, Pune", medical_history="Mild asthma", prescriptions="Salbutamol as needed", diagnosis="Seasonal bronchitis", admission_date=date.today() - timedelta(days=4)),
        Patient(full_name="Rahul Verma", age=47, gender="Male", blood_group="O+", contact="+91 98888 22222", email="rahul@example.com", address="18 MG Road, Bengaluru", medical_history="Hypertension", prescriptions="Amlodipine 5mg", diagnosis="Elevated blood pressure", admission_date=date.today() - timedelta(days=2)),
        Patient(full_name="Sara Khan", age=9, gender="Female", blood_group="A-", contact="+91 98888 33333", email="sara.guardian@example.com", address="77 Palm Street, Mumbai", medical_history="No known allergies", prescriptions="Vitamin D supplement", diagnosis="Routine pediatric check", admission_date=date.today()),
    ]
    db.session.add_all(users + doctors + patients)
    db.session.flush()
    appointments = [
        Appointment(patient_id=patients[0].id, doctor_id=doctors[0].id, scheduled_at=datetime.now().replace(hour=10, minute=30, second=0, microsecond=0), reason="Follow-up consultation", status="Scheduled"),
        Appointment(patient_id=patients[1].id, doctor_id=doctors[0].id, scheduled_at=datetime.now().replace(hour=13, minute=0, second=0, microsecond=0), reason="Blood pressure review", status="Checked In"),
        Appointment(patient_id=patients[2].id, doctor_id=doctors[2].id, scheduled_at=datetime.now() + timedelta(days=1), reason="Vaccination", status="Scheduled"),
    ]
    records = [
        MedicalRecord(patient_id=patients[0].id, title="Respiratory Review", treatment="Nebulization and rest advised.", prescription="Salbutamol inhaler, steam inhalation"),
        MedicalRecord(patient_id=patients[1].id, title="Cardiac Risk Assessment", treatment="ECG normal. Lifestyle changes advised.", prescription="Continue Amlodipine 5mg daily"),
    ]
    logs = [AuditLog(user_name="System", action="Seeded Meditrack demo data")]
    db.session.add_all(appointments + records + logs)
    db.session.commit()
