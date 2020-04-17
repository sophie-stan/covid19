import random as rd

class Person:

    def __init__(self, number, disease_time, state='S'):
        self.number=number
        self.state=state
        self.is_confined=False
        self.visited=[]
        for k in range(disease_time):
            self.visited.append([])
        self.visited_cursor=0 ## the current day
        self.remaining_confinment_time=0
        if state=='M':
            self.remaining_disease_time=disease_time
        else:
            self.remaining_disease_time=0

    def __str__(self):
        ##return "Person number {} / state {}".format(self.number,self.state)
        return str(self.number)

    def __repr__(self):
        return self.__str__()

    ## When self is in contact with a person
    def update(self, person, death_rate, spread_rate, disease_time):
        if not(self.is_confined):
            self.visited[self.visited_cursor].append(person) ## add to the list 'visited' the person in contact with self
        if self.state=='S' and person.state=='M' and rd.random() < spread_rate: ## the person wil be sick
            self.state='M'
            self.remaining_disease_time=disease_time

        elif self.state=='M':
            if self.remaining_disease_time==0: ## end of the disease
                if rd.random() < death_rate: ## death
                    self.state='D'
                    self.confine_all(disease_time)
                else: ## immunity
                    self.state='R'

    ## Update the list 'visited'
    def update_visited(self, disease_time):
        if self.is_confined:
            if self.remaining_disease_time == 0:
                self.is_confined = False
            else:
                self.remaining_disease_time -= 1
        else:
            self.visited_cursor = (self.visited_cursor + 1)%disease_time


    def confine_all(self, disease_time):
        for i in range(len(self.visited)):
            for j in range(len(self.visited[i])):
                self.visited[i][j].is_confined = True
                self.visited[i][j].remaining_confinment_time = disease_time + 1




