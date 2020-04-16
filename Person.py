import random as rd

class Person:

    def __init__(self, number, state='S', disease_time=0):
        self.number=number
        self.state=state
        self.is_confined=False
        self.visited=[]
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
        self.visited.append([person, 0]) ## add to the list 'visited' the person in contact with self
        if self.state=='S' and person.state=='M' and rd.random() < spread_rate: ## the person wil be sick
            self.state='M'
            self.remaining_disease_time=disease_time

        elif self.state=='M':
            if self.remaining_disease_time==0: ## end of the disease
                if rd.random() < death_rate: ## death
                    self.state='D'
                    self.confine_all()
                else: ## immunity
                    self.state='R'

    ## Update the list 'visited'
    def update_visited(self, disease_time):
        for i in range(len(self.visited)):
            if self.visited[k][1] > disease_time :
                self.visited.pop(k)
            else :
                self.visited[k][1]+=1


    def confine_all(self):
        for i in range(len(self.visited)):
            self.visited[i][0].is_confined = True




