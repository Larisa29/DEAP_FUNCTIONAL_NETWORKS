import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

class BaseClassifier():
    """ Clasa de baza pentru cei doi clasificatori implementati: Random Forest si SVM."""
    def __init__(self, path0, path1):
        self.path0 = path0
        self.path1 = path1

    def load_and_shuffle_data(self):
        """
        Functia preia doua fisiere ce contin instante pentru clasa 0 si clasa 1, le concateneaza si le amesteca intr-o ordine aleatoare,
        returnand setul de date final obtinut.
        """
        first_dataset = pd.read_csv(self.path0)
        second_dataset = pd.read_csv(self.path1)
        dataset = pd.concat([first_dataset, second_dataset])
        shuffled_dataset = dataset.sample(frac=1)
        dataset = shuffled_dataset.reset_index(drop=True)

        return dataset

    def plot_confusion_matrix(self, confusion_matrix, classes, accuracy):
        """
        Functia este necesara pentru a genera matricile de confuzie in urma clasificarii. Se ataseaza si acuratetea obtinuta, pentru
        o interpretare mai clara a rezultatelor.
        """
        plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Greens)
        plt.title('Matrice de confuzie')
        plt.text(0.5, -0.1, f'Acuratețe: {round(accuracy * 100, 2)}%', ha='center', va='center', transform=plt.gca().transAxes)
        plt.colorbar()
        plt.xticks(np.arange(len(classes)), classes, rotation=45)
        plt.yticks(np.arange(len(classes)), classes)
        for i in range(len(classes)):
            for j in range(len(classes)):
                if confusion_matrix[i][j] > confusion_matrix.max() / 1.5:
                    font_color = 'white'
                else:
                    font_color = 'black'
                plt.text(j, i, str(confusion_matrix[i][j]), ha='center', va='center', color=font_color)
        plt.show()
