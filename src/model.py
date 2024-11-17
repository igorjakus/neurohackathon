import numpy as np
import pickle

class Model:
    def __init__(self):
        self._load_model()
        self._load_scaler()


    def _load_model(self):
        with open('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/trained/svm_model.pkl', 'rb') as file:
            self.svm = pickle.load(file)
    
    def _load_scaler(self):
        with open('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/trained/scaler.pkl', 'rb') as file:
            self.scaler = pickle.load(file)

    def predict(self, eeg_data: np.array) -> int:
        eeg_data = eeg_data.reshape(1, -1)
        eeg_data = self.scaler.transform(eeg_data)
        return self.svm.predict(eeg_data)
