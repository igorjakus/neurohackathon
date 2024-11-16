import time
import matplotlib.pyplot as plt
from brainaccess.core.eeg_manager import EEGManager
from brainaccess.utils import acquisition
# dictionary with electrode names
HALO = {
    0: "Fp1",
    1: "Fp2",
    2: 'O1',
    3: 'O2'
}
CAP = {
    0: "F3",
    1: "F4",
    2: "C3",
    3: "C4",
    4: "P3",
    5: "P4",
    6: "O1",
    7: "O2",
}
# device port (can be checked in BrainAccess Board)
DEVICE_PORT = "COM4"
eeg = acquisition.EEG()
eeg_recordings = []
with EEGManager() as manager:
    eeg.setup(manager, CAP, port=DEVICE_PORT)
    for _ in range(10):
        eeg.start_acquisition()
        time.sleep(1)
        # add annotation to EEG recording
        eeg.annotate("HERE")
        time.sleep(1)
        eeg.get_mne()
        eeg_data = eeg.data.mne_raw # EEG data as MNE object
        eeg_recordings.append(eeg_data)
        # process EEG data...
        eeg.stop_acquisition()
        manager.clear_annotations()
    manager.disconnect()
eeg.close()
# plot some of the acquired data
eeg_recordings[0].pick_types(
    eeg=True, stim=False, eog=False, exclude="bads"
).apply_function(lambda x: x * 10**-6).filter(l_freq=1, h_freq=50).notch_filter(
    [50, 100]
).plot()

plt.show()