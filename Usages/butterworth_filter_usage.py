from DataPreprocessing.band_filtering import *

def call_separate_bands_for_DEAP():
    """
    Functie necesara pentru separarea benzilor de frecventa pentru toti subiectii.
    """
    #separarea canelelor pe benzi, subiecti din DEAP
    root_path = os.path.join(ROOT_DIR, "Data", "DEAP Subjects")
    bands_separation("Alpha", root_path, 128)
    bands_separation("Beta",  root_path, 128)
    bands_separation("Theta", root_path, 128)

#apelez o singura data functia de separare a tuturor semnaleleor pt toti subiectii din DEAP
# call_separate_bands_for_DEAP()

