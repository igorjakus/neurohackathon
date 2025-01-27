import pickle

import numpy as np


class Model:
    def __init__(self, path):
        self._load_model(path)
        self._load_scaler(path)


    def _load_model(self, path):
        with open(path + 'trained/svm_model.pkl', 'rb') as file:
            self.svm = pickle.load(file)
    
    def _load_scaler(self, path):
        with open(path + 'trained/scaler.pkl', 'rb') as file:
            self.scaler = pickle.load(file)

    def predict(self, eeg_data: np.array) -> int:
        eeg_data = eeg_data.reshape(1, -1)
        eeg_data = self.scaler.transform(eeg_data)
        return self.svm.predict(eeg_data)
