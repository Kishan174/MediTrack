import os
from io import BytesIO

from flask import Blueprint, Response, current_app, flash, redirect, render_template, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename

from forms import MedicalRecordForm
from models import MedicalRecord, Patient, db
from utils import login_required, log_action, roles_required


records_bp = Blueprint("records", __name__, url_prefix="/records")


def fill_choices(form):
    form.patient_id.choices = [(p.id, p.full_name) for p in Patient.query.order_by(Patient.full_name).all()]


@records_bp.route("/")
@login_required
def list_records():
    records = MedicalRecord.query.order_by(MedicalRecord.recorded_at.desc()).all()
    return render_template("records/list.html", records=records)


@records_bp.route("/new", methods=["GET", "POST"])
@roles_required("Admin", "Doctor")
def create_record():
    form = MedicalRecordForm()
    fill_choices(form)
    if form.validate_on_submit():
        record = MedicalRecord(patient_id=form.patient_id.data, title=form.title.data, treatment=form.treatment.data, prescription=form.prescription.data)
        file = form.report_file.data
        if file:
            os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            record.report_file = filename
        db.session.add(record)
        db.session.commit()
        log_action(f"Added medical record for {record.patient.full_name}")
        flash("Medical record saved.", "success")
        return redirect(url_for("records.list_records"))
    return render_template("records/form.html", form=form, title="Add medical record")


@records_bp.route("/<int:record_id>/pdf")
@login_required
def download_pdf(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Meditrack Report {record.id}")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(72, 740, "Meditrack Medical Report")
    pdf.setFont("Helvetica", 11)
    lines = [
        f"Patient: {record.patient.full_name}",
        f"Age/Gender: {record.patient.age} / {record.patient.gender}",
        f"Diagnosis: {record.patient.diagnosis or 'Not recorded'}",
        f"Record: {record.title}",
        f"Date: {record.recorded_at.strftime('%d %b %Y, %I:%M %p')}",
        "",
        "Treatment:",
        record.treatment,
        "",
        "Prescription:",
        record.prescription or "Not recorded",
    ]
    y = 705
    for line in lines:
        pdf.drawString(72, y, line[:95])
        y -= 20
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    log_action(f"Downloaded PDF for record #{record.id}")
    return Response(buffer, mimetype="application/pdf", headers={"Content-Disposition": f"attachment; filename=meditrack_record_{record.id}.pdf"})
