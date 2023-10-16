import csv
import os
import pandas as pd
import numpy as np
import pyedflib
import scipy.io
from configurations.config import ROOT_DIR

#conform indexarii datasetului DEAP am extras doar canalele necesare in acest proiect
channels_DEAP = {
        1: 'Fp1' ,
        3: 'F3'  ,
        4: 'F7'  ,
        7: 'C3'  ,
        8: 'T3'  ,
        11: 'P3' ,
        12: 'T4' ,
        14: 'O1' ,
        16: 'Pz' ,
        17: 'Fp2',
        19: 'Fz' ,
        20: 'F4' ,
        21: 'F8' ,
        24: 'Cz' ,
        25: 'C4' ,
        26: 'T5' ,
        29: 'P4' ,
        30: 'T6' ,
        32: 'O2'
}
def extract_trials():
    """
     Functia este responsabila cu selectia subiectilor relevanti acestui proiect, din setul de date DEAP. Se extrag doar trial-urile care
     au valorile pentru valenta si excitare astfel incat sa indice cadranele 1-3.
    """
    path = os.path.join(ROOT_DIR, "participant_ratings_initial.csv")
    df = pd.read_csv(path)
    condition1 = (df['Arousal'] > 5.5) & (df['Valence'] > 5.5)
    condition2 = (df['Arousal'] < 4) & (df['Valence'] < 4)

    filtered_df = df[condition1 | condition2]

    path_save = os.path.join("Data", "participant_ratings.csv")
    filtered_df.to_csv(path_save, index=False)

def create_directories(path, participant_id):
    subj_path = os.path.join(path, f'Subject{str(participant_id)}')
    if not os.path.exists(subj_path):
        os.mkdir(subj_path)

    trial_path = os.path.join(subj_path, "Trials")
    if not os.path.exists(trial_path):
        os.mkdir(trial_path)
    return trial_path

def read_file(file_name):
    """
    Functie de citire a semnalelor din format .mat, pentru fiecare trial asociat unui subiect.
    """
    subjects_path = os.path.join("Data", "DEAP Subjects")
    if not os.path.exists(subjects_path):
        os.mkdir(subjects_path)

    participant_id = ''.join([character for character in file_name if character.isdigit()])
    participants_info_path = os.path.join("Data", "participant_ratings.csv")
    info_df = pd.read_csv(participants_info_path)

    path = os.path.join(ROOT_DIR, "Data", "RawData", file_name)
    print("path: ", path)
    # dictionar cu 2 arrays: 'data' 40x40x8064 si 'labels' 40x4
    subject_data = scipy.io.loadmat(path)
    t = 0
    ch_counter = 0
    # iterez trial-urile conform participant_ratings.csv
    for trial in subject_data['data']:
        t += 1
        filtered_info_df = info_df[info_df['Participant_id'] == float(participant_id)]
        if t in filtered_info_df['Trial'].values:
            #creez dataframe-ul care o sa contina canalele trial-ului curent
            trial_df = pd.DataFrame(columns=channels_DEAP.values())
            ch_counter = 0
            print(f"trial: {t}")
            for channel in trial:
                ch_counter+=1
                if ch_counter in channels_DEAP.keys():
                    trial_df[channels_DEAP[ch_counter]]  =  channel
            trial_path = create_directories(subjects_path, participant_id)

            current_trial_path = os.path.join(trial_path, f'Trial {str(t)}')
            if not os.path.exists(current_trial_path):
                os.mkdir(current_trial_path)

            current_trial_path = os.path.join(current_trial_path, f'trial_{str(t)}.csv')
            # salvare in fisier .csv
            trial_df.to_csv(current_trial_path)

def read_all_DEAP_files():
    path = os.path.join(ROOT_DIR, "Data", "RawData")
    for filename in os.listdir(path):
        read_file(filename)

#apelez o singura data functia de citire
read_all_DEAP_files()