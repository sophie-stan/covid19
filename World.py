import random as rd


class World:

    def __init__(self, disease_params, world_state, elapsed_days=1):
        """
        Parameters
        ----------
        disease_params is a structure (Death_rate, Spread_rate, disease_time).
        world_state is a dictionary in which person states are counted.
        elapsed_days (the counter of elapsed days since the beginning of the experiment).
        """
        self.death_rate = disease_params.DEATH_RATE
        self.spread_rate = disease_params.SPREAD_RATE
        self.disease_time = disease_params.DISEASE_TIME
        self.world_state = world_state
        self.elapsed_days = elapsed_days

    # World state updates
    def m_to_d(self):
        self.world_state['M'] -= 1
        self.world_state['D'] += 1

    def m_to_r(self):
        self.world_state['M'] -= 1
        self.world_state['R'] += 1

    def s_to_m(self):
        self.world_state['S'] -= 1
        self.world_state['M'] += 1

    def none_to_c(self):
        self.world_state['C'] += 1

    def c_to_none(self):
        self.world_state['C'] -= 1

    # Persons update (state, confinement, dayly_met_persons)
    # along with the graphs
    def update_world(self, sub_graph, population):

        # ! address of persons in sub_graph = address of persons in population !
        for person in population:
            # Healthy people get sick because of sick people
            for person_to_see in sub_graph.will_visit[person.ID]:

                if person.state == 'S' and person_to_see.state == 'M':
                    if rd.random() < self.spread_rate:
                        person.state = 'M'
                        person.contamination_day = self.elapsed_days
                        self.s_to_m()
                if person.state == 'M' and person_to_see.state == 'S':
                    if rd.random() < self.spread_rate:
                        person_to_see.state = 'M'
                        person_to_see.contamination_day = self.elapsed_days
                        self.s_to_m()

            person.add_daily_met_persons(sub_graph.will_visit[person.ID], sub_graph.will_be_visited_by[person.ID])

            # Sick persons may die after r days with a death_rate probability
            if person.state == 'M' and (self.elapsed_days - person.contamination_day == self.disease_time):
                if rd.random() < self.death_rate:
                    person.state = 'D'
                    self.m_to_d()
                    sub_graph.remove_vertex(person)  # sub_graph of meetings
                    sub_graph.relationships_graph.remove_vertex(person)  # sub_graph of contacts

                    """ Scenario 2
                    Persons in relation with dead person get confined
                    Aim: find those persons in the daily_met_persons of person
                    """
                    persons_to_confine = []
                    for day in person.daily_met_persons:
                        for met_person in day:
                            persons_to_confine.append(met_person)
                    # Removes duplicates
                    tmp = set(persons_to_confine)
                    persons_to_confine = list(tmp)
                    for person_to_confine in persons_to_confine:
                        self.none_to_c()
                        person_to_confine.confinement_day = self.elapsed_days
                        sub_graph.confined_person(person_to_confine)

                else:
                    person.state = 'R'
                    self.m_to_r()

            # Confined persons can stop confinement after r + 1 days of confinement
            if person.is_confined():
                if (self.elapsed_days - person.confinement_day) == (self.disease_time + 1):
                    person.confinement_day = - 1  # no more confined
                    self.c_to_none()  # World
                    sub_graph.confined_person(person)  # SubGraph

        sub_graph.update_subgraph()
        self.elapsed_days += 1
        return self.world_state
