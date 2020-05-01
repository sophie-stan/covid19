import random as rd

class Graph:

    ## persons is a list of persons sorted by person.ID
    def __init__(self, persons, circular=False, random=False, num_contact=None):
        self.num_vertices=len(persons)
        self.num_edges=0
        self.num_contact=num_contact

        self.adjacency=[]
        for k in range(self.num_vertices):
            self.adjacency.append([])

        ## Must be done in first
        if random:
            if num_contact==None or num_contact > self.num_vertices:
                print("Please enter a valid ID of random contact")
            else:
                self.random_graph(persons, num_contact)

        if circular:
            self.circular_graph(persons)



    def __str__(self):
        return self.adjacency.__str__()

    def __repr__(self):
        return self.__repr__()

    ## Create all edges for a circular graph
    def circular_graph(self, persons):
        N=len(persons)
        for k in range(N):
            self.add_edge(persons[k], persons[(k+1)%N])

    ## Create all edges for a random graph
    def random_graph(self, persons, num_contact):
        N=len(persons)
        for k in range(N):
            aux=[]
            for i in range(N):
                if i!=k:
                    aux.append(persons[i])

            j=0
            while j < num_contact:
                random_person=rd.choice(aux)
                self.add_edge(persons[k],random_person)
                aux.remove(random_person)
                j+=1



    ## Add edge between two persons
    def add_edge(self, person_1, person_2):
        if not(person_2 in self.adjacency[person_1.ID]):
            self.num_edges+=1
            self.adjacency[person_1.ID].append(person_2)
            self.adjacency[person_2.ID].append(person_1)







G = Graph
