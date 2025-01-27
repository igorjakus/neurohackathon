import time

from eeg.model import Model
from src.eeg.connect import Connect

# from sender import send_email_risk, send_email_seizure

model = Model()
connection = Connect()

while True:
    data = connection.get_data()
    prediction_table = []
    for vec in data:
        prediction_table.append(model.predict(vec))
    
    print(data[0], prediction_table[0])

    # if prediction == 1:
    #     send_email_risk(data)
    # elif prediction == 2:
    #     send_email_seizure(data)
    
    time.sleep(5)