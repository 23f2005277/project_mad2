from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email_id = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)

    doctor = db.relationship('Doctor', back_populates='user', uselist=False, cascade="all, delete-orphan")
    patient = db.relationship('Patient', back_populates='user', uselist=False, cascade="all, delete-orphan")


class Doctor(db.Model):
    __tablename__ = 'doctor'
    doctor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    duser_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    qualification = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    ddepartment_id = db.Column(db.Integer, db.ForeignKey("department.department_id"), nullable=False)

    user = db.relationship('User', back_populates='doctor')
    department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade="all, delete-orphan")
    presents = db.relationship('Present', back_populates='doctor', cascade="all, delete-orphan")

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    puser_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    address = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String, nullable=False)
    medical_history = db.Column(db.Text, nullable=True)

    user = db.relationship('User', back_populates='patient')
    appointments = db.relationship('Appointment', back_populates='patient', cascade="all, delete-orphan")

class Department(db.Model):
    __tablename__ = "department"
    department_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    department_name = db.Column(db.String, nullable=False, unique=True)
    department_desc = db.Column(db.Text)

    doctors = db.relationship('Doctor', back_populates='department', cascade="all, delete-orphan")

class Appointment(db.Model):
    __tablename__ = "appointment"
    appointment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    adoctor_id = db.Column(db.Integer, db.ForeignKey("doctor.doctor_id"), nullable=False)
    apatient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    status = db.Column(db.String)
    mode = db.Column(db.String)
     
    doctor = db.relationship('Doctor', back_populates='appointments')
    patient = db.relationship('Patient', back_populates='appointments')
    treatment = db.relationship('Treatment', back_populates='appointment', uselist=False, cascade="all, delete-orphan")

class Treatment(db.Model):
    __tablename__ = "treatment"
    treatment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tappointment_id = db.Column(db.Integer, db.ForeignKey("appointment.appointment_id"), nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    info = db.Column(db.Text)
    visit_method = db.Column(db.String)

    appointment = db.relationship('Appointment', back_populates='treatment')

class Present(db.Model):
    __tablename__ = "present"
    present_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pdoctor_id = db.Column(db.Integer, db.ForeignKey("doctor.doctor_id"), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    booked = db.Column(db.Boolean, default=False)
    slot_number = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=False)

    doctor = db.relationship('Doctor', back_populates='presents')