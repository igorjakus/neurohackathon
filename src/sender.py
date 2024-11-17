import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


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


def send_email(subject, body_template, attachment_path=None):
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
    attachment_path = "data/eeg_msg.txt"

    # e-mail
    message.attach(MIMEText(body, "plain"))

    # add attachment if provided
    print(attachment_path)
    if attachment_path:
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            # Encode file in ASCII characters for email transport
            encoders.encode_base64(part)

            # Add header for attachment
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}"
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


send_email_risk()
send_email_seizure()