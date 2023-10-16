import networkx as nx

class GraphMetrics:
    """
    Clasa se ocupa calculul tuturor metricilor de graf, necesare contruirii instantelor de antrenare.
    """
    def __init__(self, graph):
        self.graph = graph

    def average_cost(self):
        total_cost = 0
        edges_counter = 0
        for u, v, data in self.graph.edges(data = True):
            total_cost += data['weight']
            edges_counter += 1
        if edges_counter > 0:
            average_cost = total_cost / edges_counter
        else:
            average_cost = 0

        return  average_cost

    def betweenness_centrality(self):
        # returneaza un dictionar cu nodurile drept chei si bc drept valori
        bc = nx.betweenness_centrality(self.graph, weight = 'weight')
        return bc
    def degree_centrality(self):
        nodes_centralities = {}
        for node in self.graph.nodes():
            degree_centrality = 0
            for edge in self.graph.edges(node, data=True):
                degree_centrality += edge[2]['weight']
            nodes_centralities[node] = degree_centrality

        return nodes_centralities
    def average_path_length(self):
        sum_distances = 0
        for node in self.graph.nodes():
            #returnez un dicționar cu lungimile drumurilor cele mai scurte de la nodul de pornire la fiecare alt nod
            lengths_dict = nx.single_source_dijkstra_path_length(self.graph, node, weight='weight')
            sum_distances += sum(lengths_dict.values())
        nodes_counter = self.graph.number_of_nodes()
        average = sum_distances / (nodes_counter * (nodes_counter - 1))

        return average

    def clustering_coefficient_using_nx(self):
        cc = nx.average_clustering(self.graph, weight=True)
        return cc

    def global_efficiency(self):
        sum_distances = 0
        for node in self.graph.nodes():
            #returnez un dicționar cu lungimile drumurilor cele mai scurte de la nodul de pornire la fiecare alt nod
            lengths_dict = nx.single_source_dijkstra_path_length(self.graph, node, weight='weight')
            for val in lengths_dict.values():
                if val != 0:
                    sum_distances += (1 / val)
        nodes_counter = self.graph.number_of_nodes()
        average = sum_distances / (nodes_counter * (nodes_counter - 1))

        return average






