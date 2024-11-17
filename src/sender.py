import os
import smtplib
import numpy as np
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


EEG_FILE_PATH = "/home/lidia/neurohackathon/data/last_eeg_read.csv"
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
    eeg_data_example1 = [142.0, 262.0, 382.0, 451.0, 452.0, 435.0, 544.0, 562.0, 462.0, 182.0, -132.0, -290.0, -329.0, -290.0, -246.0, -226.0, -220.0, -229.0, -243.0, -274.0, -307.0, -336.0, -346.0, -329.0, -278.0, -209.0, -148.0, -95.0, -58.0, -18.0, 11.0, 15.0, 14.0, -11.0, -44.0, -72.0, -77.0, -18.0, 177.0, 517.0, 843.0, 961.0, 874.0, 713.0, 537.0, 376.0, 140.0, -64.0, -199.0, -259.0, -282.0, -304.0, -334.0, -342.0, -341.0, -311.0, -257.0, -220.0, -168.0, -119.0, -73.0, -31.0, 21.0, 60.0, 124.0, 287.0, 789.0, 1168.0, 1325.0, 909.0, 203.0, -314.0, -577.0, -624.0, -597.0, -586.0, -552.0, -479.0, -402.0, -333.0, -333.0, -323.0, -326.0, -314.0, -288.0, -233.0, -159.0, -82.0, 11.0, 117.0, 338.0, 732.0, 1004.0, 1051.0, 709.0, 195.0, -223.0, -477.0, -566.0, -483.0, -364.0, -230.0, -189.0, -237.0, -310.0, -378.0, -398.0, -376.0, -329.0, -218.0, -116.0, -34.0, -23.0, -68.0, -112.0, -114.0, -99.0, -78.0, -59.0, -19.0, 41.0, 105.0, 132.0, 130.0, 110.0, 86.0, 83.0, 109.0, 156.0, 199.0, 287.0, 531.0, 1036.0, 1328.0, 1375.0, 955.0, 464.0, 128.0, -45.0, -108.0, -150.0, -175.0, -180.0, -149.0, -132.0, -133.0, -182.0, -235.0, -264.0, -256.0, -225.0, -178.0, -132.0, -58.0, 13.0, 73.0, 237.0, 437.0, 616.0, 582.0, 396.0, 105.0, -107.0, -213.0, -133.0, 31.0, 105.0, 20.0, -208.0, -394.0, -486.0, -512.0, -495.0, -458.0, -406.0, -340.0, -241.0, -145.0]
    eeg_data_example2 = eeg_data_example1
    send_email_risk(eeg_data_example1)
    send_email_seizure(eeg_data_example2)
    send_email_risk(eeg_data_example1)
    send_email_seizure(eeg_data_example2)
