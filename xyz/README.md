# Hospital Management System

A full-stack web application for managing hospital operations including patients, doctors, appointments, and treatments.

---

## 🚀 Tech Stack

**Frontend**

* Vue 3
* Vite
* Vue Router
* Axios
* CSS

**Backend**

* Flask
* SQLAlchemy
* SQLite
* JWT Authentication
* Redis (Caching)
* Celery (Background Tasks)

---

## ⚙️ Setup Instructions

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🔄 Background Services

```bash
redis-server
```

```bash
~/go/bin/MailHog
```

```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

```bash
celery -A celery_worker.celery_app beat --loglevel=info
```

---

## 🔑 Features

* JWT-based authentication
* Role-based access (Admin, Doctor, Patient)
* Appointment booking system
* Doctor availability slots
* Treatment management
* Patient history tracking
* API caching using Redis
* Background jobs using Celery

---

## 📌 Notes

* Default admin is created automatically
* SQLite database is used for simplicity
* Ensure Redis and Celery are running for full functionality

---

