from ConnectivityMeasures.connectivity import *
from ConnectivityMeasures.connectivity_context import *

def call_PLI_for_DEAP_subjects():
    """
    Functia este necesara pentru a apela pentru toti subiectii si toate trial-urile deodata functia care stabileste conectivitatea
    folosind metoda PLI.
    """

    subjects_path = os.path.join("Data", "DEAP Subjects")
    pli_strategy = PhaseLagIndexStrategy()
    context = ConnectivityContext(pli_strategy)
    for subject in os.listdir(subjects_path):
        print("Subject curent: ", subject)
        current_subject_path = os.path.join(subjects_path, subject)
        trials_path = os.path.join(current_subject_path, "Trials")
        for t in os.listdir(trials_path):
            print(" \tTrial curent: ", t)
            context.apply_connectivity_measure(current_subject_path, t, "Alpha", "PLI", 128)
            context.apply_connectivity_measure(current_subject_path, t, "Beta", "PLI", 128

def call_coherence_for_DEAP_subjects():
    """
    Functia este necesara pentru a apela pentru toti subiectii si toate trial-urile deodata functia care stabileste conectivitatea
    folosind coerenta.
    """

    subjects_path = os.path.join("Data", "DEAP Subjects")
    coherence_strategy = CoherenceStrategy()
    context = ConnectivityContext(coherence_strategy)
    for subject in os.listdir(subjects_path):
        current_subject_path = os.path.join(subjects_path, subject)
        trials = os.path.join(current_subject_path, "Trials")
        for t in os.listdir(trials):
            context.apply_connectivity_measure(current_subject_path, t, "Alpha", "coherence", 128)
            context.apply_connectivity_measure(current_subject_path, t, "Beta", "coherence", 128)

def call_WPLI_for_DEAP_subjects():
    """
    Functia este necesara pentru a apela pentru toti subiectii si toate trial-urile deodata functia care stabileste conectivitatea
    folosind modalitatea wPLI.
    """

    subjects_path = os.path.join("Data", "DEAP Subjects")
    wpli_strategy = WeightedPhaseLagIndexStrategy()
    context = ConnectivityContext(wpli_strategy)
    for subject in os.listdir(subjects_path):
        current_subject_path = os.path.join(subjects_path, subject)
        trials = os.path.join(current_subject_path, "Trials")
        for t in os.listdir(trials):
            context.apply_connectivity_measure(current_subject_path, t, "Alpha", "WPLI", 128)
            context.apply_connectivity_measure(current_subject_path, t, "Beta", "WPLI", 128)

#aplic o singura data metodele de conectivitate pentru toti subiectii
# call_PLI_for_DEAP_subjects()
# call_coherence_for_DEAP_subjects()
# call_WPLI_for_DEAP_subjects()