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
    """ This class gathers the lists of Persons, a Person will see on D-day.

    A SubGraph is the initial Graph of relationships if there is no visiting mode enabled (K = K_PRIME).
    Any other cases: each Person chooses num_persons_to_visit among the num_relationships they have.
    """

    def __init__(self, relationships_graph, num_persons_to_visit, visiting_mode="None", confinement_mode="None"):
        """
        Parameters
        ----------
        relationships_graph is the network of relationships/contacts between the Persons.
        num_persons_to_visit is the number of Persons a Person will visit daily.
        visiting_mode can be None, dynamic or static (see main.py).
        confinement_mode can be None, low or high (see main.py)
        """

        self.relationships_graph = relationships_graph
        self.population_size = relationships_graph.population_size
        self.num_persons_to_visit = num_persons_to_visit
        self.visiting_mode = visiting_mode
        self.confinement_mode = confinement_mode

        if self.visiting_mode == "None":
            # Visiting everyone everyday
            self.will_visit = copy.copy(relationships_graph.can_visit)
            self.will_be_visited_by = copy.copy(relationships_graph.can_be_visited_by)

        else:
            self.will_visit = [[] for k in range(self.population_size)]
            self.will_be_visited_by = [[] for k in range(self.population_size)]
            self.construct_sub_graph()

    def __str__(self):
        return self.will_visit.__str__()

    def __repr__(self):
        return self.__repr__()

    def construct_sub_graph(self):
        """ Constructs a random SubGraph given the relationships_graph.

        Ignores confined people
        """
        for person in self.relationships_graph.population:
            if person.is_confined():
                continue
            self.construct_list_of_persons_to_visit(person)

    def construct_list_of_persons_to_visit(self, person):
        """ Construct the list of persons, a person will visit,
         After freeing it."""

        # Freeing the old list of persons (if non empty)
        for will_visit_person in self.will_visit[person.ID]:  # children must be aware
            self.will_be_visited_by[will_visit_person.ID].remove(person)
            # and know their visiting father won't visit them
        self.will_visit[person.ID].clear()

        # Random list generated
        candidates_to_visit = my_rd_sample(self.relationships_graph.can_visit[person.ID],
                                           self.num_persons_to_visit)
        # Confined persons should not be visited
        for can_visit_person in candidates_to_visit:
            if not (can_visit_person.is_confined()):
                self.will_visit[person.ID].append(can_visit_person)

        # Update of children's list can_be_visited_by
        for will_visit_person in self.will_visit[person.ID]:  # children must be aware
            self.will_be_visited_by[will_visit_person.ID].append(person)

    def update_sub_graph(self):
        """ The sub_graph needs to be updated only if dynamic mode is enabled. """
        if self.visiting_mode == "dynamic":
            self.will_visit = [[] for k in range(self.population_size)]
            self.will_be_visited_by = [[] for k in range(self.population_size)]
            self.construct_sub_graph()

    def targeted_confinement(self, person):
        """ person becomes confined and is no more allowed to see persons. """
        # High confinement is like being dead almost
        if self.confinement_mode == "high":
            self.remove_vertex(person)
        # Low confinement is a static mode for one person
        elif self.confinement_mode == "low":
            self.remove_vertex(person)
            self.construct_list_of_persons_to_visit(person)

    def targeted_deconfinement(self, person):
        """ person is not confined anymore, she can see other persons again. """
        if self.visiting_mode == "None":
            self.will_visit[person.ID] = copy.copy(self.relationships_graph.will_visit[person.ID])
            self.will_be_visited_by[person.ID] = copy.copy(self.relationships_graph.will_be_visited_by[person.ID])
        else:
            self.construct_list_of_persons_to_visit(person)

    def remove_vertex(self, person):
        """ Removes a vertex from the sub_graph (a person is dead or confined highly) """
        for parent in self.will_be_visited_by[person.ID]:  # search visiting parents
            if person in self.will_visit[parent.ID]:
                (self.will_visit[parent.ID]).remove(person)
        for child in self.will_visit[person.ID]:
            (self.will_be_visited_by[child.ID]).remove(person)

        self.will_visit[person.ID].clear()
        self.will_be_visited_by[person.ID].clear()
