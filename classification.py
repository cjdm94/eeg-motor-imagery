#%%
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import ShuffleSplit, cross_val_score
from mne import Epochs, pick_types, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
from mne.decoding import CSP
%matplotlib qt

# Load the data
subject = 1
runs = [6, 10, 14]
raw_frames = eegbci.load_data(subject, runs)
raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_frames])
#%%

#%%
# Apply default sensor locations (montage) to data
eegbci.standardize(raw)
montage = make_standard_montage('standard_1005')
raw.set_montage(montage) 
#%%

#%%
# Filter the data to include motor-related mu (alpha) and beta rhythms 
raw.filter(7., 30.)
events, _ = events_from_annotations(raw, event_id=dict(T1=0, T2=1))
picks = pick_types(raw.info, meg=False, eeg=True, stim=False,
                  exclude='bads')
#%%

#%%
# Make epochs around left hand and right hand events
tmin, tmax = -1., 4.
epochs = Epochs(raw, events, None, tmin, tmax, proj=True,picks=picks, 
                baseline=None, preload=True)
epochs_train = epochs.copy().crop(tmin=1., tmax=2.)
labels = epochs.events[:, -1]
#%%

#%%
# Make K folds for cross-validation of classifier
scores = []
epochs_data = epochs.get_data()
epochs_data_train = epochs_train.get_data()
cv = ShuffleSplit(10, test_size=0.2, random_state=42)
cv_split = cv.split(epochs_data_train)
#%%

#%%
# Assemble a classifier based on the Common Spatial Patterns for feature extraction
lda = LinearDiscriminantAnalysis()
csp = CSP(n_components=4, reg=None, log=True, norm_trace=False)
#%%

#%%
# Train CSP classifier in order to visualise patterns (inverse of spatial filters)
csp.fit_transform(epochs_data, labels)
csp.plot_patterns(epochs.info, ch_type='eeg', units='Patterns (AU)', size=1.5)
#%%

#%%
# Prepare to classify the data in a sliding window (starting from imagery onset)
sfreq = raw.info['sfreq']
w_length = int(sfreq * 0.5) # running classifier: window length
w_step = int(sfreq * 0.1) # running classifier: window step size
w_start = np.arange(0, epochs_data.shape[2] - w_length, w_step)
scores_windows = []
#%%

#%%
# Do cross-validated classification for each sliding window
for train_idx, test_idx in cv_split:
    y_train, y_test = labels[train_idx], labels[test_idx]
    
    X_train = csp.fit_transform(epochs_data_train[train_idx], y_train)
    X_test = csp.transform(epochs_data_train[test_idx])

    # fit classifier
    lda.fit(X_train, y_train)

    # running classifier: test classifier on sliding window
    score_this_window = []
    for n in w_start:
        X_test = csp.transform(epochs_data[test_idx][:, :, n:(n + w_length)])
        score_this_window.append(lda.score(X_test, y_test))
    scores_windows.append(score_this_window)
#%%

#%%
# Plot scores (classification accuracy) over time
w_times = (w_start + w_length / 2.) / sfreq + epochs.tmin
plt.figure()
plt.plot(w_times, np.mean(scores_windows, 0), label='Score')
plt.axvline(0, linestyle='--', color='k', label='Onset')
plt.axhline(0.5, linestyle='-', color='k', label='Chance')
plt.xlabel('time (s)')
plt.ylabel('classification accuracy')
plt.title('Classification score over time')
plt.legend(loc='lower right')
plt.show()
#%%


