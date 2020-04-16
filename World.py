class World:

    def __init__(self, death_rate, spread_rate, disease_time):
        self.death_rate=death_rate
        self.spread_rate=spread_rate
        self.disease_time=disease_time

    ## Update all person of 'persons' which must be in the graph
    ## Return a dictionnary with the number of each state
    def update_all(self, graph, persons):
        state={'S':0,'R':0,'D':0,'M':0}
        for k in range(len(persons)):
            for j in range(len(graph.adjacency[k])): ## for each nodes connected to persons[k]
                persons[k].update(graph.adjacency[k][j], self.death_rate, self.spread_rate, self.disease_time)
            if persons[k].state=='M' and persons[k].remaining_disease_time!=0:
                persons[k].remaining_disease_time-=1
            state[persons[k].state]+=1
            persons[k].update_visited(disease_time)
            
        return state
