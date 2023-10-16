from Classification.random_forest import RandomForest_classifier
from Classification.svm import SVM_classifier
from configurations.config import ROOT_DIR
import os

"""
Fisiser ce contine apeluri pentru clasificatori, in functie de trasaturile pe care vrem sa le folosim pentru antrenare. Rezultatele
fiecarei clasificari sunt pastrate in fisiere text in folderul ClassificationResults.
"""

def apply_RF_PLI_global_features():
    pli_path_class_1 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_features",
                                    "balanced_pli_features_class_1.csv")
    pli_path_class_0 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_features",
                                    "balanced_pli_features_class_0.csv")
    random_forest = RandomForest_classifier(pli_path_class_1, pli_path_class_0)
    dataset_shuffled = random_forest.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults" , "RandomForest_Classification", "output_balanced_pli_global_metrics_random_forest.txt")
    random_forest.cross_validation_random_forest(dataset_shuffled, 5, output)
# apply_RF_PLI_global_features()

def apply_RF_PLI_global_and_local_features():
    pli_path_class_1 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_pli_features_class_1.csv")
    pli_path_class_0 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_pli_features_class_0.csv")
    random_forest = RandomForest_classifier(pli_path_class_1, pli_path_class_0)
    dataset_shuffled = random_forest.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults" , "RandomForest_Classification", "output_balanced_pli_local_global_metrics_random_forest.txt")
    random_forest.cross_validation_random_forest(dataset_shuffled, 5, output)
#apply_RF_PLI_global_and_local_features()

# apel random forest pentru wPLI balansat, cu trasaturi de graf si cele de nod
def apply_RF_wPLI_global_and_local_features():
    wpli_path_class_1 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_WPLI_features_class_1.csv")
    wpli_path_class_0 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_WPLI_features_class_0.csv")
    random_forest = RandomForest_classifier(wpli_path_class_1, wpli_path_class_0)
    dataset_shuffled = random_forest.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults" , "RandomForest_Classification", "output_balanced_w-pli_local_global_metrics_random_forest.txt")
    random_forest.cross_validation_random_forest(dataset_shuffled, 5, output)
#apply_RF_wPLI_global_and_local_features()


# apel random forest pentru coerenta balansat, cu trasaturi globale si locale
def apply_RF_coherence_global_and_local_features():
    coherence_path_class_1 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_coherence_features_class_1.csv")
    coherence_path_class_0 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_coherence_features_class_0.csv")
    random_forest = RandomForest_classifier(coherence_path_class_1, coherence_path_class_0)
    dataset_shuffled = random_forest.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults" , "RandomForest_Classification", "output_balanced_coherence_local_global_metrics_random_forest.txt")
    random_forest.cross_validation_random_forest(dataset_shuffled, 5, output)
# apply_RF_coherence_global_and_local_features()

#APEL PT wPLI trasaturi globale
def apply_RF_wpli_global_features():
    global_wpli_path_class_1_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_WPLI_features_class_1.csv")
    global_wpli_path_class_0_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_WPLI_features_class_0.csv")
    random_forest = RandomForest_classifier(global_wpli_path_class_1_balanced, global_wpli_path_class_0_balanced)
    dataset_shuffled = random_forest.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "RandomForest_classification", "output_balanced_wpli_global_metrics_random_forest.txt")
    random_forest.cross_validation_random_forest(dataset_shuffled, 5, output)
#apply_RF_wpli_global_features()

#apel pt coerenta trasaturi globale
def apply_RF_coherence_global_features():
    global_coherence_path_class_1_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_coherence_features_class_1.csv")
    global_coherence_path_class_0_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_coherence_features_class_0.csv")
    random_forest = RandomForest_classifier(global_coherence_path_class_1_balanced, global_coherence_path_class_0_balanced)
    dataset_shuffled = random_forest.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "RandomForest_classification", "output_balanced_cohernece_global_metrics_random_forest.txt")
    random_forest.cross_validation_random_forest(dataset_shuffled, 5, output)
# apply_RF_coherence_global_features()

#aplic RF pt trasaturile globale, pentru toate metodele concatenate
def apply_RF_pli_wpli_coherence_global_features():
    global_concat_path_class_1_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_WPLI_coherence_features_class_1_merged.csv")
    global_concat_path_class_0_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_WPLI_coherence_features_class_0_merged.csv")
    random_forest = RandomForest_classifier(global_concat_path_class_1_balanced, global_concat_path_class_0_balanced)
    dataset_shuffled = random_forest.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "RandomForest_classification", "output_balanced_pli_wpli_cohernece_global_metrics_random_forest.txt")
    random_forest.cross_validation_random_forest(dataset_shuffled, 5, output)
#apply_RF_pli_wpli_coherence_global_features()

#aplic RF pt trasaturile globale si locale, pentru toate metodele concatenate
def apply_RF_pli_wpli_coherence_global_local_features():
    global_concat_path_class_1_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_PLI_WPLI_coherence_features_class_1_merged.csv")
    global_concat_path_class_0_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_PLI_WPLI_coherence_features_class_0_merged.csv")
    random_forest = RandomForest_classifier(global_concat_path_class_1_balanced, global_concat_path_class_0_balanced)
    dataset_shuffled = random_forest.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "RandomForest_classification", "output_balanced_pli_wpli_cohernece_global_local_metrics_random_forest.txt")
    random_forest.cross_validation_random_forest(dataset_shuffled, 5, output)
#apply_RF_pli_wpli_coherence_global_local_features()

#aplicare SVM pentru trasaturi locale si globale, pentru metode individuale
def apply_SVM_pli_global_local_features():
    pli_path_class_1 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_pli_features_class_1.csv")
    pli_path_class_0 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_pli_features_class_0.csv")
    svm = SVM_classifier(pli_path_class_1, pli_path_class_0)
    dataset_shuffled = svm.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults" , "SVM_Classification", "output_balanced_pli_local_global_metrics_svm.txt")
    svm.cross_validation_svm(dataset_shuffled, 5, output)
#apply_SVM_pli_global_local_features()

def apply_SVM_wpli_global_local_features():
    global_wpli_path_class_1_balanced = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_features", "balanced_WPLI_features_class_1.csv")
    global_wpli_path_class_0_balanced = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_features", "balanced_WPLI_features_class_0.csv")
    svm = SVM_classifier(global_wpli_path_class_1_balanced, global_wpli_path_class_0_balanced)
    dataset_shuffled = svm.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults" , "SVM_Classification", "output_balanced_wpli_local_global_metrics_svm.txt")
    svm.cross_validation_svm(dataset_shuffled, 5, output)
# apply_SVM_wpli_global_local_features()

# apel SVM pentru coerenta balansat, cu trasaturi globale si locale
def apply_SVM_coherence_global_and_local_features():
    coherence_path_class_1 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_coherence_features_class_1.csv")
    coherence_path_class_0 = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_and_local_features",
                                    "balanced_coherence_features_class_0.csv")
    svm = SVM_classifier(coherence_path_class_1, coherence_path_class_0)
    dataset_shuffled = svm.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults" , "SVM_Classification", "output_balanced_coherence_local_global_metrics_svm.txt")
    svm.cross_validation_svm(dataset_shuffled, 5, output)
# apply_SVM_coherence_global_and_local_features()

#APEL PT wPLI trasaturi globale
def apply_SVM_pli_global_features():
    global_pli_path_class_1_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_features_class_1.csv")
    global_pli_path_class_0_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_features_class_0.csv")
    svm = SVM_classifier(global_pli_path_class_1_balanced, global_pli_path_class_0_balanced)
    dataset_shuffled = svm.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "SVM_Classification", "output_balanced_pli_global_metrics_svm.txt")
    svm.cross_validation_svm(dataset_shuffled, 2, output)
# apply_SVM_pli_global_features()

#APEL PT wPLI trasaturi globale
def apply_SVM_wpli_global_features():
    global_wpli_path_class_1_balanced = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_features", "balanced_WPLI_features_class_1.csv")
    global_wpli_path_class_0_balanced = os.path.join(ROOT_DIR, "Features", "balanced_features", "balanced_global_features", "balanced_WPLI_features_class_0.csv")
    svm = SVM_classifier(global_wpli_path_class_1_balanced, global_wpli_path_class_0_balanced)
    dataset_shuffled = svm.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "SVM_Classification", "output_balanced_wpli_global_metrics_svm.txt")
    svm.cross_validation_svm(dataset_shuffled, 5, output)
# apply_SVM_wpli_global_features()

#APEL PT wPLI trasaturi globale
def apply_SVM_coherence_global_features():
    global_coherence_path_class_1_balanced = os.path.joi n(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_coherence_features_class_1.csv")
    global_coherence_path_class_0_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_coherence_features_class_0.csv")
    svm = SVM_classifier(global_coherence_path_class_1_balanced, global_coherence_path_class_0_balanced)
    dataset_shuffled = svm.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "SVM_Classification", "output_balanced_coherence_global_metrics_svm.txt")
    svm.cross_validation_svm(dataset_shuffled, 5, output)
# apply_SVM_coherence_global_features()

#aplic SVM pt trasaturile globale, pentru toate metodele concatenate
def apply_SVM_pli_wpli_coherence_global_features():
    global_concat_path_class_1_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_WPLI_coherence_features_class_1_merged.csv")
    global_concat_path_class_0_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_features", "balanced_PLI_WPLI_coherence_features_class_0_merged.csv")
    svm = SVM_classifier(global_concat_path_class_1_balanced, global_concat_path_class_0_balanced)
    dataset_shuffled = svm.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "SVM_Classification", "output_balanced_pli_wpli_cohernece_global_metrics_svm.txt")
    svm.cross_validation_svm(dataset_shuffled, 5, output)
#apply_SVM_pli_wpli_coherence_global_features()

#aplic SVM pt trasaturile globale, pentru toate metodele concatenate
def apply_SVM_pli_wpli_coherence_global_local_features():
    global_concat_path_class_1_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_PLI_WPLI_coherence_features_class_1_merged.csv")
    global_concat_path_class_0_balanced = os.path.join(ROOT_DIR,"Features", "balanced_features", "balanced_global_and_local_features", "balanced_PLI_WPLI_coherence_features_class_0_merged.csv")
    svm = SVM_classifier(global_concat_path_class_1_balanced, global_concat_path_class_0_balanced)
    dataset_shuffled = svm.load_and_shuffle_data()
    output = os.path.join(ROOT_DIR, "ClassificationResults", "SVM_Classification", "output_balanced_pli_wpli_coherence_local_global_metrics_svm.txt")
    svm.cross_validation_svm(dataset_shuffled, 5, output)
#apply_SVM_pli_wpli_coherence_global_local_features()