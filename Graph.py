import random as rd


class Graph:
    """ This class allows to construct a sub_graph implemented by an will_visit list.

    Vertices are Person.
    Each Person has a group of a certain amounts of relationships.
    A sub_graph can be random, circular, or mixed.
    """

    def __init__(self, population, num_relationships, circular=False, random=False):
        """
        Parameters
        ----------
        population is the list of all the Persons sorted out following their ID.
        num_relationships is the number of Persons, a Person is related to.
        circular is an option which allows to set up a circular sub_graph.
        random is an option which allows to set up a random sub_graph.
        """
        self.population = population
        self.population_size = len(population)
        self.num_relationships = num_relationships

        self.can_visit = [[] for k in range(self.population_size)]
        self.can_be_visited_by = [[] for k in range(self.population_size)]
        if circular:
            self.construct_circular_graph()
        if random:
            self.construct_random_graph()

    def __str__(self):
        return self.can_visit.__str__()

    def __repr__(self):
        return self.__repr__()

    def add_edge(self, parent, child):
        """ Adds an edge from parent to child only if it doesn't exist yet. """
        if not (child in self.can_visit[parent.ID]):
            self.can_visit[parent.ID].append(child)
            self.can_be_visited_by[child.ID].append(parent)

    def construct_circular_graph(self):
        """ Constructs a circular sub_graph. """
        pop_size = self.population_size
        for k in range(pop_size):
            self.add_edge(self.population[k], self.population[(k + 1) % pop_size])
            self.add_edge(self.population[k], self.population[(k - 1) % pop_size])

    def construct_random_graph(self):
        """ Constructs a random sub_graph """
        pop_size = self.population_size
        for i in range(pop_size):
            potential_relationships_i = []
            for j in range(pop_size):
                if i != j:
                    potential_relationships_i.append(self.population[j])
            relationships_i = rd.sample(potential_relationships_i, self.num_relationships)
            # num_relationships is obviously less than len(potential_relationships_i) = n - 1
            for person in relationships_i:
                self.add_edge(self.population[i], person)

    def remove_vertex(self, dead_person):
        """ Removes a vertex from the sub_graph (a person is dead) """
        for person in self.can_be_visited_by[dead_person.ID]:  # search parents
            (self.can_visit[person.ID]).remove(dead_person)  # remove the dead child
        for person in self.can_visit[dead_person.ID]:  # search children
            (self.can_be_visited_by[person.ID]).remove(dead_person)  # remove the dead parent

        self.can_visit[dead_person.ID].clear()  # remove all children
        self.can_be_visited_by[dead_person.ID].clear()  # remove all parents
