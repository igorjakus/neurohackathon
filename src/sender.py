import os
import smtplib
import numpy as np
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


EEG_FILE_PATH = "data/last_eeg_read.csv"


def send_email_risk(eeg):
    subject = "Seizure Risk Alert"

    body_template = (
        "Seizure threat detected!\n"
        "Time: {}.\n"
        "Location: {}, {}.\n"
    )

    send_email(subject, body_template, eeg)


def send_email_seizure(eeg):
    subject = "Seizure Alert"
    
    body_template = (
        "Seizure detected!\n"
        "Time: {}.\n"
        "Location: {}, {}.\n"
    )

    send_email(subject, body_template, eeg)


def save_eeg(eeg_data):
    np.savetxt(EEG_FILE_PATH, eeg_data, delimiter=',', fmt='%d')


def send_email(subject, body_template, eeg_data):
    save_eeg(eeg_data)

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

    try:
        with open(EEG_FILE_PATH, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        # Encode file in ASCII characters for email transport
        encoders.encode_base64(part)

        # Add header for attachment
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(EEG_FILE_PATH)}"
        )

        # Attach the file to the email
        message.attach(part)
    except Exception as e:
        print(f"Błąd podczas dodawania załącznika: {e}")
        return

    # send e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
    except Exception as e:
        print(f"Error during sending: {e}")

if __name__ == "__main__":
    send_email_risk()
    send_email_seizure()