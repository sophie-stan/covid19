class World:

    def __init__(self, death_rate, spread_rate, disease_time, low_confinement, high_confinement):
        self.death_rate=death_rate
        self.spread_rate=spread_rate
        self.disease_time=disease_time
        self.low_confinement=low_confinement
        self.high_confinement=high_confinement

    ## Update all person of 'persons' which must be in the graph
    ## Return a dictionnary with the number of each state
    def update_all(self, graph, persons):
        state={'S':0,'R':0,'D':0,'M':0,'C':0}
        for k in range(len(persons)):
            if (self.low_confinement and persons[k].is_confined):
                for i in range(len(persons[k].visited[persons[k].visited_cursor])): ## for each person visited yesterday
                    persons[k].update_in_contact(persons[k].visited[persons[k].visited_cursor][i], self.death_rate, self.spread_rate, self.disease_time)
            elif not(self.high_confinement and persons[k].is_confined):
                for j in range(len(graph.adjacency[k])): ## for each nodes connected to persons[k]
                    persons[k].update_in_contact(graph.adjacency[k][j], self.death_rate, self.spread_rate, self.disease_time)

            persons[k].update_end_of_day(self.disease_time, self.death_rate)

            state[persons[k].state]+=1
            if persons[k].is_confined:
                state['C']+=1
            

        return state
