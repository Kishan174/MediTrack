from flask import Blueprint, flash, redirect, render_template, url_for

from forms import DoctorForm
from models import Doctor, db
from utils import login_required, log_action, roles_required


doctors_bp = Blueprint("doctors", __name__, url_prefix="/doctors")


@doctors_bp.route("/")
@login_required
def list_doctors():
    doctors = Doctor.query.order_by(Doctor.specialization, Doctor.name).all()
    return render_template("doctors/list.html", doctors=doctors)


@doctors_bp.route("/new", methods=["GET", "POST"])
@roles_required("Admin")
def create_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor()
        form.populate_obj(doctor)
        db.session.add(doctor)
        db.session.commit()
        log_action(f"Added doctor {doctor.name}")
        flash("Doctor profile created.", "success")
        return redirect(url_for("doctors.list_doctors"))
    return render_template("doctors/form.html", form=form, title="Add doctor")


@doctors_bp.route("/<int:doctor_id>/edit", methods=["GET", "POST"])
@roles_required("Admin")
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm(obj=doctor)
    if form.validate_on_submit():
        form.populate_obj(doctor)
        db.session.commit()
        log_action(f"Updated doctor {doctor.name}")
        flash("Doctor profile updated.", "success")
        return redirect(url_for("doctors.list_doctors"))
    return render_template("doctors/form.html", form=form, title="Edit doctor")


@doctors_bp.route("/<int:doctor_id>/delete", methods=["POST"])
@roles_required("Admin")
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.active = False
    db.session.commit()
    log_action(f"Deactivated doctor {doctor.name}")
    flash("Doctor marked unavailable.", "info")
    return redirect(url_for("doctors.list_doctors"))
