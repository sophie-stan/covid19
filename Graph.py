import random as rd


class Graph:
    """ This class allows to construct a graph implemented by an adjacency list.

    Vertices are Person.
    Each Person has a group of a certain amounts of relationships.
    A graph can be random, circular, or mixed.
    """

    def __init__(self, population, num_relationships, circular=False, random=False):
        """
        Parameters
        ----------
        population is the list of all the Persons sorted out following their ID
        num_relationships is the number of Persons, a Person is related to
        circular is an option which allows to set up a circular graph
        random is an option which allows to set up a random graph
        """
        self.population = population
        self.population_size = len(population)
        self.num_relationships = num_relationships

        self.adjacency = [[] for k in range(self.population_size)]
        if circular:
            self.construct_circular_graph()
            self.num_relationships = 2
        if random:
            self.construct_random_graph()

    def __str__(self):
        return self.adjacency.__str__()

    def __repr__(self):
        return self.__repr__()


    def add_edge(self, person_1, person_2):
        """ Adds an edge from person_1 to person_2. """
        self.adjacency[person_1.ID].append(person_2)

    def construct_circular_graph(self):
        """ Constructs a circular graph. """
        pop_size = self.population_size
        for k in range(pop_size):
            self.add_edge(self.population[k], self.population[(k + 1) % pop_size])
            self.add_edge(self.population[k], self.population[(k - 1) % pop_size])

    def construct_random_graph(self):
        """ Constructs a random graph """
        pop_size = self.population_size
        for i in range(pop_size):
            relationships_i = []
            potential_relationships_i = []
            for j in range(pop_size):
                if i != j:
                    potential_relationships_i.append(self.population[j])
            relationships_i = rd.sample(potential_relationships_i, self.num_relationships)
            # Chooses self.num_relationships random persons
            # among the potential relationships that i can have
            for person in relationships_i:
                self.add_edge(self.population[i], person)

    def remove_vertex(self, dead_person):
        """ Removes a vertex from the graph (a person is dead) """
        for p in self.adjacency[dead_person.ID]:
            if dead_person in self.adjacency[p.ID]:
                (self.adjacency[p.ID]).remove(dead_person)
        self.adjacency[dead_person.ID].clear()
