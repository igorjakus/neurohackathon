import time
from model import Model
from connect import Connect
import numpy as np
from sender import send_email_risk, send_email_seizure
import matplotlib.pyplot as plt
import pandas as pd

def plot_3_channels(data_arr, timestamps):
    timestamps = np.arange(timestamps)
    titles =  ["No seizure detected","Seizure risk","Seizure detected"]
    for j in range(3) :

        # Create a figure with 8 subplots
        _, axes = plt.subplots(3, 1, figsize=(10, 15))

        # Plot each row of the array on a separate subplot
        # axes[0].set_title(titles[j])
        for i in range(3):
            axes[i].plot(timestamps, data_arr[j][i])
            axes[i].set_xlabel("Timestamp")
            axes[i].set_ylabel("Value")
        
        # Adjust layout to prevent overlap
        plt.tight_layout()
        plt.show()


df= pd.read_csv('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/data/dane_0.csv', header=None)
X0 = df.to_numpy()

df= pd.read_csv('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/data/dane_1.csv', header=None)
X1 = df.to_numpy()

df= pd.read_csv('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/data/dane_2.csv', header=None)
X2 = df.to_numpy()

plot_3_channels([X0,X1,X2], 178)

