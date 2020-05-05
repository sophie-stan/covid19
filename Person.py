class Person:

    def __init__(self, ID, disease_params, state='S', contamination_day=None, confinement_day=None):
        """
        Parameters
        ----------
        ID is a constant number which identifies a Person
        state is a character: S for Sain, M for Malade, R for Rémission, D for Décédé
        contamination_day is a constant number, the date of contamination
        confinement_mode says whether or not a Person is confined and how
        confinement_day is a constant number, the date of confinement
        """
        self.ID = ID
        self.state = state
        self.contamination_day = contamination_day
        self.confinement_day = confinement_day
        self.disease_time = disease_params.DISEASE_TIME
        self.daily_met_persons = []

    def __str__(self):
        # return "Person ID {} / state {}".format(self.ID,self.state)
        return str(self.ID)

    def __repr__(self):
        return self.__str__()

    def is_confined(self):
        return not ((self.confinement_day is None) or (self.confinement_day == -1))

    def add_daily_met_persons(self, visited, visited_by):
        """ Adds daily persons met to queue """
        met_persons = visited + visited_by
        self.daily_met_persons.append(met_persons)
        if len(self.daily_met_persons) > self.disease_time:
            self.daily_met_persons.pop(0)


''' 
def confine_all(self):
    for i in range(disease_time):
        self.visited[i][0].is_confined = True
        
    '''
