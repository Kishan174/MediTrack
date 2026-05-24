CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL,
    active BOOLEAN,
    created_at DATETIME
);

CREATE TABLE patient (
    id INTEGER NOT NULL PRIMARY KEY,
    full_name VARCHAR(140) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(30) NOT NULL,
    blood_group VARCHAR(8),
    contact VARCHAR(80) NOT NULL,
    email VARCHAR(160),
    address TEXT,
    medical_history TEXT,
    prescriptions TEXT,
    diagnosis TEXT,
    admission_date DATE,
    created_at DATETIME
);

CREATE TABLE doctor (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(140) NOT NULL,
    specialization VARCHAR(120) NOT NULL,
    phone VARCHAR(80) NOT NULL,
    email VARCHAR(160),
    availability VARCHAR(180) NOT NULL,
    room VARCHAR(40),
    bio TEXT,
    active BOOLEAN
);

CREATE TABLE appointment (
    id INTEGER NOT NULL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    scheduled_at DATETIME NOT NULL,
    reason VARCHAR(220) NOT NULL,
    status VARCHAR(30),
    notes TEXT,
    created_at DATETIME,
    FOREIGN KEY(patient_id) REFERENCES patient (id),
    FOREIGN KEY(doctor_id) REFERENCES doctor (id)
);

CREATE TABLE medical_record (
    id INTEGER NOT NULL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    title VARCHAR(160) NOT NULL,
    treatment TEXT NOT NULL,
    prescription TEXT,
    report_file VARCHAR(220),
    recorded_at DATETIME,
    FOREIGN KEY(patient_id) REFERENCES patient (id)
);

CREATE TABLE audit_log (
    id INTEGER NOT NULL PRIMARY KEY,
    user_name VARCHAR(120) NOT NULL,
    action VARCHAR(220) NOT NULL,
    created_at DATETIME
);
