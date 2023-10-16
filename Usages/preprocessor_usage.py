import os
from Classification.preprocessor import Preprocessor
from configurations.config import ROOT_DIR
"""
Fisierul contine apeluri de functii ale clasei Preprocessor pentru diverse subseturi de instante construite folosind 
setul de date DEAP si stocate in diferite fisiere. Sunt aplicate separat metode pentru instante ce contin atat trasaturi globale
cat si trasaturi globale imbinate cu trasaturi locale. 
"""
preprocessor = Preprocessor()
#preprocessor.preprocess_ratings()
subjects_path = os.path.join(ROOT_DIR, "Data", "DEAP Subjects")

#creare instante cu trasaturi globale nebalansate
preprocessor.compute_graph_metrics_alpha_beta_bands("coherence", subjects_path, 0)
preprocessor.compute_graph_metrics_alpha_beta_bands("PLI", subjects_path, 0)
preprocessor.compute_graph_metrics_alpha_beta_bands("WPLI", subjects_path, 0)

#creare instante cu trasaturi globale si locale  nebalansate
preprocessor.compute_graph_metrics_alpha_beta_bands("coherence", subjects_path, 1)
preprocessor.compute_graph_metrics_alpha_beta_bands("PLI", subjects_path, 1)
preprocessor.compute_graph_metrics_alpha_beta_bands("WPLI", subjects_path, 1)

#cai spre trasaturi neechilibrate, globale
global_pli_path_class_1 = os.path.join(ROOT_DIR,"Features", "global_features", "PLI_features_class_1.csv")
global_pli_path_class_0 = os.path.join(ROOT_DIR,"Features", "global_features", "PLI_features_class_0.csv")
global_coh_path_class_1 = os.path.join(ROOT_DIR,"Features", "global_features", "coherence_features_class_1.csv")
global_coh_path_class_0 = os.path.join(ROOT_DIR,"Features", "global_features", "coherence_features_class_0.csv")
global_wpli_path_class_1 = os.path.join(ROOT_DIR,"Features", "global_features", "WPLI_features_class_1.csv")
global_wpli_path_class_0 = os.path.join(ROOT_DIR,"Features", "global_features", "WPLI_features_class_0.csv")

#cai spre trasaturi neechilibrate, globale si locale
global_local_pli_path_class_1 = os.path.join(ROOT_DIR,"Features", "global_and_local_features", "PLI_features_class_1.csv")
global_local_pli_path_class_0 = os.path.join(ROOT_DIR,"Features", "global_and_local_features", "PLI_features_class_0.csv")
global_local_coh_path_class_1 = os.path.join(ROOT_DIR,"Features", "global_and_local_features", "coherence_features_class_1.csv")
global_local_coh_path_class_0 = os.path.join(ROOT_DIR,"Features", "global_and_local_features", "coherence_features_class_0.csv")
global_local_wpli_path_class_1 = os.path.join(ROOT_DIR,"Features", "global_and_local_features", "WPLI_features_class_1.csv")
global_local_wpli_path_class_0 = os.path.join(ROOT_DIR,"Features", "global_and_local_features", "WPLI_features_class_0.csv")

###################### operatii pentru trasaturi globale ########################
#balansez toate trasaturile globale
preprocessor.balance_instances(global_pli_path_class_0, global_pli_path_class_1, "balanced_global_features")
preprocessor.balance_instances(global_wpli_path_class_0, global_wpli_path_class_1, "balanced_global_features")
preprocessor.balance_instances(global_coh_path_class_0, global_coh_path_class_1, "balanced_global_features")

#path-uri spre trasaturile globale balansate
global_pli_path_class_1 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_features_class_1.csv")
global_pli_path_class_0 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_features_class_0.csv")
global_coh_path_class_1 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_coherence_features_class_1.csv")
global_coh_path_class_0 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_coherence_features_class_0.csv")
global_wpli_path_class_1 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_WPLI_features_class_1.csv")
global_wpli_path_class_0 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_WPLI_features_class_0.csv")

#concatenare trasaturi globale
global_features_concat_class_1 = preprocessor.concat_multiple_connectivity_types_features(global_pli_path_class_1, global_wpli_path_class_1, global_coh_path_class_1)
concat_global_features_path_class_1 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_WPLI_coherence_features_class_1_merged.csv")
global_features_concat_class_1.to_csv(concat_global_features_path_class_1, index = False)

global_features_concat_df_class_0 = preprocessor.concat_multiple_connectivity_types_features(global_pli_path_class_0, global_wpli_path_class_0, global_coh_path_class_0)
concat_global_features_path_class_0 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_WPLI_coherence_features_class_0_merged.csv")
global_features_concat_df_class_0.to_csv(concat_global_features_path_class_0, index = False)


###################### operatii pentru trasaturi globale si locale #######################
# balansez toate trasaturile globale si locale
preprocessor.balance_instances(global_local_pli_path_class_0, global_local_pli_path_class_1, "balanced_global_and_local_features")
preprocessor.balance_instances(global_local_wpli_path_class_0, global_local_wpli_path_class_1, "balanced_global_features")
preprocessor.balance_instances(global_local_coh_path_class_0, global_local_coh_path_class_1, "balanced_global_features")

#cai spre trasaturi echilibrate, globale si locale
global_local_pli_path_class_1 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_pli_features_class_1.csv")
global_local_pli_path_class_0 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_pli_features_class_0.csv")
global_local_coh_path_class_1 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_coherence_features_class_1.csv")
global_local_coh_path_class_0 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_coherence_features_class_0.csv")
global_local_wpli_path_class_1 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_WPLI_features_class_1.csv")
global_local_wpli_path_class_0 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_WPLI_features_class_0.csv")

#concatenare trasaturi globale si locale
global_local_features_concat_class_1 = preprocessor.concat_multiple_connectivity_types_features(global_local_pli_path_class_1, global_local_wpli_path_class_1, global_local_coh_path_class_1)
concat_local_global_features_path_class_1 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_PLI_WPLI_coherence_features_class_1_merged.csv")
global_local_features_concat_class_1.to_csv(concat_local_global_features_path_class_1, index = False)

global_features_concat_df_class_0 = preprocessor.concat_multiple_connectivity_types_features(global_local_pli_path_class_0, global_local_wpli_path_class_0, global_local_coh_path_class_0)
concat_global_features_path_class_0 = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_PLI_WPLI_coherence_features_class_0_merged.csv")
global_features_concat_df_class_0.to_csv(concat_global_features_path_class_0, index = False)
