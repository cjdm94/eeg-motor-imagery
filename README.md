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

This script classifies whether subject has imagined moving their left or right arm.

## Filtering the data

We can easily filter the data between 7 and 30 Hz, which corresponds roughly to the frequencies expected during motor imagery (mu/alpha rhythms and beta rhythms).

You can play around with the exact numbers to maximise the classification accuracy.

## Constructing the epochs

We don't want to train on the whole time segment, because we know from experience that the motor imagery signal (event-related desynchronisation) is strongest shortly after the participant starts imaginging movement. Therefore, we crop the epochs to between 100ms and 200s after the motor imagery. We will then analyse the performance of the classifier over the entire segment, and we should expect maximal performance during this window.

## Cross validation of the classifier

Before we construct a classifier, we should follow proper machine learning protocol. Typically in machine learning you have a training dataset and a test dataset; the classifier will characterise one dataset, and then we must train it to classify datasets it hasn't yet seen.

To make optimal use of our limited number of trials (80-90), we will split our epochs into 10 groups, using the ShuffleSplit function. This function will use 9 groups as training data and test on the remaining group.

## Feature extraction

We use the common spatial patterns algorithm for feature extraction. The CSP algorithm is a sptial filter which takes the 64 EEG channels and weights them according to point at a source which shows a maximal power difference between the two conditions. When we run it, it should point at the left and right motor cortex because those will show the event-related desynchronisation that will tell us whether the left or right hand was imagined as moving. Instead of 64 EEG channels, we will use 4 "virtual" channels pointing to the motor cortex. We will therefore extract 4 features from the 64 channels, and we can visualise this topographically.

<img src=./img/extracted-features.png height="200px">

These are the weights given to each channel to construct the features/components. In the first component the left pre-motor area is lit up, and the third component focuses in on a source in the right pre-motor area. The 2nd and 4th components seem not to be very informative, but we keep them anyway - it is common practice to use 4 components for feature selection via CSP.

In summary, the 1st and 3rd components will probably tell our classifier whether the test data is left or right motor imagery.

## Classifier

We use a linear discriminant analysis as the classifier. We run the classifier on different windows of time surrounding the moment of motor imagery (this is what the loop is doing). This will show us the performance of the classifier over the course of the trials.

<img src=./img/classification-results.png height="200px">

We can see that between 1 and 1.5s the classifier was able to decode whether it was left or right-hand motor imagery with around 80-90% accuracy.
