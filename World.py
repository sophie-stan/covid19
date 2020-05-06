import copy
import random as rd

from SubGraph import my_rd_sample


class World:

    def __init__(self, population, disease_params, p_test, num_tested_persons, world_state, elapsed_days=1):
        """
        Parameters
        ----------
        disease_time is a structure (Death_rate, Spread_rate, disease_time).
        world_state is a dictionary in which person states are counted.
        elapsed_days (the counter of elapsed days since the beginning of the experiment).
        """
        self.alive_persons = copy.copy(population)

        self.death_rate = disease_params.DEATH_RATE
        self.spread_rate = disease_params.SPREAD_RATE
        self.disease_time = disease_params.DISEASE_TIME

        self.p_test = p_test
        self.num_tested_persons = num_tested_persons
        self.world_state = world_state
        self.elapsed_days = elapsed_days

    # World state updates
    def sick_to_dead(self, dead_person):
        self.world_state['M'] -= 1
        self.world_state['D'] += 1
        self.alive_persons.remove(dead_person)

    def sick_to_reminiscent(self):
        self.world_state['M'] -= 1
        self.world_state['R'] += 1

    def healthy_to_sick(self):
        self.world_state['S'] -= 1
        self.world_state['M'] += 1

    def none_to_confined(self):
        self.world_state['C'] += 1

    def confined_to_none(self):
        self.world_state['C'] -= 1

    def scenario_2(self, sub_graph, dead_person):
        """ Scenario 2:
        Persons in contact with the dead person get confined.
        """
        candidates_to_confinement = []
        for day in dead_person.daily_met_persons:
            for met_person in day:
                candidates_to_confinement.append(met_person)
        # Removes duplicates
        tmp = set(candidates_to_confinement)
        candidates_to_confinement = list(tmp)

        persons_to_confine = []
        for candidate_to_confinement in candidates_to_confinement:
            if candidate_to_confinement.is_confined():
                candidate_to_confinement.confinement_day = self.elapsed_days  # Person
            else:
                persons_to_confine.append(candidate_to_confinement)

        for person_to_confine in persons_to_confine:
            self.none_to_confined()  # World
            person_to_confine.confinement_day = self.elapsed_days  # Person
            sub_graph.confined_person(person_to_confine)  # SubGraph

    def scenario_3(self, sub_graph, dead_person):
        """ Scenario 3:
        Persons in contact with the dead person get confined
        Only if they're tested positive
        """
        candidates_to_confinement = []
        for day in dead_person.daily_met_persons:
            for met_person in day:
                candidates_to_confinement.append(met_person)
        # Removes duplicates
        tmp = set(candidates_to_confinement)
        candidates_to_confinement = list(tmp)

        persons_to_confine = []
        for candidate_to_confinement in candidates_to_confinement:
            if (candidate_to_confinement.state == 'M') and (rd.random() < self.p_test):
                if candidate_to_confinement.is_confined():
                    candidate_to_confinement.confinement_day = self.elapsed_days  # Person
                else:
                    persons_to_confine.append(candidate_to_confinement)

        for person_to_confine in persons_to_confine:
            self.none_to_confined()  # World
            person_to_confine.confinement_day = self.elapsed_days  # Person
            sub_graph.confined_person(person_to_confine)  # SubGraph

    def scenario_4(self, sub_graph):
        """ Aim: find certain amount of persons in the pop
         not dead and not confined to test and then confine
         """
        candidates_to_confinement = my_rd_sample(self.alive_persons, self.num_tested_persons)
        persons_to_confine = []
        for candidate_to_confinement in candidates_to_confinement:
            if (candidate_to_confinement.state == 'M') and (rd.random() < self.p_test):
                if candidate_to_confinement.is_confined():
                    candidate_to_confinement.confinement_day = self.elapsed_days  # Person
                else:
                    persons_to_confine.append(candidate_to_confinement)

        for person_to_confine in persons_to_confine:
            self.none_to_confined()  # World
            person_to_confine.confinement_day = self.elapsed_days  # Person
            sub_graph.confined_person(person_to_confine)  # SubGraph

    def scenario_5(self, sub_graph, person):
        self.scenario_3(sub_graph, person)
        self.scenario_4()

    # Persons update (state, confinement, daily_met_persons)
    # along with the graphs and the world
    def update_world(self, sub_graph, population):

        # ! address of persons in sub_graph = address of persons in population !
        for person in population:
            # Healthy people get sick because of sick people
            for person_to_see in sub_graph.will_visit[person.ID]:

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

            person.add_daily_met_persons(sub_graph.will_visit[person.ID], sub_graph.will_be_visited_by[person.ID])

            # Sick persons may die after r days with a death_rate probability
            if person.state == 'M' and (self.elapsed_days - person.contamination_day == self.disease_time):
                if rd.random() < self.death_rate:
                    person.state = 'D'
                    self.sick_to_dead(person)  # World
                    sub_graph.remove_vertex(person)  # SubGraph of meetings
                    sub_graph.relationships_graph.remove_vertex(person)  # Graph of contacts

                    if sub_graph.confinement_mode != "None":
                        # self.scenario_2(sub_graph, person)
                        self.scenario_3(sub_graph, person)
                        self.scenario_4(sub_graph)

                else:
                    person.state = 'R'
                    self.sick_to_reminiscent()

            # Confined persons can stop confinement after r + 1 days of confinement
            if person.is_confined():
                if (self.elapsed_days - person.confinement_day) == (self.disease_time + 1):
                    person.confinement_day = - 1  # Person
                    self.confined_to_none()  # World
                    sub_graph.confined_person(person)  # SubGraph

        sub_graph.update_subgraph()
        self.elapsed_days += 1
        return self.world_state
