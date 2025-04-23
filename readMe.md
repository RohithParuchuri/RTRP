pip install --upgrade pip
pip install virtualenv .
python -m virtualenv .
.\scripts\activate



CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
, is_doctor INTEGER NOT NULL DEFAULT 0);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE user_profile (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    age INTEGER,
    sex TEXT,
    addres TEXT,
    phone TEXT,
    email TEXT,
    emergency_contact TEXT,
    blood_type TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);
CREATE TABLE medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patientUsername TEXT NOT NULL,
    medicineName TEXT NOT NULL,
    dosage TEXT NOT NULL,
    frequency TEXT NOT NULL,
    instructions TEXT
);