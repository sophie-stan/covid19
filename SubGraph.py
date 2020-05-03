import random as rd


class SubGraph:

    def __init__(self, relationships_graph, num_persons_to_visit, visiting_mode=None):
        """
        Parameters
        ----------
        graph is the network of relationships between the persons belonging to the population
        num_persons_to_visit is the number of Persons a Person will visit daily
        """

        self.relationships_graph = relationships_graph
        self.population_size = relationships_graph.population_size
        self.num_persons_to_visit = num_persons_to_visit
        self.visiting_mode = visiting_mode

        # A person can't visit more persons than she is actually related to
        assert (self.num_persons_to_visit <= relationships_graph.num_relationships)

        if self.visiting_mode is None:
            # Visiting everyone everyday
            self.adjacency = relationships_graph.adjacency

        else:
            self.adjacency = [[] for k in range(self.population_size)]
            size_pop = relationships_graph.population_size
            for ID in range(size_pop):
                self.adjacency[ID] = rd.sample(relationships_graph.adjacency[ID], self.num_persons_to_visit)
                # Chooses self.num_persons_to_visit random persons
                # among the potential contacts that i can have (graph.adjacency[i])

    def __str__(self):
        return self.adjacency.__str__()
    def __repr__(self):
        return self.__repr__()

    # Removes a vertex from the graph (a person is dead)
    def remove_vertex(self, dead_person):
        for p in self.relationships_graph.adjacency[dead_person.ID]:
            if dead_person in self.adjacency[p.ID]:
                (self.adjacency[p.ID]).remove(dead_person)
        self.adjacency[dead_person.ID].clear()
