import numpy as np
import brainaccess_board as bb
from time import sleep
from model import Model

def send_email():
    pass

def downsample(data_channel):
    # Downsample from 250 Hz to 178 Hz by averaging over appropriate windows
    data_new = np.zeros(178)
    for i in range(178):
        start_index = int(np.floor(i * 250 / 178))
        end_index = int(np.floor((i + 1) * 250 / 178))
        if end_index == start_index:
            end_index = start_index + 1
        if end_index > 250:
            end_index = 250
        data_window = data_channel[start_index:end_index]
        data_new[i] = np.mean(data_window)
    return data_new


if __name__ == "__main__":
    model = Model()

    while True:
        db, status = bb.db_connect()
        if status:
            data = db.get_mne()
            mne_data = data[next(iter(data))] 

            # Select electrode channels
            channels_of_electrodes = ['F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2']
            mne_data.pick(channels_of_electrodes).filter(1, 40)

            # Get data
            data = mne_data.get_data()
            np_data = np.array(data)
            data_last_1s = np_data[:, -250:]  # Last second of data at 250 Hz

            # Select the 'C3' channel
            channel_index = channels_of_electrodes.index('C3')
            data_channel = data_last_1s[channel_index, :]  # Data from 'C3'

            data_new = downsample(data_channel)
            
            # Make prediction
            prediction = model.predict(data_new)
            print(f'Prediction: {prediction}')

            # Check prediction and send email if needed
            if prediction == 1:
                send_email()

        sleep(5)