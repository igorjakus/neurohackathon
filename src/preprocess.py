import numpy as np
import pandas as pd

def preprocess_data(dataset: pd.DataFrame) -> np.array:
    def split_id(id) -> tuple:
        try:
            time_stamp, idk, person = id.split(".")
        except Exception:
            time_stamp, idk = id.split(".")
            person = 999
        
        time_stamp = int(time_stamp[1:])
        person = int(person)
        return person, time_stamp, idk

    # Extract columns
    ids = dataset["Unnamed"]
    values = dataset.iloc[:, 1:179].to_numpy()  # Assuming values are numeric
    labels = dataset["y"]

    # Extract person and time_stamp from ids
    people, time_stamps = zip(*[split_id(id)[:2] for id in ids])

    # Create a structured numpy array
    dtype = [('person', 'i4'), ('time_stamp', 'i4'), ('values', 'f4', (178,)), ('labels', 'i4')]  # Assuming 178 values
    preprocessed = np.array(list(zip(people, time_stamps, values, labels)), dtype=dtype)

    # Filter out invalid entries (person == 999)
    preprocessed = preprocessed[preprocessed['person'] != 999]

    # Sort by person and time_stamp
    return np.sort(preprocessed, order=['person', 'time_stamp'])

def get_data() -> np.array:
    """
    5 - eyes open, means when they were recording the EEG signal of the brain the patient had their eyes open
    4 - eyes closed, means when they were recording the EEG signal the patient had their eyes closed
    3 - Yes they identify where the region of the tumor was in the brain and recording the EEG activity from the healthy brain area
    2 - They recorder the EEG from the area where the tumor was located
    1 - Recording of seizure activity
    """
    return preprocess_data(pd.read_csv("../data/Epileptic_Seizure_Recognition.csv"))
