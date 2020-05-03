import random as rd


class World:

    def __init__(self, disease_params, world_state, elapsed_days=1):
        """
        Parameters
        ----------
        disease_params is a structure (Death_rate, Spread_rate, disease_time)
        world_state is a dictionary in which person states are counted
        elapsed_days (the counter of elapsed days since the beginning of the experiment)
        """
        self.death_rate = disease_params.DEATH_RATE
        self.spread_rate = disease_params.SPREAD_RATE
        self.disease_time = disease_params.DISEASE_TIME
        self.world_state = world_state
        self.elapsed_days = elapsed_days

    def sick_to_dead(self):
        self.world_state['D'] += 1
        self.world_state['M'] -= 1

    def sick_to_reminiscent(self):
        self.world_state['R'] += 1
        self.world_state['M'] -= 1

    def healthy_to_sick(self):
        self.world_state['M'] += 1
        self.world_state['S'] -= 1

    def confined_person(self):
        self.world_state['C'] +=1

    def unconfined_person(self):
        self.world_state['C'] -=1

    def update_world(self, graph, population):

        # Update of the population state
        # ! address of persons in graph = address of persons in population !
        for person in population:
            # Healthy people get sick because of sick people
            for person_to_see in graph.adjacency[person.ID]:
                if person.state == 'S' and person_to_see.state == 'M':
                    if rd.random() < self.spread_rate:
                        person.state = 'M'
                        person.contamination_day = self.elapsed_days
                        self.healthy_to_sick()
                if person.state == 'M' and person_to_see.state == 'S':
                    if rd.random() < self.spread_rate:
                        person_to_see.state = 'M'
                        person_to_see.contamination_day = self.elapsed_days
                        self.healthy_to_sick()

            # Sick persons may die after r days with a death_rate probability
            if person.state == 'M' and (self.elapsed_days - person.contamination_day == self.disease_time):
                if rd.random() < self.death_rate:
                    person.state = 'D'
                    self.sick_to_dead()
                    graph.remove_vertex(person)  # graph of meetings
                    graph.relationships_graph.remove_vertex(person)  # graph of contacts
                else:
                    person.state = 'R'
                    self.sick_to_reminiscent()

            # Confined persons can stop confinement after r + 1 days of confinement
            if person.is_confined():
                if (self.elapsed_days - person.confinement_day) == (self.disease_time + 1):
                    person.confinement_day = -1
                    person.confinement_mode = None
                    self.unconfined_person()
                    graph.unconfined_person(person)

        graph.update_subgraph()
        self.elapsed_days += 1
        return self.world_state

