import csv
from io import StringIO

from flask import Blueprint, Response, flash, jsonify, redirect, render_template, request, url_for

from forms import PatientForm
from models import Patient, db
from utils import login_required, log_action, roles_required


patients_bp = Blueprint("patients", __name__, url_prefix="/patients")


@patients_bp.route("/")
@login_required
def list_patients():
    query = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    patients = Patient.query
    if query:
        patients = patients.filter(Patient.full_name.ilike(f"%{query}%") | Patient.contact.ilike(f"%{query}%") | Patient.diagnosis.ilike(f"%{query}%"))
    pagination = patients.order_by(Patient.created_at.desc()).paginate(page=page, per_page=8, error_out=False)
    return render_template("patients/list.html", pagination=pagination, query=query)


@patients_bp.route("/new", methods=["GET", "POST"])
@roles_required("Admin", "Receptionist")
def create_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(**{field: getattr(form, field).data for field in ["full_name", "age", "gender", "blood_group", "contact", "email", "address", "medical_history", "prescriptions", "diagnosis", "admission_date"]})
        db.session.add(patient)
        db.session.commit()
        log_action(f"Added patient {patient.full_name}")
        flash("Patient profile created.", "success")
        return redirect(url_for("patients.profile", patient_id=patient.id))
    return render_template("patients/form.html", form=form, title="Add patient")


@patients_bp.route("/<int:patient_id>")
@login_required
def profile(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template("patients/profile.html", patient=patient)


@patients_bp.route("/<int:patient_id>/edit", methods=["GET", "POST"])
@roles_required("Admin", "Receptionist", "Doctor")
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        log_action(f"Updated patient {patient.full_name}")
        flash("Patient profile updated.", "success")
        return redirect(url_for("patients.profile", patient_id=patient.id))
    return render_template("patients/form.html", form=form, title="Edit patient")


@patients_bp.route("/<int:patient_id>/delete", methods=["POST"])
@roles_required("Admin")
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    log_action(f"Deleted patient {patient.full_name}")
    flash("Patient deleted.", "info")
    return redirect(url_for("patients.list_patients"))


@patients_bp.route("/suggest")
@login_required
def suggest():
    q = request.args.get("q", "").strip()
    rows = Patient.query.filter(Patient.full_name.ilike(f"%{q}%")).limit(6).all() if q else []
    return jsonify([{"id": p.id, "name": p.full_name, "contact": p.contact} for p in rows])


@patients_bp.route("/export.csv")
@login_required
def export_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Age", "Gender", "Blood Group", "Contact", "Email", "Diagnosis", "Admission Date"])
    for p in Patient.query.order_by(Patient.full_name).all():
        writer.writerow([p.full_name, p.age, p.gender, p.blood_group, p.contact, p.email, p.diagnosis, p.admission_date])
    log_action("Exported patients CSV")
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=meditrack_patients.csv"})
