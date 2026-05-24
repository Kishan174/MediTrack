from flask import Blueprint, flash, redirect, render_template, request, url_for

from forms import AppointmentForm
from models import Appointment, Doctor, Patient, db
from utils import login_required, log_action, roles_required


appointments_bp = Blueprint("appointments", __name__, url_prefix="/appointments")


def fill_choices(form):
    form.patient_id.choices = [(p.id, p.full_name) for p in Patient.query.order_by(Patient.full_name).all()]
    form.doctor_id.choices = [(d.id, f"{d.name} - {d.specialization}") for d in Doctor.query.filter_by(active=True).order_by(Doctor.name).all()]


@appointments_bp.route("/")
@login_required
def list_appointments():
    status = request.args.get("status", "")
    appointments = Appointment.query
    if status:
        appointments = appointments.filter_by(status=status)
    appointments = appointments.order_by(Appointment.scheduled_at.desc()).all()
    return render_template("appointments/list.html", appointments=appointments, status=status)


@appointments_bp.route("/new", methods=["GET", "POST"])
@roles_required("Admin", "Receptionist")
def create_appointment():
    form = AppointmentForm()
    fill_choices(form)
    if form.validate_on_submit():
        appointment = Appointment()
        form.populate_obj(appointment)
        db.session.add(appointment)
        db.session.commit()
        log_action(f"Booked appointment for {appointment.patient.full_name}")
        flash("Appointment booked.", "success")
        return redirect(url_for("appointments.list_appointments"))
    return render_template("appointments/form.html", form=form, title="Book appointment")


@appointments_bp.route("/<int:appointment_id>/edit", methods=["GET", "POST"])
@roles_required("Admin", "Receptionist", "Doctor")
def edit_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    form = AppointmentForm(obj=appointment)
    fill_choices(form)
    if form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.commit()
        log_action(f"Updated appointment #{appointment.id}")
        flash("Appointment updated.", "success")
        return redirect(url_for("appointments.list_appointments"))
    return render_template("appointments/form.html", form=form, title="Reschedule appointment")


@appointments_bp.route("/<int:appointment_id>/cancel", methods=["POST"])
@roles_required("Admin", "Receptionist")
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = "Cancelled"
    db.session.commit()
    log_action(f"Cancelled appointment #{appointment.id}")
    flash("Appointment cancelled.", "info")
    return redirect(url_for("appointments.list_appointments"))
