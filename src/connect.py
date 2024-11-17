import numpy as np
import brainaccess_board as bb
from time import sleep
import mne
import matplotlib.pyplot as plt
from scipy.signal import resample


def plot_8_channels(data, timestamps):
    timestamps = np.arange(timestamps)

    # Create a figure with 8 subplots
    _, axes = plt.subplots(8, 1, figsize=(10, 15))

    # Plot each row of the array on a separate subplot
    for i in range(8):
        axes[i].plot(timestamps, data[i])
        axes[i].set_title(f"Graph {i+1}")
        axes[i].set_xlabel("Timestamp")
        axes[i].set_ylabel("Value")

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()



class Connect():
    def __init__(self):
        pass

    def get_data(self):
        db, status = bb.db_connect()
        if status:
            data = db.get_mne()
            mne_data = data[next(iter(data))] 

        channels_of_electrodes = ['F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2']
        mne_data.pick(channels_of_electrodes).filter(1, 40)
        #mne_data.pick(channels_of_electrodes)
        data = mne_data.get_data()
        np_data = np.array(data)
        data_last_1s = np_data[:, -250:] * 1000000 # 250 is a sfreq
        data_last_1s = data_last_1s - np.mean(data_last_1s, axis = 1, keepdims=True)
        #print(data_last_1s.shape) -> (8 ,250)

        #TO DO - downsampling z 250hz do 178hz

        return data_last_1s
    
    def downsample(data):
        # Downsample from 250 Hz to 178 Hz by averaging over appropriate windows
        target_samples = 178
        resampled_data = np.zeros((8, target_samples))
        for i in range(data.shape[0]):
            resampled_data[i] = resample(data[i], target_samples)

connection = Connect()
test = np.random(8,250)



# data = connection.get_data()
# plot_8_channels(data, 1000)
