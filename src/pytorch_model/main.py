import numpy as np
import pandas as pd
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import Dataset, DataLoader

import csv



df= pd.read_csv('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/data/Epileptic_Seizure_Recognition.csv')

print(df.head())
label = df.loc[0, 'y']
vector = df.iloc[0, 1:-1].to_numpy()

print(vector, label)