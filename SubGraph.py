import copy
import random as rd


def my_rd_sample(L, n):
    """ If all friends of a person are dead, nb_friends < num_relationships
    --> rd.sample returns an error """
    if n <= len(L):
        return rd.sample(L, n)
    else:
        return L


class SubGraph:
    """ This class gathers the lists of Persons, a Person will see.

    A SubGraph is the Graph of relationships if there is no visiting mode.
    Any other cases: each Person chooses num_persons_to_visit among the num_relationships they have
    Warnings: Person cannot choose more person to visit than they actually know (see circular)
    """

    def __init__(self, relationships_graph, num_persons_to_visit, visiting_mode=None, confinement_mode=None):
        """
        Parameters
        ----------
        relationships_graph is the network of relationships between the Persons
        num_persons_to_visit is the number of Persons a Person will visit daily
        visiting_mode says whether or not num_persons_to_visit will be usefull
        """

        self.relationships_graph = relationships_graph
        self.population_size = relationships_graph.population_size
        self.num_persons_to_visit = num_persons_to_visit
        self.visiting_mode = visiting_mode

        # A person can't visit more persons than she is actually related to
        assert (self.num_persons_to_visit <= relationships_graph.num_relationships)

        if self.visiting_mode is None:
            # Visiting everyone everyday
            self.adjacency = copy.copy(relationships_graph.adjacency)

        else:
            self.adjacency = [[] for k in range(self.population_size)]
            self.construct_subgraph()

    def __str__(self):
        return self.adjacency.__str__()

    def __repr__(self):
        return self.__repr__()

    def construct_subgraph(self):
        """ Constructs a random Subgraph given the relationships_graph.

        Ignore confined people
        """
        for person in self.relationships_graph.population:
            if person.is_confined():
                continue
            self.adjacency[person.ID] = my_rd_sample(self.relationships_graph.adjacency[person.ID],
                                                     self.num_persons_to_visit)
            for person_can_see in self.adjacency[person.ID]:
                # if person_can_see is confined,
                # he/she does not have the right to be seen by anyone else
                if person_can_see.is_confined():
                    self.adjacency[person.ID].remove(person_can_see)

    def update_subgraph(self):
        """ The graph needs to be updated only if dynamic mode"""
        if self.visiting_mode == "dynamic":
            self.construct_subgraph()

    def confined_person(self, person):
        """ person becomes confined and is not more allowed to see some persons. """
        # High confinement is like being dead almost
        if person.confinement_mode == "high":
            self.remove_vertex(person)
        # Low confinement is a static mode for one person
        elif person.confinement_mode == "low":
            self.adjacency[person.ID] = my_rd_sample(self.relationships_graph.adjacency[person.ID],
                                                     self.num_persons_to_visit)

    def unconfined_person(self, person):
        """ person is not confined anymore, she can see other persons again. """
        if self.visiting_mode is None:
            self.adjacency[person.ID] = copy.copy(self.relationships_graph.adjacency[person.ID])
        else:
            self.adjacency[person.ID] = my_rd_sample(self.relationships_graph.adjacency[person.ID],
                                                     self.num_persons_to_visit)

    def remove_vertex(self, dead_person):
        """ Removes a vertex from the graph (a person is dead or confined highly) """
        for p in self.relationships_graph.adjacency[dead_person.ID]:
            if dead_person in self.adjacency[p.ID]:
                (self.adjacency[p.ID]).remove(dead_person)
        self.adjacency[dead_person.ID].clear()
