import numpy as np
import pandas as pd
import sys
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
from sklearn.model_selection import StratifiedKFold
from Classification.base_classifier import BaseClassifier
from sklearn.metrics import classification_report, confusion_matrix

class SVM_classifier(BaseClassifier):
    def __init__(self, path0, path1):
        super().__init__(path0, path1)
    def train_svm(self, X_train, y_train):
        """
        Functie responsabila cu antrenarea clasificatorului SVM pentru setul de antrenare X_train si clasele corespondente
        y_train.
        """
        svm = SVC()
        svm.fit(X_train, y_train)
        return svm

    def test_svm(self, svm, X_test, y_test):
        """
        Functie responsabila cu testarea clasificatorului SVM pentru setul de antrenare X_test si clasele corespondente
        y_test.
        """
        y_pred = svm.predict(X_test)
        current_confusion_matrix = confusion_matrix(y_test, y_pred)
        # print("Instante de test: ", X_test)
        array_test = y_test.to_numpy()
        print("Clase reale: \n", array_test)
        zero_counter = len(array_test) - np.count_nonzero(array_test)
        one_counter = np.count_nonzero(array_test)
        print("Numarul de zero-uri din setul initial:", zero_counter)
        print("Numarul de unu-uri din setul initial:", one_counter)
        print("Clase predicted de SVM: \n", y_pred)
        accuracy = accuracy_score(y_test, y_pred)  # compara etichetele obtinute cu cele reale, facand raport intre nr predictii orecte/nr total instante
        print(classification_report(array_test, y_pred))
        return accuracy, current_confusion_matrix

    def cross_validation_svm(self, dataset, number_of_batches, output_file):
        """
        Functie care realizeaza validarea incrucisata pentru un set de date dat ca parametru. Se impart datele intr-un numar de subdiviziuni, dat prin
        parametrul number_of_batches, iar rezultatele fiecarei iteratii sunt pastrate in fisiere pentru a putea urmari performantele asociate
        fiecarei subdiviziuni.
        """
        original_stdout = sys.stdout
        target_label = dataset.columns[-1]
        accuracy_scores_list = []
        stratified_k_fold = StratifiedKFold(n_splits=number_of_batches, shuffle=True, random_state=1)
        X = dataset.drop(target_label, axis=1)
        target = dataset[target_label]
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        fold = 1
        with open(output_file, 'w') as f:
            sys.stdout = f
            # initializez matricea de confuzie
            confusion_mat = np.zeros((2, 2))
            #train_index si test_index sunt liste de indecsi
            for train_index, test_index in stratified_k_fold.split(X, target):
                X_train_fold, X_test_fold = X.iloc[train_index], X.iloc[test_index]
                y_train_fold, y_test_fold = target.iloc[train_index], target.iloc[test_index]
                print("FOLD: ", fold)
                print(f"Instantele de antrenare sunt: \n {X_train_fold} \n", flush=True)
                print(f"Clasele de antrenare sunt: \n {y_train_fold} \n", flush=True)
                print(f"Instantele de test sunt: \n {y_test_fold} \n", flush=True)
                print(f"Exista {len(y_test_fold)} instante de test")
                svm = self.train_svm(X_train_fold, y_train_fold)
                accuracy, current_fold_conf_matrix = self.test_svm(svm, X_test_fold, y_test_fold)
                print(f"Acuratetea pt fold {fold} este {accuracy} \n")
                print(f"Matricea de confuzie pt fold {fold} este: \n", current_fold_conf_matrix)
                confusion_mat += current_fold_conf_matrix
                accuracy_scores_list.append(accuracy)
                fold += 1
            average_accuracy = sum(accuracy_scores_list) / len(accuracy_scores_list)
            print(f"ACURATETEA MEDIE DETERMINATA ESTE {average_accuracy} \n")
            print("Matricea de confuzie finala este: \n", confusion_mat)
            classes = ["happy", "sad"]
            super().plot_confusion_matrix(confusion_mat, classes, average_accuracy)

        sys.stdout = original_stdout