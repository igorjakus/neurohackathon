import numpy as np
import brainaccess_board as bb
from time import sleep
import mne
import matplotlib.pyplot as plt


def plot_1s(data_1s, timestamps):
    timestamps = np.arange(timestamps)

    # Create a figure with 8 subplots
    _, axes = plt.subplots(8, 1, figsize=(10, 15))

    # Plot each row of the array on a separate subplot
    for i in range(8):
        axes[i].plot(timestamps, data_1s[i])
        axes[i].set_title(f"Graph {i+1}")
        axes[i].set_xlabel("Timestamp")
        axes[i].set_ylabel("Value")

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()


while True:
    db, status = bb.db_connect()
    if status:
        data = db.get_mne()
        mne_data = data[next(iter(data))] 


    channels_of_electrodes = ['F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2']
    mne_data.pick(channels_of_electrodes).filter(1, 40)
    
    # mne_data.pick(channels_of_electrodes)
    
    data = mne_data.get_data()
    np_data = np.array(data)
    data_last_1s = np_data[:, -1000:] # 250 is a sfreq
    
    print(np_data.shape)
    print(data_last_1s.shape)
    print(data_last_1s)
    plot_1s(data_last_1s, 1000)
    print()

    sleep(5)
    