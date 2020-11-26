# Documentation

## analysis.py

## Choosing the channels

We keep the TRIM channels, since this is where our event markers are saved. We keep the EOG so we can automatically reject eye movement artefacts.

## Plotting the power spectrum

We compute the average power of a signal in a specific frequency range. This implies the decomposition of the EEG signal into frequency components, which is commonly achieved through Fourier transforms.

Raw EEG has 5 main bandwidths:

Gamma, 30-80Hz (sensory perception - conscious processing)
Beta, 13-30Hz (awake, alert, some mental effort)
Alpha, 8-12Hz (awake, eyes closed and resting)
Theta, 6-8Hz (early light sleep)
Delta, 0.5-4Hz (deep sleep)

Plotting the power spectrum allows us to verify that the EEG shows the expected brain activity in the different frequency bands, e.g. we see a large peak in the theta frequency, and another peak in the alpha frequency, which appear strongly in the parieto-occipital areas.

<img src=./img/power-spectrum.png height="200px">

#### A note on Fourier transforms

## Plotting the time series

We can get a feeling for the cleanliness of the data by plotting the raw time-series for each sensor. This can be an opportunity to remove any erroneous channels from the data - if, for example, there was some unintended movement of a particular sensor during the recording.

It can also visualise artefacts, like eye movements. These can be marked manually and filtered out. They can also be removed automatically by ICA.

## Independent component analysis

Independent Component Analysis is used to remove artefacts from EEG. It is more generally a signal processing method to separate independent sources linearly mixed in several sensors. For instance, when recording EEG on the scalp, ICA can separate out artifacts embedded in the data (since they are usually independent of each other).

For EEG applications, you can show the time-series, power spectrum and/or topography of each component in order to judge which components represent artefacts. For example, a topographical component with a bi-lateral character is classically an indication of eye movement artefacts. This artefact (electrical activity) will most likely be picked up by multiple electrodes, so it is helpful to remove this "component" from the data.

If you use EOG channels, you can use them to automatically reject any components that correspond the eye artefacts. You would run an ICA decomposition, and then correlate the EOG channelt to the ICA components.

## Constructing epochs (rejecting bad trials)

A stim channel (short for “stimulus channel”) is a channel that records voltages (usually sent from the experiment-controlling computer) that are time-locked to experimental events, such as the onset of a stimulus or a button-press response by the subject.

Based on the events recorded by this channel, we can chunk the data into epochs, specificying time before and time after stimulus presentation, for example 200ms before and 500ms after the event.

At this point we can reject any Epochs where the signal amplitude exceeds specified lower and upper bounds - for example 150uV and 250uV. Anything exceeding these are too large to have originated from the brain.

## Time frequency analysis

We can use Morlet wavelets (other methods can be used) to see a time-frequency analysis of each epoch. Plotting this can show the changes in frequency for given channel over time during the epoch.

## Constructing evoked responses from epochs

We simply average across trials to get the evoked repsonses from epochs.

## classification.py