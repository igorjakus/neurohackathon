import time
from model import Model
from connect import Connect
import numpy as np
from sender import send_email_risk, send_email_seizure

model = Model()
connection = Connect()

while True:
    data = connection.get_data()
    prediction_table = []
    for vec in data:
        prediction_table.append(model.predict(vec))
    
    print(data[0], prediction_table[0])

    # if prediction == 1:
    #     print("pwaw 0")
    #     # send_email_risk()
    # elif prediction == 2:
    #     print("pwaw very very bad")

        # send_email_seizure()
    
    time.sleep(5)