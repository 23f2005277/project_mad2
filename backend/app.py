from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Doctor, Patient, Department, Appointment, Treatment, Present
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secretkey'

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

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

    access_token = create_access_token(identity=user.user_id)
    return jsonify({'message': 'successful login', 'data':{'username':user.username, 'role':user.role, 'email': user.email_id, 'access_token': access_token}}), 200

def admin_creation():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password=generate_password_hash('password'), role='Admin', email_id='admin@gmail.com')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin_creation()
    

    app.run(debug=True, port=5001)