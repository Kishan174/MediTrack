from datetime import date, timedelta

from flask import Blueprint, jsonify, render_template
from sqlalchemy import func

from models import Appointment, AuditLog, Doctor, Patient
from utils import login_required


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    today_start = date.today()
    today_end = today_start + timedelta(days=1)
    stats = {
        "patients": Patient.query.count(),
        "appointments_today": Appointment.query.filter(Appointment.scheduled_at >= today_start, Appointment.scheduled_at < today_end).count(),
        "doctors_available": Doctor.query.filter_by(active=True).count(),
        "records": sum(len(patient.records) for patient in Patient.query.all()),
    }
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(6).all()
    todays_appointments = Appointment.query.filter(Appointment.scheduled_at >= today_start, Appointment.scheduled_at < today_end).order_by(Appointment.scheduled_at).all()
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(7).all()
    return render_template("dashboard.html", stats=stats, recent_patients=recent_patients, todays_appointments=todays_appointments, logs=logs)


@dashboard_bp.route("/api/dashboard/analytics")
@login_required
def analytics():
    status_rows = Appointment.query.with_entities(Appointment.status, func.count(Appointment.id)).group_by(Appointment.status).all()
    gender_rows = Patient.query.with_entities(Patient.gender, func.count(Patient.id)).group_by(Patient.gender).all()
    return jsonify({
        "appointments": {"labels": [r[0] for r in status_rows], "data": [r[1] for r in status_rows]},
        "patients": {"labels": [r[0] for r in gender_rows], "data": [r[1] for r in gender_rows]},
    })
