import os
import pandas as pd
import numpy as np
from configurations.config import ROOT_DIR

def create_dataframe_for_subject():
    """
    Functie necesara pentru crearea head-ului dataframe-urilor si pentru crearea primei coloane.
    """

    rows = ['C3', 'C4', 'Cz', 'F3', 'F4', 'F7', 'F8', 'Fp1', 'Fp2', 'Fz', 'O1', 'O2', 'P3', 'P4', 'Pz', 'T3', 'T4',
            'T5', 'T6']
    columns = ['C3', 'C4', 'Cz', 'F3', 'F4', 'F7', 'F8', 'Fp1', 'Fp2', 'Fz', 'O1', 'O2', 'P3', 'P4', 'Pz', 'T3',
               'T4', 'T5', 'T6']
    df = pd.DataFrame(index=rows, columns=columns)
    return df

def add_value_in_df(val, dataframe, row, column):
    dataframe.loc[row, column] = val

class ConnectivityContext:
    """
    Clasa  ConnectivityContext se ocupa cu aplicarea efectiva a strategiilor de calcul ale conectivitatii dintre nodurile grafurilor.
    """
    def __init__(self, connectivity_strategy):
        self.strategy = connectivity_strategy

    def apply_connectivity_measure(self, subject_path, trial, band_type, measure_type, fs):
        """
        Functia se ocupa cu aplicarea unei metode de conectivitate intre toti electrozii castii EEG, pentru un subiect si un treial specificat.
        Metoda de conectivitatea este aleasa prin intermediul parametrului  measure_type.
        """
        trial_path = os.path.join(subject_path, "Trials", trial)
        # creez folder pentru rezultatele metodei de conectivitate acurente, unde o sa am mai multe csv-uri, pt fiecare banda de frecventa.
        connectivity_directory = os.path.join(trial_path, f'{measure_type}')

        if not os.path.exists(connectivity_directory):
            os.mkdir(connectivity_directory)

        df = create_dataframe_for_subject()
        channels_path = os.path.join(trial_path, "Channels")
        # creez lista cu toate directoarele numite dupa electrozi
        channels_list = [d for d in os.listdir(channels_path)]
        for current_channel in range(len(channels_list)):
            channels_excluding_current_channel = channels_list
            channels_excluding_current_channel = [d for d in channels_list if d != current_channel]
            current_channel_path = os.path.join(trial_path, "Channels", channels_list[current_channel], f'{band_type}.csv')
            current_channel_dataframe = pd.read_csv(current_channel_path)
            current_channel_values = current_channel_dataframe[band_type].values

            # parcurg toti electrozii cu care trebuie sa calculez pli, wpli sau coerenta pt current_channel
            for folowing_channel in range(current_channel + 1, len(channels_list)):
                folowing_channel_path = os.path.join(trial_path, "Channels", channels_list[folowing_channel], f'{band_type}.csv')
                folowing_channel_dataframe = pd.read_csv(folowing_channel_path)
                folowing_channel_values = folowing_channel_dataframe[band_type].values
                connectivity_measure = self.strategy.compute_connectivity(current_channel_values, folowing_channel_values, fs)
                add_value_in_df(connectivity_measure, df, channels_list[current_channel], channels_list[folowing_channel])
        #dataaframeul este simetric, asa ca ii completez valorile din partea inferior triunghiulara cu ceele din partea superiror triunghiulara - transpus
        df = df.add(df.T, fill_value=0).fillna(df)
        if (measure_type != "coherence"):
            # populez Nan cu valoarea 0 pentru diagonala principala
            df = df.fillna(0)
        else:
            df = df.fillna(1)
        print(f"dataframe final pt subiectul {subject_path}, banda {band_type}, metoda de conectivitate {measure_type} este:\n {df}")
        # salveaza dataframe in .csv
        connectivity_path = os.path.join(connectivity_directory, f'{measure_type}_results_for_{band_type}_band.csv')
        df.to_csv(connectivity_path)