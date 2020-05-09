class Person:

    def __init__(self, ID, disease_duration, state='S', contamination_day=None, confinement_day=None):
        """
        Parameters
        ----------
        ID is a constant number which identifies a Person.
        disease_duration is the duration of the disease.
        state is a character: 'S' for Sain, 'M' for Malade, 'R' for Rémission, 'D' for Décédé
        contamination_day is a constant number, the date of contamination
        confinement_day is a constant number, the date of confinement
        """
        self.ID = ID
        self.state = state
        self.contamination_day = contamination_day
        self.confinement_day = confinement_day
        self.disease_duration = disease_duration
        self.daily_met_persons = []

    def __str__(self):
        # return "Person ID {} / state {}".format(self.ID,self.state)
        return str(self.ID)

    def __repr__(self):
        return self.__str__()

    def is_confined(self):
        return not ((self.confinement_day is None) and not(self.confinement_day == -1))

    def add_daily_met_persons(self, visited, visited_by):
        """ Adds daily persons met to queue """
        met_persons = visited + visited_by
        self.daily_met_persons.append(met_persons)
        if len(self.daily_met_persons) > self.disease_duration:
            self.daily_met_persons.pop(0)

    def construct_candidates_to_confinement(self):
        """ When self dies, construct the list of candidates to confinement. """
        candidates_to_confinement = []
        for day in self.daily_met_persons:
            candidates_to_confinement += day
        # Removes duplicates
        tmp = set(candidates_to_confinement)
        candidates_to_confinement = list(tmp)
        return candidates_to_confinement
