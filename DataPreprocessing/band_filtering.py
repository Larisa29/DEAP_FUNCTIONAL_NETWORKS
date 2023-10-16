import csv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyedflib
from scipy.signal import butter, lfilter
from configurations.config import ROOT_DIR

def butterworth_bandpass(lowcut, highcut, sampling_freq, order=5):
    """
    Metoda responsabila pentru obtinerea coeficientilor necesari filtrului Butterworth, unde lowcut si highcut sunt frecventele de taiere.
    """
    nyq = 0.5 * sampling_freq
    #nomalizez frecventele de taiere
    low = lowcut / nyq
    high = highcut / nyq
    numerator, denominator = butter(order, [low, high], btype='band')
    return numerator,denominator

def butterworth_bandpass_filter(data, lowcut, highcut, sampling_freq, order=5):
    """
    Metoda necesara pentru filtrarea semnalului dat prin parametrul 'data', folosind filtrul Butterworth, unde lowcut si highcut
    sunt frecventele de taiere.
    """
    numerator, denominator = butterworth_bandpass(lowcut, highcut, sampling_freq, order=order)
    filtered_signal = lfilter(numerator, denominator, data)
    return filtered_signal

def determine_band_parameters(band_type):
    """
    Functie prin care se stabileste intervalul de frecvente asociat fiecarei benzi folosite in proiect.
    """
    low = 0
    high = 0
    match band_type:
        case "Alpha":
            low = 8
            high = 13
        case "Beta":
            low =  13.5
            high = 30
        case "Theta":
            low = 4
            high = 8

    return low, high

def create_filtered_bands_files_for_subject(trial_dataframe, channels_directory, band_type, lowcut, highcut, fs):
    """
    Functie pentru crearea fisierelor unde vor fi stocate semnalele impartite pe benzi de frecventa.
    """
    for (channel_label, channel_data) in trial_dataframe.items():
        current_channel_path = os.path.join(channels_directory, channel_label)
        if not os.path.exists(current_channel_path):
            os.mkdir(current_channel_path)
        band_path = os.path.join(channels_directory, channel_label, f'{band_type}.csv')
        values_for_channel = np.array(channel_data.values)  # valorile canalului curent
        filtered_band = butterworth_bandpass_filter(values_for_channel, lowcut, highcut, fs)
        print(f'banda {band_type} pt canalul {channel_label} este {filtered_band} \n')
        if not os.path.exists(band_path):
            fp = open(band_path, 'w')
            fp.write(band_type + "\n")
            for i in filtered_band:
                fp.write(str(i) + '\n')
            fp.close()

def bands_separation(band_type, root_path, sampling_freq):
    """
    Functie pentru separarea efectiva a semnalelor in benzi de frecventa pentru fiecare subiect si fiecare trial.
    """
    lowcut, highcut = determine_band_parameters(band_type)
    for subject in os.listdir(root_path):
        subject_path = os.path.join(root_path, subject)
        trials_path = os.path.join(subject_path, 'Trials')

        if not os.path.exists(trials_path):
            return

        for trial in os.listdir(trials_path):
            trial_path = os.path.join(trials_path, trial)
            if os.path.isdir(trial_path):
                channels_path = os.path.join(trial_path, 'Channels')
                if not os.path.exists(channels_path):
                    os.mkdir(channels_path)
                for file_name in os.listdir(trial_path):
                    if file_name.endswith('.csv'):
                        trial_data = os.path.join(trial_path, file_name)
                        trial_dataframe = pd.read_csv(trial_data, index_col=0)
                        create_filtered_bands_files_for_subject(trial_dataframe, channels_path, band_type, lowcut, highcut, sampling_freq)
