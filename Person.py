import random as rd

class Person:

    def __init__(self, number, disease_time, state='S', debug = False, debug_visited = False):
        self.number=number
        self.state=state
        self.is_confined=False
        self.visited=[]
        self.debug=debug ## if the debug mode is enabled informations are printed
        self.debug_visited=debug_visited ## to print informations about the list visited
        self.day=1 ## a variable used for the debug mode
        for k in range(disease_time):
            self.visited.append([])
        self.visited_cursor=0 ## the current day
        self.remaining_confinment_time=0
        if state=='M':
            self.remaining_disease_time=disease_time
        else:
            self.remaining_disease_time=0

        if self.debug:
            print("DAY 1")
            print("I was born with the state {},  I am number {}".format(self.state, self.number))

    def __str__(self):
        ##return "Person number {} / state {}".format(self.number,self.state)
        return str(self.number)

    def __repr__(self):
        return self.__str__()

    ## When self is in contact with a person
    def update_in_contact(self, person, death_rate, spread_rate, disease_time):
        if self.debug_visited:
            print("I am in contact with {}".format(person.number))
        if not(self.is_confined):
            if self.debug_visited:
                print("I add {} to my list of visited at the place {}".format(person.number, self.visited_cursor))
            self.visited[self.visited_cursor].append(person) ## add to the list 'visited' the person in contact with self
        if self.state=='S' and person.state=='M' and rd.random() < spread_rate: ## the person will be sick
            self.state='M'
            self.remaining_disease_time=disease_time
            if self.debug:
                print("I become sick for {} day(s)".format(disease_time))



    ## Update the list 'visited'
    def update_end_of_day(self, disease_time, death_rate, p_test):
        if self.is_confined:
            if self.remaining_confinment_time == 0:
                if self.debug:
                    print("My confinment is finished")
                self.is_confined = False
            else:
                if self.debug:
                    print("My confinment will end in {} day(s)".format(self.remaining_confinment_time))
                self.remaining_confinment_time -= 1
        else:
            self.visited_cursor = (self.visited_cursor + 1)%disease_time
            self.visited[self.visited_cursor]=[]


        if self.debug and self.day != 1:
            print("\n DAY {}".format(self.day))
        self.day+=1

        if self.state=='M':
            if self.remaining_disease_time==0: ## end of the disease
                if rd.random() < death_rate: ## death
                    if self.debug:
                        print("I am dead :'(")
                    self.state='D'
                    self.test_all_visited(disease_time, p_test)
                else: ## immunity
                    if self.debug:
                        print("I become immune")
                    self.state='R'
            else:
                if self.debug:
                    print("My disease will end in {} day(s)".format(self.remaining_disease_time))
                self.remaining_disease_time -= 1

    ## Order to the person of the list visited to be confined
    def confine_all(self, disease_time):
        for i in range(len(self.visited)):
            for j in range(len(self.visited[i])):
                if not(self.visited[i][j].is_confined):
                    self.visited[i][j].confine(disease_time)
                    if self.debug:
                        print("I confine {} for {} days".format(self.visited[i][j].number, self.visited[i][j].remaining_confinment_time))


    ## Order to the person of the list visited to be tested
    def test_all_visited(self, disease_time, p_test):
        for i in range(len(self.visited)):
            for j in range(len(self.visited[i])):
                if not(self.visited[i][j].is_confined):
                    self.visited[i][j].test_virus(disease_time, p_test)

    ## Test the person if he was in contact with the deceased and confine him if he is positive to the virus
    def test_virus(self, disease_time, p_test):
        if self.state == 'M' and self.is_confined == False and rd.random() < p_test: ## the person will be tested positive to the virus and so will be confined
            self.is_confined = True
            self.remaining_confinment_time = disease_time + 1
            if self.debug:
                print("I confine myself for {} day(s)".format(self.remaining_confinment_time))

    ## Confine himself
    def confine(self, disease_time):
        self.is_confined = True
        self.remaining_confinment_time = disease_time + 1
        if self.debug:
            print("I confine myself for {} day(s)".format(self.remaining_confinment_time))


