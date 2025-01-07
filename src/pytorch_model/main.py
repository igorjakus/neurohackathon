import pandas as pd

df= pd.read_csv('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/data/Epileptic_Seizure_Recognition.csv')

print(df.head())
label = df.loc[0, 'y']
vector = df.iloc[0, 1:-1].to_numpy()

print(vector, label)