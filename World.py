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
            if not (self.high_confinement and persons[k].is_confined):
                for j in range(len(graph.adjacency[k])): ## for each nodes connected to persons[k]
                    persons[k].update(graph.adjacency[k][j], self.death_rate, self.spread_rate, self.disease_time)
            if persons[k].state=='M' and persons[k].remaining_disease_time!=0:
                persons[k].remaining_disease_time-=1
            state[persons[k].state]+=1
            if persons[k].is_confined:
                state['C']+=1
            persons[k].update_visited(self.disease_time)

        return state
