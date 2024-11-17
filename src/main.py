import time
from model import Model
from connect import Connection
from sender import send_email_risk, send_email_seizure

model = Model()
connection = Connection()

while True:
    data = connection.get_data()
    prediction = model.predict(data)

    if prediction == 1:
        send_email_risk()
    elif prediction == 2:
        send_email_seizure()
    
    time.sleep(5)