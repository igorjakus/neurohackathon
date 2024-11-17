import numpy as np
import pandas as pd


df= pd.read_csv('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/data/Epileptic_Seizure_Recognition.csv')

# Extract features (all columns except the last one or the 'y' column)
X = df.iloc[:, 1:-1].to_numpy()

# Extract labels (the 'y' column)
y = df['y'].to_numpy()
arr_0 = []

for i, row in enumerate(X):
    if y[i] == 1:
        arr_0.append(row)


def save_eeg(eeg_data):
    np.savetxt("C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/data/dataset_2.csv", eeg_data, delimiter=',', fmt='%d')

arr_0 = np.array(arr_0)
save_eeg(arr_0)
