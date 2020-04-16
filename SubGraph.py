import random as rd

class SubGraph:

    def __init__(self, graph, num_contact):
        self.graph=graph
        self.num_vertices=graph.num_vertices
        self.num_edges=0
        self.num_contact=num_contact
        assert(self.num_contact <= graph.num_contact)

        self.adjacency=[]
        for k in range(self.num_vertices):
            self.adjacency.append([])

        self.init_graph(graph)

    def __str__(self):
        return self.adjacency.__str__()

    def __repr__(self):
        return self.__repr__()

    ## Create the sub graph of the graph
    def init_graph(self, graph):
        N=len(graph.adjacency)
        for k in range(N):
            self.adjacency[k]=rd.sample(graph.adjacency[k], self.num_contact) ## Choose num_contact random persons from the possible contact in the main graph