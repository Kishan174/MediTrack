from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, DateField, DateTimeLocalField, EmailField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Optional(), Length(min=6)])
    role = SelectField("Role", choices=[("Admin", "Admin"), ("Doctor", "Doctor"), ("Receptionist", "Receptionist")])
    submit = SubmitField("Save user")


class PatientForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(max=140)])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=0, max=130)])
    gender = SelectField("Gender", choices=[("Female", "Female"), ("Male", "Male"), ("Other", "Other")])
    blood_group = SelectField("Blood group", choices=[("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-")])
    contact = StringField("Contact", validators=[DataRequired(), Length(max=80)])
    email = EmailField("Email", validators=[Optional(), Email()])
    address = TextAreaField("Address", validators=[Optional()])
    medical_history = TextAreaField("Medical history", validators=[Optional()])
    prescriptions = TextAreaField("Prescriptions", validators=[Optional()])
    diagnosis = TextAreaField("Diagnosis", validators=[Optional()])
    admission_date = DateField("Admission date", validators=[DataRequired()])
    submit = SubmitField("Save patient")


class DoctorForm(FlaskForm):
    name = StringField("Doctor name", validators=[DataRequired(), Length(max=140)])
    specialization = StringField("Specialization", validators=[DataRequired(), Length(max=120)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=80)])
    email = EmailField("Email", validators=[Optional(), Email()])
    availability = StringField("Availability", validators=[DataRequired(), Length(max=180)])
    room = StringField("Room", validators=[Optional(), Length(max=40)])
    bio = TextAreaField("Profile bio", validators=[Optional()])
    active = BooleanField("Available", default=True)
    submit = SubmitField("Save doctor")


class AppointmentForm(FlaskForm):
    patient_id = SelectField("Patient", coerce=int, validators=[DataRequired()])
    doctor_id = SelectField("Doctor", coerce=int, validators=[DataRequired()])
    scheduled_at = DateTimeLocalField("Date and time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    reason = StringField("Reason", validators=[DataRequired(), Length(max=220)])
    status = SelectField("Status", choices=[("Scheduled", "Scheduled"), ("Checked In", "Checked In"), ("Completed", "Completed"), ("Cancelled", "Cancelled")])
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Save appointment")


class MedicalRecordForm(FlaskForm):
    patient_id = SelectField("Patient", coerce=int, validators=[DataRequired()])
    title = StringField("Record title", validators=[DataRequired(), Length(max=160)])
    treatment = TextAreaField("Treatment", validators=[DataRequired()])
    prescription = TextAreaField("Prescription", validators=[Optional()])
    report_file = FileField("Upload report", validators=[Optional(), FileAllowed(["pdf", "png", "jpg", "jpeg", "doc", "docx"], "Supported files only")])
    submit = SubmitField("Save record")
