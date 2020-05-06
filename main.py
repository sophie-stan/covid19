# sos.chdir("/home/celaglae/Documents/ALGO_GRAPH_projet_COVID19/sub_graph")

from collections import namedtuple
import matplotlib.pyplot as plt

from Graph import *
from Person import *
from SubGraph import *
from World import *

rd.seed()

"""GLOBAL PARAMETERS"""
# Graph shape:
# random
# circular
# mixed (random circular union)
RANDOM_GRAPH = True
CIRCULAR_GRAPH = True

# Graph size (constant)
POPULATION_SIZE = 1000

# Number of relationships (contacts)
K = 10

# Number of visited persons per day
K_PRIME = 5
assert (K < POPULATION_SIZE)
assert (K_PRIME <= K)

# Visiting mode: "None", "static", "dynamic".
# "None": K_PRIME = K
# "static": people see the same K_PRIME chosen persons everyday
# "dynamic": people choose K_PRIME different persons to see everyday
VISITING_MODE = "dynamic"

# Confinement mode: "None", "low", "high".
#  "None": people see their K relationships everyday
# "low": static mode during DISEASE_TIME + 1 days
# "high": NO CONTACT AT ALL during DISEASE_TIME + 1
CONFINEMENT_MODE = "high"
# Containment mode (when 5% of the population is sick the dynamic mode is automatically enable and when it 10% of
# the population the static mode is enable) containment = True """

# Test validity probability
P_TEST = 0.7
NUM_TESTED_PERSONS = POPULATION_SIZE // 3
assert(NUM_TESTED_PERSONS < POPULATION_SIZE)

# Disease parameters
DiseaseStruct = namedtuple("DISEASE_PARAMS", "DEATH_RATE SPREAD_RATE DISEASE_TIME")
DISEASE_PARAMS = DiseaseStruct(DEATH_RATE=0.2, SPREAD_RATE=0.03, DISEASE_TIME=14)

""" INITIALIZATION """
# Creation of the population in which the last person is infected on day one
population = []
for ID in range(POPULATION_SIZE - 1):
    population.append(Person(ID, DISEASE_PARAMS.DISEASE_TIME))
population.append(Person(POPULATION_SIZE - 1, DISEASE_PARAMS.DISEASE_TIME, state='M', contamination_day=1))

# Creation of the sub_graph, sub_graph and the world
G = Graph(population, circular=CIRCULAR_GRAPH, random=RANDOM_GRAPH, num_relationships=K)
sub_G = SubGraph(relationships_graph=G, num_persons_to_visit=K_PRIME, visiting_mode=VISITING_MODE,
                 confinement_mode=CONFINEMENT_MODE)
world_state = {'S': POPULATION_SIZE - 1, 'R': 0, 'D': 0, 'M': 1, 'C': 0}
w = World(population, DISEASE_PARAMS, P_TEST, NUM_TESTED_PERSONS, world_state)

X = []
D = []
M = []
S = []
R = []
C = []

""" MAIN LOOP 
Main loop ends when all persons are healthy, dead or cured
Or in case people remain sick, after 12 months
"""
while (world_state['M'] != 0) and (w.elapsed_days < 360):
    world_state = w.update_world(sub_G, population)

    '''
    if world_state['M'] > 0.05 * POPULATION_SIZE and not (dynamic) and not (static) and containment:
        dynamic = True
        plt.plot([k, k], [0, POPULATION_SIZE], label="Dynamic mode enable")

    if world_state['M'] > 0.1 * POPULATION_SIZE and dynamic and not (static) and containment:
        dynamic = False
        static = True
        plt.plot([k, k], [0, POPULATION_SIZE], label="Static mode enable")
    if dynamic:
        sub_G = SubGraph(G, k_prime)
    '''

    X.append(w.elapsed_days)
    D.append(world_state['D'])
    M.append(world_state['M'])
    S.append(world_state['S'])
    R.append(world_state['R'])
    C.append(world_state['C'])

plt.plot(X, D, color='black', label='Dead')
plt.plot(X, M, color='red', label='Sick')
plt.plot(X, S, color='green', label='Healthy')
plt.plot(X, R, color='orange', label='Reminiscent')
plt.plot(X, C, color='purple', label='Confined')

plt.xlabel("Days")
plt.ylabel("ID of people")
plt.title("Modelling of a disease, visiting mode = " + VISITING_MODE + ", confinement mode = " + CONFINEMENT_MODE)
plt.legend()
plt.show()

print(world_state)
