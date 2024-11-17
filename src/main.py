import time
from model import Model
from connect import Connection
from sender import send_email_risk, send_email_seizure

model = Model()
connection = Connection()

while True:
    data = connection.get_data()
    prediction_table = []
    for vec in data:
        prediction_table.push(model.predict(vec))
    
    print(prediction_table)

    # if prediction == 1:
    #     send_email_risk(data)
    # elif prediction == 2:
    #     send_email_seizure(data)
    
    time.sleep(5)