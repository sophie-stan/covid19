# sos.chdir("/home/celaglae/Documents/ALGO_GRAPH_projet_COVID19/graph")

from collections import namedtuple

import matplotlib.pyplot as plt

from Graph import *
from Person import *
from SubGraph import *
from World import *

rd.seed()

# GLOBAL PARAMETERS #####
# Graph parameters
GRAPH_RANDOM = True
GRAPH_CIRCULAR = False
K = 50  # Number of relationships
K_PRIME = 5  # Number of visited persons per day

# Visiting mode: None, static, dynamic
VISITING_MODE = "static"

# confinement mode: None, low, high
CONFINEMENT_MODE = "low"
'''## Containment mode (when 5% of the population is sick the dynamic mode is automatically enable and when it 10% of 
the population the static mode is enable) containment = True '''
# Disease parameters
DiseaseStruct = namedtuple("DISEASE_PARAMS", "DEATH_RATE SPREAD_RATE DISEASE_TIME")
DISEASE_PARAMS = DiseaseStruct(DEATH_RATE=0.5, SPREAD_RATE=0.09, DISEASE_TIME=14)

# Initial size of the population (not constant)
POPULATION_SIZE = 300

# INITIALIZATION #####


# Creation of the population in which the last person is infected on day one
population = []
for k in range(POPULATION_SIZE - 1):
    population.append(Person(k))
population.append(Person(POPULATION_SIZE - 1, state='M', contamination_day=1))

# Creation of the graph and the world

G = Graph(population, circular=GRAPH_CIRCULAR, random=GRAPH_RANDOM, num_relationships=K)
sub_G = SubGraph(relationships_graph=G, visiting_mode=VISITING_MODE,num_persons_to_visit=K_PRIME)  # does not change if static mode

##########
X = []
D = []
M = []
S = []
R = []
C = []
##########


# MAIN LOOP #####



world_state = {'S': POPULATION_SIZE - 1, 'R': 0, 'D': 0, 'M': 1, 'C': 0}
w = World(DISEASE_PARAMS, world_state)

# Main loop ends when all persons are healthy, dead or cured
while world_state['M'] != 0:

    if VISITING_MODE == "static":
        world_state = w.update_world(sub_G, population)
    elif VISITING_MODE == "dynamic":
        sub_G = SubGraph(G, num_persons_to_visit=K_PRIME)
        world_state = w.update_world(sub_G, population)
    else:  # no visiting mode set up
        world_state = w.update_world(G, population)

    # Study of the virus outbreak limited to 6m
    if w.elapsed_days > 180:
        break

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
    # C.append(world_state['C'])

plt.plot(X, D, '.', label='Dead')
plt.plot(X, M, '.', label='Sick')
plt.plot(X, S, '.', label='Healthy')
plt.plot(X, R, '.', label='Reminiscent')
# if low_confinement or high_confinement:
#   plt.plot(X, C, '.', label="Confined")

plt.xlabel("Days")
plt.ylabel("ID of people")
plt.title("Modelisation of the Covid-19")
plt.legend()
plt.show()

print(world_state)
