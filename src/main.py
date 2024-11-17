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
    #     print("pwaw 0")
    #     # send_email_risk()
    # elif prediction == 2:
    #     print("pwaw very very bad")

        # send_email_seizure()
    
    time.sleep(5)