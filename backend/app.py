from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Doctor, Patient, Department, Appointment, Treatment, Present
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt

from datetime import timedelta


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secretkeytocreatesecuretokensforitotwork'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

from flask_jwt_extended import JWTManager

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

    if User.query.filter_by(username=data['username']).first():
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
@jwt_required()
def all_doctors():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    doctors = Doctor.query.all()
    result = []
    for doctor in doctors:
        result.append({
            'doctor_id': doctor.doctor_id,
            'name': doctor.name,
            'qualification': doctor.qualification,
            'contact': doctor.contact,
            'experience_years': doctor.experience_years,
            'department': doctor.department.department_name, 
            'username': doctor.user.username,
            'email': doctor.user.email_id,
        })
    return jsonify({'data': result}), 200

@app.route('/api/add_department', methods=['POST'])
@jwt_required()
def add_department():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    data = request.get_json()

    if Department.query.filter_by(department_name=data['department_name']).first():
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
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    departments = Department.query.all()
    result = []
    for department in departments:
        result.append({
            'department_id': department.department_id,
            'department_name': department.department_name,
            'department_description': department.department_desc
        })
    return jsonify({'data': result}), 200


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