from flask import render_template
from celery_worker import celery_app
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib 
from jinja2 import Environment, FileSystemLoader
from models import db, User, Patient, Doctor, Appointment, Treatment
from datetime import datetime, timedelta

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS='priyanshi.vasudev612@gmail.com'
SENDER_PASSWORD=''

env = Environment(loader=FileSystemLoader('templates'))

def send_email(to_address,subject,message,content="text",attachment=None):
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment,"rb") as a:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment: filename={attachment}")
        msg.attach(part)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
    #s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

@celery_app.task
def send_monthly_report():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "Admin doesn't exist"
    
    completed = 0
    booked = 0
    cancelled = 0
    
    appointments = Appointment.query.all()
    for appt in appointments:
        if appt.status == 'Completed':
            completed += 1
        elif appt.status == 'Booked':
            booked += 1
        elif appt.status == 'Cancelled':
            cancelled += 1
     
    total = len(appointments)

    doctor_data = {}
    for appoint in appointments:
        doc_name = appoint.doctor.name
        if doc_name not in doctor_data:
            doctor_data[doc_name] = {
                'booked' : 0,
                'completed' : 0,
                'cancelled' : 0,
                'department' : appoint.doctor.department.department_name
            }

        if appoint.status == 'Booked':
            doctor_data[doc_name]['booked'] += 1
        elif appoint.status == 'Completed':
            doctor_data[doc_name]['completed'] += 1
        elif appoint.status == 'Cancelled':
            doctor_data[doc_name]['cancelled'] += 1
    
    template = env.get_template('monthly_report.html')
    html = template.render(doctor_data=doctor_data, total=total, completed=completed, booked=booked, cancelled=cancelled )
    send_email(admin.email_id, "Monthly report",html, content='html')

    return "Monthly report sent successfully"

@celery_app.task
def send_daily_reminder():
    current_day = (datetime.now()).date()

    appointments = Appointment.query.filter(
        Appointment.appointment_date == current_day,
        Appointment.status == 'Booked'
    ).all()

    for appoint in appointments:
        patient_email = appoint.patient.user.email_id

        message = f"""Hello {appoint.patient.name},
        Reminder: You have an appointment today.
        Doctor: {appoint.doctor.name}
        Time: {appoint.appointment_time.strftime('%H:%M')}
        Please be on time, and try to reach half an hour early.
        Thank you."""
        
        send_email(patient_email, "Appointment Reminder", message)
    
    return "Reminders sent successfully"


@celery_app.task
def send_doctor_monthly_report():
    doctors = Doctor.query.join(User).filter(User.active == True).all()

    for doc in doctors:
        appointments = Appointment.query.filter(Appointment.adoctor_id == doc.doctor_id,
            Appointment.status == 'Completed').all()

        total = len(appointments)
        total_treatment = 0

        for i in appointments:
            if i.treatment is not None:
                total_treatment += 1

        appointment_data = []
        for appt in appointments:
            treatment = appt.treatment
            appointment_data.append({
                'date': appt.appointment_date.strftime('%d-%m-%Y'),
                'time': appt.appointment_time.strftime('%H:%M'),
                'patient': appt.patient.name,
                'mode': appt.mode,
                'treatment': treatment.treatment if treatment else '-',
                'prescription': treatment.prescription if treatment else '-',
                'info': treatment.info if treatment else '-',
                'visit_method': treatment.visit_method if treatment else '-',
            })
    
        template = env.get_template('send_doctor_monthly_report.html')
        html = template.render(appointment_data=appointment_data, total=total,
                            total_treatment=total_treatment)
        send_email(
            doc.user.email_id,
            subject=f"Monthly Report — {datetime.now().strftime('%B %Y')}",
            message=html,
            content="html")
        
    return 'Doctor monthly report sent successfully'

@celery_app.task
def export_patient_data(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return "Patient not found"

    treatments = (Treatment.query.join(Appointment).filter(Appointment.apatient_id == patient.patient_id, Appointment.status == "Completed")
        .order_by(Appointment.appointment_date.desc()).all())

    appointment_data = []
    for treatment in treatments:
        appointment = treatment.appointment
        doctor = appointment.doctor
        appointment_data.append({
            'date': appointment.appointment_date.strftime('%d-%m-%Y'),
            'doctor_name': doctor.name,
            'department': doctor.department.department_name,
            'treatment': treatment.treatment,
            'prescription': treatment.prescription,
            'info': treatment.info or '-',
            'visit_method': treatment.visit_method or '-',
        })

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('patient_history_report.html')
    html = template.render(
        patient_name=patient.name,
        month=datetime.now().strftime('%B %Y'),
        appointments=appointment_data
    )

    send_email(
        to_address=patient.user.email_id,
        subject="Your Treatment History Report",
        message=html,
        content="html"
    )

    return "Patient history report sent"
