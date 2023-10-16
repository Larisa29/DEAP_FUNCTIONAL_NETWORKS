import networkx as nx
import matplotlib.pyplot as plt
import os
import matplotlib.colors as colors
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from PIL import Image

from configurations.config import ROOT_DIR
class GraphHandler:
    """
    Clasa GraphHandler se ocupa cu procesarile ce au loc la nivel de graf: crearea grafurilor si vizualizarea acestora.
    """
    # atribut partajat intre toate instantele
    NODE_POSITIONS = {
        'Fp1': (250, 140),
        'Fp2': (470, 140),
        'F7': (130, 240),
        'F3': (260, 250),
        'Fz': (362, 162),
        'F4': (500, 250),
        'F8': (600, 240),
        'T3': (100, 380),
        'C3': (230, 380),
        'Cz': (375, 380),
        'C4': (500, 380),
        'T4': (630, 380),
        'P3': (270, 500),
        'Pz': (360, 600),
        'P4': (450, 500),
        'T5': (150, 520),
        'O1': (235, 620),
        'T6': (600, 520),
        'O2': (500, 620)
    }

    def __init__(self, path):
        self.path = path

    def create_graph(self):
        """
        Functie responsabila cu crearea grafurilor, folosind nodurile date de NODE_POSITIONS. Se folosesc rezultatele calculate in etape
        anterioare, fiind preluate din fisier .csv. Se pastreaza in graf doar un anumit numar de muchii, adica cele a caror pondere
        depaseste un prag specific.
        """
        graph = nx.Graph()
        graph.add_nodes_from(GraphHandler.NODE_POSITIONS.keys())
        #preluare rezultate intermediare ale unei metrici specifice de conectivitate pentru o banda
        connectivity_dataframe = pd.read_csv(self.path, index_col=0)

        edges_list = []
        # traversez dataframe linie cu linie pentru a construi o lista de tuple: sursa-destinatie-weight
        for index_row, row in connectivity_dataframe.iterrows():
            for col_name, value in row.items():
                if (index_row != col_name):
                    edges_list.append((index_row, col_name, value))

        percentile = 60
        edges_weights = []
        for edge in edges_list:
            edges_weights.append(edge[2])

        #pragul va fi o valoare sub care conexiunile sunt considerate mai slabe si vor fi excluse din retea
        threshold = np.percentile(edges_weights, percentile)
        #selectez conexiunile care depasesc thresholdul
        for edge in edges_list:
            if edge[2] >= threshold:
                graph.add_edge(edge[0], edge[1], weight=edge[2])
        return graph

    def visualize_graph(self, graph):
        """
        Functia preia un graf ca argument si ii construieste o reprezentare vizuala. Legaturile dintre noduri au asociate diferite culori,
        pentru a marca intensitatea lor si rolul in graf.
        """
        img_path = os.path.join(ROOT_DIR, "Resources","eeg.png")
        img = Image.open(img_path)
        #creez o lista care imi zice toate weighturile pe care le am pt a le putea normaliza si mapa la o paleta de culori
        weights = []
        # data = dictionar cu info. aditionale despre muchii
        for u, v, data in graph.edges(data=True):
            weights.append(data['weight'])
        min_weight = min(weights)
        max_weight = max(weights)

        #definesc gradientul(color map-ul)
        cmap = colors.LinearSegmentedColormap.from_list('mycmap', [(0, 'green'), (0.5, 'yellow'),(1, 'red')])
        c_norm = colors.Normalize(vmin=min_weight, vmax=max_weight)
        #creez un obiect ScalarMappable util pt a mapa weight-urile muchiilor la o culoare din cmap
        scalar_map = cm.ScalarMappable(norm=c_norm, cmap=cmap)

        color_map = []
        for weight in weights:
            rgba_color = scalar_map.to_rgba(weight)
            #creez lista cu culorile folosite pt a o folosi la adaugarea muchiilor in graf
            color_map.append(rgba_color)

        fig, ax = plt.subplots(figsize=(12, 8))
        #adaug imaginea in fig
        ax.imshow(img)
        nx.draw_networkx_nodes(graph, pos=GraphHandler.NODE_POSITIONS, ax=ax, node_size=400)
        nx.draw_networkx_labels(graph, GraphHandler.NODE_POSITIONS, ax=ax, font_size=10)
        nx.draw_networkx_edges(graph, GraphHandler.NODE_POSITIONS, ax=ax, width=2, edge_color=color_map)

        #adaug colorbar
        scalar_map.set_array([])
        fig.colorbar(scalar_map, ax=ax, label = "weights range")

        splited_path = self.path.split("\\")
        print("splitted path: ", splited_path)
        path = ", ".join(splited_path[5:])

        #caut dupa coloana subject valoarea coloanei class
        splitted_strings = path.split(", ")
        subject = splitted_strings[0]
        trial = splitted_strings[2]
        print("subject= ", subject)
        plt.title(path)
        plt.savefig("graph.png")
        plt.close(fig)

