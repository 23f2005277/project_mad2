from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Doctor, Patient, Department, Appointment, Treatment, Present
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt
#from flask_cache import Cache
from datetime import timedelta, date, datetime, time


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secretkeytocreatesecuretokensforitotwork'
#app.config['CACHE_TYPE'] = 'redis'
#app.config['CACHE_REDIS_HOST'] = 'redis ://localhost:6379/0'


CORS(app)
db.init_app(app)
jwt = JWTManager(app)
#cache = Cache()

@jwt.invalid_token_loader
def invalid_token_callback(error):
    print("Invalid token error:", error)
    return jsonify({'message': 'Invalid token', 'error': str(error)}), 422

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists. Please login instead or select a different username'}), 400
    
    user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        email_id=data['email_id'],
        role='patient'
    )

    db.session.add(user)
    db.session.commit()

    patient = Patient(
        puser_id=user.user_id,
        name = "",
        age = 0,
        gender = "",
        address = "",
        contact = "",
        medical_history = "",
    )
    
    db.session.add(patient)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=str(user.user_id), additional_claims={'role': user.role})
    return jsonify({'message': 'successful login', 'data':{'username':user.username, 'role':user.role, 'email': user.email_id, 'access_token': access_token}}), 200

@app.route('/api/add_doctor', methods=['POST'])
@jwt_required()
def add_doctor():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()

    if User.query.filter_by(username=data['username'], active=True).first():
        return jsonify({'message': 'Username already exists.'}), 400
    
    user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        email_id=data['email_id'],
        role='doctor')

    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        duser_id=user.user_id,
        name=data['name'],
        qualification=data['qualification'],
        contact=data['contact'],
        experience_years=data['experience_years'],
        ddepartment_id=data['ddepartment_id']
    )

    db.session.add(doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor added successfully'}), 201

@app.route('/api/alldoctors', methods=['GET'])
#@cache.cached(timeout=60)
@jwt_required()
def all_doctors():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    doctors = Doctor.query.join(User).filter(User.active == True).all()
    result = []
    for doctor in doctors:
        result.append({
            'doctor_id': doctor.doctor_id,
            'name': doctor.name,
            'qualification': doctor.qualification,
            'contact': doctor.contact,
            'experience_years': doctor.experience_years,
            'department': doctor.department.department_name, 
            'ddepartment_id': doctor.ddepartment_id,
            'username': doctor.user.username,
            'email': doctor.user.email_id,
        })
    return jsonify({'data': result}), 200

@app.route('/api/update_doctor/<int:doctor_id>', methods=['PUT'])
@jwt_required()
def update_doctor(doctor_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    data = request.get_json()
    user = User.query.filter_by(user_id=doctor.duser_id).first()

    doctor.name = data.get('name', doctor.name)
    doctor.qualification = data.get('qualification', doctor.qualification)
    doctor.contact = data.get('contact', doctor.contact)
    doctor.experience_years = data.get('experience_years', doctor.experience_years)
    doctor.ddepartment_id = data.get('ddepartment_id', doctor.ddepartment_id)

    user.username = data.get('username', user.username)
    user.email_id = data.get('email_id', user.email_id)

    if data.get('password'):
        user.password = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({'message': 'Doctor updated successfully'}), 200

@app.route('/api/delete_doctor/<int:doctor_id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(doctor_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    else:
        current_day = date.today()

        Appointment.query.filter(Appointment.adoctor_id == doctor.doctor_id,
                                  Appointment.appointment_date >= current_day).update({"status" : "Cancelled"})
        Present.query.filter(Present.pdoctor_id == doctor.doctor_id,
                                  Present.available_date >= current_day).delete()
        doctor.user.active = False
    db.session.commit()

    return jsonify({'message': 'Doctor deleted successfully'}), 200

@app.route('/api/add_department', methods=['POST'])
@jwt_required()
def add_department():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    data = request.get_json()

    if Department.query.filter_by(department_name=data['department_name'], active=True).first():
        return jsonify({'message': 'Department already exists.'}), 400

    department = Department(
        department_name=data['department_name'],
        department_desc=data['department_desc']
    )
    db.session.add(department)
    db.session.commit()

    return jsonify({'message': 'Departments added successfully'}), 201

@app.route('/api/alldepartments', methods=['GET'])
@jwt_required()
def all_departments():
    #if get_jwt().get('role') != 'admin':
    #    return jsonify({'message': 'Admin access required'}), 403

    departments = Department.query.filter_by(active=True).all()
    result = []
    for department in departments:
        result.append({
            'department_id': department.department_id,
            'department_name': department.department_name,
            'department_description': department.department_desc
        })
    return jsonify({'data': result}), 200

@app.route('/api/update_department/<int:department_id>', methods=['PUT'])
@jwt_required()
def update_department(department_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    department = Department.query.get(department_id)

    if not department:
        return jsonify({'message': 'Department not found'}), 404

    data = request.get_json()

    department.department_name = data.get('department_name', department.department_name)
    department.department_desc = data.get('department_desc', department.department_desc)

    db.session.commit()
    return jsonify({'message': 'Department updated successfully'}), 200

@app.route('/api/delete_department/<int:department_id>', methods=['DELETE'])
@jwt_required()
def delete_department(department_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    department = Department.query.get(department_id)

    if not department:
        return jsonify({'message': 'Department not found'}), 404
    
    current_day = date.today()
    for doctor in department.doctors:
        Appointment.query.filter(Appointment.adoctor_id == doctor.doctor_id,
                                  Appointment.appointment_date >= current_day).update({"status" : "Cancelled"})
        Present.query.filter(Present.pdoctor_id == doctor.doctor_id,
                                  Present.available_date >= current_day).delete()
        doctor.user.active = False
    
    department.active = False
    db.session.commit()

    return jsonify({'message': 'Department deleted successfully'}), 200

@app.route('/api/department/<int:department_id>', methods=['GET'])
@jwt_required()
def get_department(department_id):
    department = Department.query.filter_by(
        department_id=department_id,
        active=True
    ).first()

    if not department:
        return jsonify({'message': 'Department not found'}), 404

    doctors = Doctor.query.join(User).filter(Doctor.ddepartment_id == department_id,
    User.active == True).all()

    return jsonify({
        'data': {
            'department_id': department.department_id,
            'department_name': department.department_name,
            'department_description': department.department_desc,
            'doctors': [
                {
                    'doctor_id': doctor.doctor_id,
                    'doctor_name': doctor.name,
                    'doctor_qualification': doctor.qualification,
                    'doctor_experience_years': doctor.experience_years,
                }
                for doctor in doctors
            ]
        }
    }), 200

@app.route('/api/patient_details', methods=['GET'])
@jwt_required()
def patient_details():
    if get_jwt().get('role') != 'patient':
        return jsonify({'message': 'Patient access required'}), 403

    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(puser_id=user_id).first()

    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    return jsonify({
        'data': {
            'patient_id': patient.patient_id,
            'username': patient.user.username,
            'email': patient.user.email_id,
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'address': patient.address,
            'contact': patient.contact,
            'medical_history': patient.medical_history,
        }
    }), 200

@app.route('/api/update_patient', methods=['PUT'])
@jwt_required()
def update_patient():
    if get_jwt().get('role') != 'patient':
        return jsonify({'message': 'Patient access required'}), 403
    
    user_id = get_jwt_identity()
    patient = Patient.query.filter_by(puser_id=user_id).first()

    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    data = request.get_json()
    user = User.query.filter_by(user_id=user_id).first()

    patient.name = data.get('name', patient.name)
    patient.age = data.get('age', patient.age)
    patient.gender = data.get('gender', patient.gender)
    patient.address = data.get('address', patient.address)
    patient.contact = data.get('contact', patient.contact)
    patient.medical_history = data.get('medical_history', patient.medical_history)

    user.username = data.get('username', user.username)
    user.email_id = data.get('email_id', user.email_id)

    if data.get('password'):
        user.password = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/api/allpatients', methods=['GET'])
@jwt_required()
def all_patients():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    patients = Patient.query.join(User).filter(User.active == True).all()
    result = []
    for pat in patients:
        result.append({
            'patient_id': pat.patient_id,
            'name': pat.name,
        })

    return jsonify({'data': result}), 200

@app.route('/api/patient_info/<int:patient_id>', methods=['GET'])
@jwt_required()
def patient_info(patient_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    patient = Patient.query.join(User).filter(User.active == True, Patient.patient_id == patient_id).first()
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404

    return jsonify({
        'data': {
            'patient_id': patient.patient_id,
            'username': patient.user.username,
            'email': patient.user.email_id,
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'address': patient.address,
            'contact': patient.contact,
            'medical_history': patient.medical_history,
        }
    }), 200

@app.route('/api/delete_patient/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    patient = Patient.query.join(User).filter(User.active == True, Patient.patient_id == patient_id).first()
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    current_day = date.today()
    Appointment.query.filter(
        Appointment.apatient_id == patient.patient_id,
        Appointment.appointment_date >= current_day
    ).update({"status":"cancelled"})

    patient.user.active = False
    db.session.commit()

    return jsonify({'message': 'Patient deleted successfully'}), 200

slots = [
    (1, time(9, 0),  time(10, 0)),
    (2, time(10, 0), time(11, 0)),
    (3, time(11, 0), time(12, 0)),
    (4, time(14, 0), time(15, 0)),
    (5, time(15, 0), time(16, 0)),
    (6, time(16, 0), time(17, 0)),]

@app.route('/api/doctor/add_slots', methods=['GET'])
@jwt_required()
def add_slots():
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403

    user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(duser_id=user_id).first()
    current_day = datetime.today().date()

    next_7_dates = [(current_day + timedelta(days=i)) for i in range(1, 8)]
    old_slots = Present.query.filter(Present.pdoctor_id == doctor.doctor_id,
                                     Present.available_date <= current_day, Present.booked == False).all()
    
    for slot in old_slots:
        db.session.delete(slot)
    db.session.commit()

    for day in next_7_dates:
        for slot_number, start, end in slots:
            exists = Present.query.filter_by(
                pdoctor_id=doctor.doctor_id,
                available_date=day,
                slot_number=slot_number
            ).first()
            if not exists:
                new_slot = Present(
                    pdoctor_id=doctor.doctor_id,
                    available_date=day,
                    start_time=start,
                    end_time=end,
                    slot_number=slot_number,
                    active=False
                )
                db.session.add(new_slot)
    db.session.commit()
    
    all_slots = Present.query.filter_by(pdoctor_id=doctor.doctor_id).order_by(
        Present.available_date, Present.slot_number).all()
    
    result = {}
    for slot in all_slots:
        date_str = slot.available_date.strftime('%Y-%m-%d')
        if date_str not in result:
            result[date_str] = []
        result[date_str].append({
            'present_id': slot.present_id,
            'slot_number': slot.slot_number,
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M'),
            'active': slot.active,
            'booked': slot.booked
        })
    return jsonify({'data': result}), 200

@app.route('/api/doctor/add_slots/<int:present_id>/toggle', methods=['PUT'])
@jwt_required()
def toggle_slot(present_id):
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403
    
    user_id = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(duser_id=user_id).first()
    
    slot = Present.query.get(present_id)
 
    if not slot:
        return jsonify({'message': 'Slot not found'}), 404

    if slot.pdoctor_id != doctor.doctor_id:
        return jsonify({'message': 'Unauthorized access'}), 403

    slot = Present.query.get(present_id)
    if not slot:
        return jsonify({'message': 'Slot not found'}), 404

    if slot.booked:
        return jsonify({'message': 'Cannot choose a booked slot'}), 400

    slot.active = not slot.active
    db.session.commit()

    return jsonify({'message': 'Slot updated', 'active': slot.active}), 200

@app.route('/api/patient/select_slot/<int:doctor_id>', methods=['GET'])
@jwt_required()
def select_slot(doctor_id):
    if get_jwt().get('role') != 'patient':
        return jsonify({'message': 'Patient access required'}), 403
    
    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(puser_id=user_id).first()
    doctor = Doctor.query.get(doctor_id)
    
    if not patient.name or patient.age == 0:
        return jsonify({'message': 'Please complete your profile before booking an appointment'}), 400
    
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    current_day = datetime.today().date()

    available_slots = Present.query.filter(Present.pdoctor_id == doctor_id, Present.active == True, Present.booked == False, Present.available_date > current_day).order_by(Present.available_date, Present.slot_number).all()

    if not available_slots:
        return jsonify({'message': 'No available slots found'}), 404

    result = {}
    for slot in available_slots:
        date_str = slot.available_date.strftime('%Y-%m-%d')
        if date_str not in result:
            result[date_str] = []
        result[date_str].append({
            'present_id': slot.present_id,
            'slot_number': slot.slot_number,
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M'),
            'active': slot.active,
            'booked': slot.booked
        })
    return jsonify({'data': result}), 200

@app.route('/api/patient/book_slot/<int:present_id>', methods=['PUT'])
@jwt_required()
def book_slot(present_id):
    if get_jwt().get('role') != 'patient':
        return jsonify({'message': 'Patient access required'}), 403

    user_id = int(get_jwt_identity())
    patient = Patient.query.filter_by(puser_id=user_id).first()
    slot = Present.query.get(present_id)

    if not patient or not slot:
        return jsonify({'message': 'Invalid patient or slot'}), 404
    
    if patient.puser_id != user_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    if not patient.name or patient.age == 0:
        return jsonify({'message': 'Please complete your profile before booking an appointment'}), 400

    old_slots = Appointment.query.filter_by(apatient_id=patient.patient_id, appointment_date=slot.available_date,
    appointment_time=slot.start_time, status="Booked").first()

    if old_slots:
        return jsonify({'message': 'Slot already booked'}), 400

    if not slot.active or slot.booked:
        return jsonify({'message': 'Slot is not available'}), 400
    
    slot.booked = True
    add_appointment = Appointment(adoctor_id=slot.pdoctor_id, apatient_id=patient.patient_id, appointment_date=slot.available_date, appointment_time=slot.start_time, status="Booked", mode="Offline")
    
    db.session.add(add_appointment)
    db.session.commit()

    return jsonify({'message': 'Slot booked successfully'}), 200

@app.route('/api/doctor/allappointments', methods=['GET'])
@jwt_required()
def all_appointments():
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403

    current_user = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(duser_id=current_user).first()

    appointments = Appointment.query.filter_by(adoctor_id=doctor.doctor_id).filter(Appointment.status == "Booked").all()

    result = []
    for appt in appointments:
        result.append({
            'appointment_id': appt.appointment_id,
            'doctor_name': appt.doctor.name,
            'patient_name': appt.patient.name,
            'appointment_date': appt.appointment_date.strftime('%Y-%m-%d'),
            'appointment_time': appt.appointment_time.strftime('%H:%M'),
            'status': appt.status,
            'mode': appt.mode,
            'has_treatment': appt.treatment is not None
        })
    return jsonify({'data': result}), 200

@app.route('/api/patient/allappointments', methods=['GET'])
@jwt_required()
def patient_all_appointments():
    if get_jwt().get('role') != 'patient':
        return jsonify({'message': 'Patient access required'}), 403

    current_user = int(get_jwt_identity())
    patient = Patient.query.filter_by(puser_id=current_user).first()

    appointments = Appointment.query.filter_by(apatient_id=patient.patient_id).filter(Appointment.status != "Cancelled").all()

    result = []
    for appt in appointments:
        result.append({
            'appointment_id': appt.appointment_id,
            'doctor_name': appt.doctor.name,
            'appointment_date': appt.appointment_date.strftime('%Y-%m-%d'),
            'appointment_time': appt.appointment_time.strftime('%H:%M'),
            'status': appt.status,
            'mode': appt.mode
        })
    return jsonify({'data': result}), 200

@app.route('/api/doctor/cancel_appointment/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def dcancel_appointment(appointment_id):
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403

    current_user = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(duser_id=current_user).first()

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    if appointment.adoctor_id != doctor.doctor_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    slot = Present.query.filter_by(
    pdoctor_id=doctor.doctor_id,
    available_date=appointment.appointment_date,
    start_time=appointment.appointment_time).first()

    if slot:
        slot.booked = False
        slot.active = True

    appointment.status = "Cancelled"
    db.session.commit()

    return jsonify({'message': 'Appointment cancelled successfully'}), 200

@app.route('/api/patient/cancel_appointment/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def pcancel_appointment(appointment_id):
    if get_jwt().get('role') != 'patient':
        return jsonify({'message': 'Patient access required'}), 403

    current_user = int(get_jwt_identity())
    patient = Patient.query.filter_by(puser_id=current_user).first()

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    if appointment.apatient_id != patient.patient_id:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    slot = Present.query.filter_by(
    pdoctor_id=appointment.adoctor_id,
    available_date=appointment.appointment_date,
    start_time=appointment.appointment_time).first()

    if slot:
        slot.booked = False
        slot.active = True

    appointment.status = "Cancelled"
    db.session.commit()

    return jsonify({'message': 'Appointment cancelled successfully'}), 200

@app.route('/api/doctor/treatment/<int:appointment_id>', methods=['GET'])
@jwt_required()
def doctor_treatment(appointment_id):
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403

    current_user = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(duser_id=current_user).first()

    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404

    appointment = Appointment.query.get(appointment_id)

    if not appointment or appointment.adoctor_id != doctor.doctor_id:
        return jsonify({'message': 'Appointment not found or unauthorized access'}), 404

    treatment = Treatment.query.filter_by(tappointment_id=appointment_id).first()

    if not treatment:
        return jsonify({'data': None}), 200

    return jsonify({'data': {
        'treatment_id': treatment.treatment_id,
        'treatment': treatment.treatment,
        'prescription': treatment.prescription,
        'info': treatment.info,
        'visit_method': treatment.visit_method
    }}), 200

@app.route('/api/doctor/update_treatment/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_treatment(appointment_id):
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403

    current_user = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(duser_id=current_user).first()

    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404

    appointment = Appointment.query.get(appointment_id)

    if not appointment or appointment.adoctor_id != doctor.doctor_id:
        return jsonify({'message': 'Appointment not found or unauthorized access'}), 404

    data = request.get_json()

    treatment = Treatment.query.filter_by(tappointment_id=appointment_id).first()

    if not treatment:
        treatment = Treatment(
        tappointment_id=appointment_id,
        treatment=data.get('treatment', ''),
        prescription=data.get('prescription', ''),
        info=data.get('info', ''),
        visit_method=data.get('visit_method', '')
    )
        db.session.add(treatment)
    else:
        treatment.treatment = data.get('treatment', treatment.treatment)
        treatment.prescription = data.get('prescription', treatment.prescription)
        treatment.info = data.get('info', treatment.info)
        treatment.visit_method = data.get('visit_method', treatment.visit_method)

    db.session.commit()
    return jsonify({'message': 'Treatment updated successfully'}), 200

@app.route('/api/doctor/complete_appointment/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def complete_appointment(appointment_id):
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403

    current_user = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(duser_id=current_user).first()
    appointment = Appointment.query.get(appointment_id)

    if not appointment or appointment.adoctor_id != doctor.doctor_id:
        return jsonify({'message': 'Appointment not found or unauthorized access'}), 404

    treatment = Treatment.query.filter_by(tappointment_id=appointment_id).first()
    if not treatment:
        return jsonify({'message': 'Please add treatment details before completing appointment'}), 400

    appointment.status = 'Completed'
    db.session.commit()
    return jsonify({'message': 'Appointment marked as completed'}), 200

@app.route('/api/doctor/mypatients', methods=['GET'])
@jwt_required()
def doctor_patients():
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403

    current_user = int(get_jwt_identity())
    doctor = Doctor.query.filter_by(duser_id=current_user).first()

    appointments = Appointment.query.filter_by(
        adoctor_id=doctor.doctor_id
    ).filter(Appointment.status != 'Cancelled').all()

    seen = set()
    result = []
    for appt in appointments:
        patient = appt.patient
        if patient.patient_id not in seen:
            seen.add(patient.patient_id)
            result.append({
                'patient_id': patient.patient_id,
                'name': patient.name,
            })

    return jsonify({'data': result}), 200

@app.route('/api/doctor/patient_history/<int:patient_id>', methods=['GET'])
@jwt_required()
def patient_history(patient_id):
    if get_jwt().get('role') != 'doctor':
        return jsonify({'message': 'Doctor access required'}), 403

    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    treatments = (Treatment.query
        .join(Appointment, Treatment.tappointment_id == Appointment.appointment_id)
        .filter(Appointment.apatient_id == patient.patient_id, Appointment.status == "Completed")
        .order_by(Appointment.appointment_date.desc())
        .all())

    result = []
    for treatment in treatments:
        appointment = treatment.appointment
        doctor = appointment.doctor
        result.append({
            'treatment_id': treatment.treatment_id,
            'treatment': treatment.treatment,
            'prescription': treatment.prescription,
            'info': treatment.info,
            'visit_method': treatment.visit_method,
            'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
            'doctor_name': doctor.name,
            'department': doctor.department.department_name
        })
    return jsonify({'patient_name': patient.name, 'medical_history': patient.medical_history, 'age': patient.age, 'data': result}), 200


def admin_creation():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password=generate_password_hash('password'), role='admin', email_id='admin@gmail.com')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin_creation()
    

    app.run(debug=True, port=5001)