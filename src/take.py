import numpy as np
import pandas as pd


def takedata(path):
    zeros = pd.read_csv(path + 'dataset_0.csv')
    ones =  pd.read_csv(path + 'dataset_1.csv')
    twos = pd.read_csv(path + 'dataset_2.csv')
    zeros_np = zeros.sample(10).to_numpy()
    ones_np = ones.sample(2).to_numpy()
    twos_np = twos.sample(1).to_numpy()
    stream =  np.concatenate((zeros_np,ones_np,twos_np))
    np.random.shuffle(stream)
    return stream
    