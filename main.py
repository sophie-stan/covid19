from collections import namedtuple
import matplotlib.pyplot as plt
from enum import Enum

from Graph import *
from Person import *
from SubGraph import *
from World import *

rd.seed()

"""GLOBAL PARAMETERS"""
# Graph shape:
# random
# circular
# mixed: When both options circular and random options are set up, a mixed graph is computed.
RANDOM_GRAPH = True
CIRCULAR_GRAPH = True

# Graph size (constant)
POPULATION_SIZE = 1000

# Number of relationships (contacts)
K = 50

# Number of visited persons per day
K_PRIME = 5
assert (K < POPULATION_SIZE)
assert (K_PRIME <= K)

# Disease parameters
DiseaseStruct = namedtuple("DISEASE_PARAMS", "DEATH_RATE SPREAD_RATE DISEASE_DURATION")
DISEASE_PARAMS = DiseaseStruct(DEATH_RATE=0.02, SPREAD_RATE=0.03, DISEASE_DURATION=14)

# Visiting mode: "None", "static", "dynamic".
# "None": K_PRIME = K
# "static": people see the same K_PRIME chosen persons everyday
# "dynamic": people choose K_PRIME different persons to see everyday
VISITING_MODE = "dynamic"

# Confinement mode: "None", "low", "high".
# "None": people see their K relationships everyday
# "low": static mode during DISEASE_DURATION + 1 days
# "high": NO CONTACT AT ALL during DISEASE_DURATION + 1
CONFINEMENT_MODE = "high"
# Containment mode (when 5% of the population is sick the dynamic mode is automatically enable and when it 10% of
# the population the static mode is enable) containment = True """

# Test validity probability
P_TEST = 0.8
NUM_TESTED_PERSONS = POPULATION_SIZE // 10
assert (NUM_TESTED_PERSONS < POPULATION_SIZE)


# Different scenarios
class Scenario(Enum):
    NO_TESTS = 1
    DEAD_CONF = 2
    DEAD_TESTS_CONF = 3
    ALEA_TESTS_CONF = 4
    MASSIVE_TESTS = 5


SCENARIO = Scenario(5)

# Estimated number of available beds for sick persons (In France, it's actually 0,00001%...)
NUM_BEDS = POPULATION_SIZE // 5


""" INITIALIZATION """
# Creation of the population in which the last person is infected on day one
population = []
for ID in range(POPULATION_SIZE - 1):
    population.append(Person(ID, DISEASE_PARAMS.DISEASE_DURATION))
population.append(Person(POPULATION_SIZE - 1, DISEASE_PARAMS.DISEASE_DURATION, state='M', contamination_day=1))

# Creation of the sub_graph, sub_graph and the world
G = Graph(population, circular=CIRCULAR_GRAPH, random=RANDOM_GRAPH, num_relationships=K)
sub_G = SubGraph(relationships_graph=G, num_persons_to_visit=K_PRIME, visiting_mode=VISITING_MODE,
                 confinement_mode=CONFINEMENT_MODE)
world_state = {'S': POPULATION_SIZE - 1, 'R': 0, 'D': 0, 'M': 1, 'C': 0}
w = World(population, DISEASE_PARAMS, P_TEST, NUM_TESTED_PERSONS, SCENARIO, world_state)

X = []
D = []
M = []
S = []
R = []
C = []

""" MAIN LOOP 
Main loop ends when all persons are healthy, dead or healed
Or in case people remain sick, after 12 months
"""
while (world_state['M'] != 0) and (w.elapsed_days < 180):
    world_state = w.update_world(sub_G, population)

    """
    label = ""
    if world_state['M'] > 0.05 * POPULATION_SIZE and VISITING_MODE == "None" and CONFINEMENT_MODE != "None":
        VISITING_MODE = "dynamic"
        label = "Dynamic mode enable"

    if world_state['M'] > 0.1 * POPULATION_SIZE and VISITING_MODE == "dynamic" and CONFINEMENT_MODE != "None":
        VISITING_MODE = "static"
        label = "Static mode enable"

    if len(label) != 0:  # A mode was enabled
        plt.plot([w.elapsed_days, w.elapsed_days], [0, POPULATION_SIZE], label=label)
    """

    X.append(w.elapsed_days)
    D.append(world_state['D'])
    M.append(world_state['M'])
    S.append(world_state['S'])
    R.append(world_state['R'])
    C.append(world_state['C'])

plt.plot(X, D, '.', color='black', label='Dead ({}%)'.
         format(round(100 * w.world_state['D'] / POPULATION_SIZE, 1)))
plt.plot(X, M, '.', color='red', label='Sick')
plt.plot(X, S, '.', color='green', label='Healthy ({}%)'.
         format(round(100 * w.world_state['S'] / POPULATION_SIZE, 1)))
plt.plot(X, R, '.', color='orange', label='Healed ({}%)'.
         format(round(100 * w.world_state['R'] / POPULATION_SIZE, 1)))
if CONFINEMENT_MODE != "None":
    plt.plot(X, C, '.', color='purple', label='Confined')

plt.hlines(max(M), 0, w.elapsed_days, color='red', linestyles='solid')
plt.hlines(NUM_BEDS, 0, w.elapsed_days, color='black', label='Number of beds', linestyles='solid')

plt.xlabel("Days")
plt.ylabel("Number of persons")
# plt.title(" Mixed graph")
plt.title("Modelling of a disease, visiting mode = " + VISITING_MODE
          + ", confinement mode = " + CONFINEMENT_MODE)
plt.legend()
plt.show()

print(world_state)
