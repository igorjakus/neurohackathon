import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_risk():
    subject = "Seizure Risk Alert"

    body_template = (
        "Seizure threat detected!\n"
        "Time: {}.\n"
        "Location: {}, {}.\n"
    )

    send_email(subject, body_template)


def send_email_seizure():
    subject = "Seizure Alert"
    
    body_template = (
        "Seizure detected!\n"
        "Time: {}.\n"
        "Location: {}, {}.\n"
    )

    send_email(subject, body_template)


def send_email(subject, body_template):
    current_time = datetime.now()
    time_stamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    body = body_template.format(time_stamp, 51.107885, 17.038538)


    to_email = "lidiapodoluk@gmail.com"

    # server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "neurohackathon24@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")

    # create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # e-mail
    message.attach(MIMEText(body, "plain"))

    # send e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
    except Exception as e:
        print(f"Error during sending: {e}")
