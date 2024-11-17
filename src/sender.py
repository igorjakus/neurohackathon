import os
import smtplib
import numpy as np
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


EEG_FILE_PATH = "data/last_eeg_read.csv"
LAST_EMAIL_TIME = None
LAST_EMAIL_TYPE = None
EMAIL_COOLDOWN = timedelta(minutes=1)  # Cooldown duration for emails


def send_email_risk(eeg):
    send_email_with_cooldown("risk", "Seizure Risk Alert", eeg)


def send_email_seizure(eeg):
    send_email_with_cooldown("seizure", "Seizure Alert", eeg)


def send_email_with_cooldown(email_type, subject, eeg_data):
    """Checks cooldown and sends email if appropriate."""
    global LAST_EMAIL_TIME, LAST_EMAIL_TYPE

    current_time = datetime.now()

    if (LAST_EMAIL_TIME and 
        current_time - LAST_EMAIL_TIME < EMAIL_COOLDOWN and 
        LAST_EMAIL_TYPE == email_type):
        # Cooldown active, and the same email type was sent
        print(f"Email of type '{email_type}' not sent due to cooldown.")
        return

    # Save email state
    LAST_EMAIL_TIME = current_time
    LAST_EMAIL_TYPE = email_type

    # Determine the email body
    body_template = (
        "Seizure threat detected!\n"
        "Time: {}.\n"
        "Location: {}, {}.\n" if email_type == "risk" else
        "Seizure detected!\n"
        "Time: {}.\n"
        "Location: {}, {}.\n"
    )
    send_email(subject, body_template, eeg_data)



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
    sender_password = "syyp fthw owcl zqjr"
    # sender_password = os.getenv("EMAIL_PASSWORD")

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
