# Meditrack

Meditrack is a full-stack Flask hospital management web application for patient records, doctors, appointments, medical records, audit logs, dashboards, CSV exports, and PDF reports.

## Features

- Flask app with blueprints, Jinja2 templates, Flask-SQLAlchemy models, and Flask-WTF forms
- Session-based authentication with Admin, Doctor, and Receptionist roles
- Patient CRUD, profiles, search, suggestions, pagination, and CSV export
- Doctor profiles with specialization and availability
- Appointment booking, rescheduling, cancellation, status tracking, and calendar-style cards
- Medical records with uploads and downloadable PDF reports
- Dashboard cards, analytics charts, audit logs, notifications, animated counters, dark/light mode
- SQLite by default, with SQLAlchemy support for MySQL by changing the database URI

## Demo Accounts

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@meditrack.com` | `admin123` |
| Doctor | `doctor@meditrack.com` | `doctor123` |
| Receptionist | `reception@meditrack.com` | `reception123` |

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Initialize the database with sample data:

```powershell
flask --app app init-db
```

Run the Flask server:

```powershell
flask --app app run --debug
```

Open `http://127.0.0.1:5000`.

## Database

The app uses SQLite by default and creates `instance/meditrack.db`. The schema is documented in `schema.sql`. To use MySQL, install a compatible driver such as `pymysql` and update `SQLALCHEMY_DATABASE_URI` in `app.py`, for example:

```python
mysql+pymysql://user:password@localhost/meditrack
```

## Project Structure

```text
app.py
models.py
forms.py
utils.py
routes/
templates/
static/
  css/
  js/
  images/
  uploads/
requirements.txt
schema.sql
README.md
```

## Notes

For production, replace the development `SECRET_KEY`, use environment variables, enable HTTPS, place uploads outside the public static tree, and configure a production WSGI server.
