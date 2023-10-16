import pandas as pd
import os
import numpy as np
import re
from configurations.config import ROOT_DIR
from Graphs.graph_visualization import GraphHandler
from Graphs.compute_metrics import GraphMetrics

def compute_instance_head(connectivity_measure, band, features_flag):
    """
    Metoda defineste denumirile coloanelor instantelor si ordinea de aparitie a trasaturilor globale si/sau locale la clasificare.
    Parametrul features_flag = 1 atunci cand se doreste considerarea atat a trasaturilor globale,
    cat si a celor locale. Pentru trasaturi globale features_flag ia valoarea 0.
    """

    channels = np.array(['Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'T3', 'T4', 'C3', 'C4', 'T5', 'T6', 'P3', 'P4', 'O1', 'O2', 'Fz', 'Cz','Pz'])
    channels_sorted = channels.sort()
    deap_cols = [f'{connectivity_measure}_{band}_cost',
                 f'{connectivity_measure}_{band}_lungime_medie',
                 f'{connectivity_measure}_{band}_coeficient_clusterizare',
                 f'{connectivity_measure}_{band}_eficienta_globala',
                 ]
    if features_flag == 1:
        for ch in channels:
            pattern_DC = f'{ch}_{connectivity_measure}_{band}_DC'  #centralitatea gradului
            deap_cols.append(pattern_DC)

        for ch in channels:
            pattern_BC = f'{ch}_{connectivity_measure}_{band}_BC'  #centralitatea de intermediere
            deap_cols.append(pattern_BC)

    return deap_cols

class Preprocessor:
    def preprocess_ratings(self):
        """
        Functia este responsabila cu determinarea claselor de care apartin subiectii, in functie de valorile scorurilor date. Se vor
        stoca intr-un fisier .csv toate scorurile si clasele asociate.
        """
        emotions = []
        ratings_path = os.path.join(ROOT_DIR, "Data", "participant_ratings.csv")
        ratings_df = pd.read_csv(ratings_path)
        for row in range(len(ratings_df)):
            if ratings_df.loc[row, 'Valence'] < 4 and ratings_df.loc[row, 'Arousal'] < 4:
                emotions.append(0) #nefericirea are asociata valoarea 0
            elif ratings_df.loc[row, 'Valence'] > 5.5 and ratings_df.loc[row, 'Arousal'] > 5.5:
                emotions.append(1)  # fericirea are asociata valoarea 1
        ratings_df['Emotion'] = emotions

        #adaug coloana 'emotie'
        path_save = os.path.join(ROOT_DIR, "Data", "participant_ratings_class.csv")
        ratings_df.to_csv(path_save, index=False)
        print("Nr de instante din fiecare clasa este: \n", ratings_df['Emotion'].value_counts())

    def balance_instances(self, df1_path, df2_path, metrics_type):
        """
        Functia este responsabila cu echilibrarea instantelor - df1 este un dataframe ce contine doar instante dint-o singura clasa, iar df2
        contine doar instante din clasa opusa. Se stocheaza in final, in doua fisiere separate, un numar egal de instante din fiecare tip de clasa.
        """
        df1 = pd.read_csv(df1_path)
        df2 = pd.read_csv(df2_path)
        if len(df1) > len(df2):
            df1 = df1.sample(len(df2))
        elif len(df1) < len(df2):
            df2 = df2.sample(len(df1))

        saved_df1_path = os.path.join(ROOT_DIR, "Features", "balanced_features", metrics_type, f'balanced_{os.path.basename(df1_path)}')
        saved_df2_path = os.path.join(ROOT_DIR, "Features", "balanced_features", metrics_type, f'balanced_{os.path.basename(df2_path)}')

        df1.to_csv(saved_df1_path, index=False)
        df2.to_csv(saved_df2_path, index=False)

    def concat_multiple_connectivity_types_features(self, df1_connectivity_type_path, df2_connectivity_type_path, df3_connectivity_type_path):#vreau sa concatenez instantele de PLI, wpli si coherence aici pentru aceeasi clasa
        """
        Functia este responsabila cu concatenarea unor obiecte de tip dataframe dupa coloane. Rezultatul returnat este un dataframe cu informatiile
        din trei dataframe-uri reunite.
        """
        df1 = pd.read_csv(df1_connectivity_type_path)
        df2 = pd.read_csv(df2_connectivity_type_path)
        df3 = pd.read_csv(df3_connectivity_type_path)
        df1.drop('emotie', axis=1, inplace=True)
        df2.drop('emotie', axis=1, inplace=True)
        features_df = pd.concat([df1, df2, df3], axis=1)
        return features_df

    def compute_graph_metrics_alpha_beta_bands(self, connectivity_measure, deap_subjects_path, features_flag):
        """
        Functia este responsabila cu crearea instantelor de antrenare in forma lor initiala, neechilibrata. Sunt construite instante
        care pot contine doar metrici globale, atunci cand features_flag=0, sau sunt construite instante cu metrici globale si locale
        atunci cand features_flag=1. Cele doua tipuri sunt pastrate in directoare separate. Instanele claselor 0 sunt pastrate in fisiere
        .csv distincte fata de cele ale clasei 1.
        """

        alpha_features_cols = compute_instance_head(connectivity_measure, "alpha", features_flag)
        beta_features_cols = compute_instance_head(connectivity_measure, "beta", features_flag)
        deap_cols = alpha_features_cols + beta_features_cols
        deap_cols.append('emotie')
        metrics_df = pd.DataFrame(columns=deap_cols)
        print(metrics_df.head())

        participant_ratings_path = os.path.join(ROOT_DIR, "Data", "participant_ratings_class.csv")
        participant_ratings_df = pd.read_csv(participant_ratings_path)

        #sortez participantii alfabetic pentru a pastra o ordine coerenta si usor de urmarit
        subjects = sorted(os.listdir(deap_subjects_path))
        for subject in subjects:
            # preiau ultimele doua carcatere din denumirea subiectului
            subject_id = subject[-2:]
            if subject_id[0] == '0':
                subject_id = subject_id[1:]
            subject_id = int(subject_id)

            trials_path = os.path.join(deap_subjects_path, subject, "Trials")
            #sortez trialurile crescator, dupa numarul trial-ului extras din denumirea directoarelor
            trials = sorted(os.listdir(trials_path), key=lambda x: int(x.split(" ")[-1]))
            for trial in trials:
                #extrag numarul efectiv al trial-ului
                trial_id = int(trial.split(" ")[-1])
                new_instance = []
                connectivity_measure_directory_path = os.path.join(trials_path, trial, connectivity_measure)
                connectivity_measure_directory = sorted(os.listdir(connectivity_measure_directory_path))
                for file in connectivity_measure_directory:
                    band_path = os.path.join(connectivity_measure_directory_path, file)
                    if os.path.isfile(band_path):
                        if "Theta" not in band_path:
                            graph_handler = GraphHandler(band_path)
                            graph = graph_handler.create_graph()
                            metrics = GraphMetrics(graph)
                            cost = metrics.average_cost()
                            average_path_length = metrics.average_path_length()
                            clustering_coefficient = metrics.clustering_coefficient_using_nx()
                            global_efficiency = metrics.global_efficiency()
                            if features_flag == 1:
                                degree_centrality = metrics.degree_centrality()
                                betweeness_centrality = metrics.betweenness_centrality()

                            new_instance.append(cost)
                            new_instance.append(average_path_length)
                            new_instance.append(clustering_coefficient)
                            new_instance.append(global_efficiency)
                            if features_flag == 1:
                                # am grija sa adaug nodurile in ordine alfabetica in instante, asa e stabilit patternul pentru trasaturi
                                for key in sorted(degree_centrality.keys()):
                                    new_instance.append(degree_centrality[key])

                                for key in sorted(betweeness_centrality.keys()):
                                    new_instance.append(betweeness_centrality[key])

                #folosesc un query pentru a extrage din fisierul cu scoruri exact clasa subiectului si trial-ului indicate
                new_instance_class = participant_ratings_df.query("Participant_id == @subject_id and Trial == @trial_id")['Emotion'].values[0]
                new_instance.append(new_instance_class)
                metrics_df.loc[len(metrics_df)] = new_instance
        # separ instantele cu clasa 0 intr-un fisier, iar pe cele cu clasa 1 in alt fisier .csv
        df_class_0 = metrics_df[metrics_df['emotie'] == 0]
        df_class_1 = metrics_df[metrics_df['emotie'] == 1]

        file_name = connectivity_measure
        if features_flag == 1:
            specific_features_type_dir = "global_and_local_features"
        else:
            specific_features_type_dir = "global_features"

        features_path_class_0 = os.path.join(ROOT_DIR,'Features', specific_features_type_dir, f'{connectivity_measure}_features_class_0.csv')
        if not os.path.exists(features_path_class_0):
            df_class_0.to_csv(features_path_class_0, index=False)

        features_path_class_1 = os.path.join(ROOT_DIR, 'Features', specific_features_type_dir, f'{connectivity_measure}_features_class_1.csv')
        if not os.path.exists(features_path_class_1):
            df_class_1.to_csv(features_path_class_1, index=False)

