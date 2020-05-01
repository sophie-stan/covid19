import random as rd

class World:

    def __init__(self, mode, k_prime, diseas_params, low_confinement, high_confinement, elapsed_days = 1):
        self.mode = mode
        self.diseas_params = diseas_params
        self.elapsed_days = elapsed_days
        self.low_confinement = low_confinement
        self.high_confinement = high_confinement
        self.k_prime = k_prime

    ## Update all person of 'persons' which must be in the graph
    ## Return a dictionnary with the ID of each state
    def update(self, graph, persons):
        state = {'S':0, 'R':0, 'D':0, 'M':0, 'C':0}

        for i in range(len(persons)):

            # Sick persons may die after r days with a death_rate probability
            if persons[i].state == 'M' and (self.elapsed_days - persons[i].contamination_day == self.disease_time):
                if rd.random() < death_rate:
                    persons[i].state = 'D'
                else:
                    persons[i].state = 'R'

            # Reminisent and dead persons cannot contaminate others or get sick themselves
            if persons[i].state == 'R' or persons[i].state == 'D':
                continue

            if self.mode == "static":
                nb_persons_to_visit = self.k_prime - len(persons[i].current_day_visited)

                if nb_persons_to_visit == 0:
                    continue

                can_visit_persons = []
                for j in range(len(graph.adjacency[i])):
                    if graph.adjacency[i][j].state == 'D' or (len(persons[j].current_day_visited) >= self.k_prime):
                        continue
                    can_visit_persons.append(i)

                if len(can_visit_persons) == 0:
                    continue

                nb_persons_to_visit = min(nb_persons_to_visit, len(can_visit_persons))

                for j in range(nb_persons_to_visit):
                    person_to_visit = rd.randint(0, len(can_visit_persons))

                    if persons[i].state == 'M' and persons[can_visit_persons[nb_person_to_visit]].[person_to_visit].state == 'M' and rd.random() < spread_rate: ## the person wil be sick
                        self.state = 'M'

                    can_visit_persons.remove(person_to_visit)

                for j in range(len(graph.adjacency[i])):

            elif self.mode == "dynamic":

            else:
                print ("Unsupported world mode: " + self.mode)


            if not (self.high_confinement and persons[k].is_confined):
                for j in range(len(graph.adjacency[k])): ## for each nodes connected to persons[k]
                    persons[k].update(graph.adjacency[k][j], self.death_rate, self.spread_rate, self.disease_time)
            if persons[k].state=='M' and persons[k].remaining_disease_time!=0:
                persons[k].remaining_disease_time-=1
            state[persons[k].state]+=1
            if persons[k].is_confined:
                state['C']+=1
            persons[k].update_visited(self.disease_time)

        self.elapsed_days += 1
        return state
