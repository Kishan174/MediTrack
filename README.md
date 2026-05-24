Meditrack – Hospital Management System

Meditrack is a full-stack healthcare management web application built using Flask.
It helps hospitals and clinics manage patients, doctors, appointments, medical records, analytics, and reports through a secure role-based system.

The project is designed with a modern UI, authentication system, dashboard analytics, PDF generation, CSV exports, and responsive pages.

🚀 Features

🔐 Authentication & Authorization
Session-based login system
Role-based access:
Admin
Doctor
Receptionist
Secure password handling
Access control for protected routes

👨‍⚕️ Patient Management
Add, edit, delete, and search patients
Patient profile pages
Pagination support
CSV export functionality
Search suggestions/autocomplete

🩺 Doctor Management
Doctor profiles
Specialization management
Availability tracking

📅 Appointment System
Book appointments
Reschedule appointments
Cancel appointments
Appointment status tracking
Calendar-style appointment cards

📁 Medical Records
Upload medical documents
Store patient medical history
Download PDF medical reports

📊 Dashboard & Analytics
Dashboard summary cards
Analytics charts and statistics
Animated counters
Notifications system
Dark/Light mode support
Audit logs

🛠️ Technologies Used
Frontend
HTML5
CSS3
Bootstrap
JavaScript
Jinja2 Templates
Backend
Python
Flask
Flask Blueprints
Flask-WTF
Flask-SQLAlchemy
Database
SQLite
MySQL (Supported via SQLAlchemy)
Other Tools
PDF Report Generation
CSV Export
File Upload System

📂 Project Structure
Meditrack/
│
├── app.py
├── models.py
├── forms.py
├── utils.py
├── schema.sql
├── requirements.txt
├── README.md
│
├── routes/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
👤 Demo Accounts
Role	Email	Password
Admin	admin@meditrack.com	admin123
Doctor	doctor@meditrack.com	doctor123
Receptionist	reception@meditrack.com	reception123

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/meditrack.git
cd meditrack
2️⃣ Create Virtual Environment
Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Linux / Mac
python3 -m venv .venv
source .venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Initialize Database
flask --app app init-db
5️⃣ Run the Application
flask --app app run --debug

Open in browser:

http://127.0.0.1:5000
🗄️ Database Configuration

By default, the application uses SQLite.

Database file:

instance/meditrack.db

To switch to MySQL:

Install PyMySQL
pip install pymysql
Update database URI in app.py
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/meditrack"
📸 Screenshots

Add screenshots here for:

Login Page
Dashboard
Patient Management
Appointment Booking
Analytics Charts

Example:

![Dashboard Screenshot](static/images/dashboard.png)
🔒 Security Notes

For production deployment:

Replace development SECRET_KEY
Use environment variables
Enable HTTPS
Store uploads outside public static folders
Use a production WSGI server like Gunicorn or Waitress

🎯 Future Enhancements
Email notifications
SMS appointment reminders
Video consultation support
REST API integration
AI-based health analytics
Multi-hospital support
