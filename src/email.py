import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

def send_email_alert(to_email, subject, body):
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
            print("E-mail wysłany!")
    except Exception as e:
        print(f"Błąd podczas wysyłania: {e}")


if __name__ == "__main__":
    # data of the receiver and message text
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    to_email = "lidiapodoluk@gmail.com"  # for example parent's e-mail address
    subject = "Seizure Alert"
    body = (
        "Zagrożenie padaczkowe wykryte u dziecka! \n"
        f"Time: {formatted_time}\n"
        "Location: 69.888888, 42.000000.\n"
    )

    print(body)
    send_email_alert(to_email, subject, body)
