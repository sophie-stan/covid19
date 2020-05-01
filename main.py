import os
from collections import namedtuple

## sos.chdir("/home/celaglae/Documents/ALGO_GRAPH_projet_COVID19/graph")

from World import *
from Person import *
from Graph import *
from SubGraph import *

import random as rd
import matplotlib.pyplot as plt
rd.seed()

# Graph parameters
GRAPH_RANDOM = False
GRAPH_CIRCULAR = True
K = 50
K_PRIME = 5
# Enum: static, dynamic
MODE = "static"

# disease parameters
DISEASE_PARAMS = Disease_Struct(DEATH_RATE = 0.03, SPREAD_RATE = 0.01, DISEASE_TIME = 14)

## Size of the POPULATION_SIZE
POPULATION_SIZE = 100

## Creation of the population
polulation = []
for k in range(POPULATION_SIZE - 1):
    population.append(Person(k))

population.append(Person(POPULATION_SIZE - 1, state = 'M', contamination_day = 1)) ## one sick person

## Creation of the graph and the world

## Partie Clement : ###
#g=Graph(p, random=True, num_contact=k)
## Partie Sophie : ###
#g=Graph(p, circular=True)
g = Graph(p, circular = GRAPH_CIRCULAR, random = GRAPH_RANDOM, num_contact = K)
subg = SubGraph(g, K_PRIME)

################################################################################

## Low confinement
low_confinement = False

## High confinement
high_confinement = True

## Containment mode (when 5% of the population is sick the dynamic mode is automatically enable and when it 10% of the population the static mode is enable)
containment = True

X = []
D = []
M = []
S = []
R = []
C = []

################################################################################

###############
## Main loop ##
###############

w = World(MODE, DISEASE_PARAMS, low_confinement, high_confinement)

world_state = {'S':population - 1, 'R':0, 'D':0, 'M':1, 'C':0}

# Main loop ends when all persons are healthy, dead or cured
while world_state['M'] != 0:

    if dynamic or static:
        world_state = w.update(subg, p)
    else:
        world_state = w.update(g, p)

    # Study of the virus outbreak limited to 6m
    if w.elapsed_days > (180):
        break

    if world_state['M'] > 0.05 * POPULATION_SIZE and not(dynamic) and not(static) and containment:
        dynamic = True
        plt.plot([k, k], [0, POPULATION_SIZE], label = "Dynamic mode enable")

    if world_state['M'] > 0.1*POPULATION_SIZE and dynamic and not(static) and containment:
        dynamic=False
        static=True
        plt.plot([k,k],[0,POPULATION_SIZE],label="Static mode enable")
    if dynamic:
        subg = SubGraph(g,k_prime)
    X.append(k)
    D.append(world_state['D'])
    M.append(world_state['M'])
    S.append(world_state['S'])
    R.append(world_state['R'])
    C.append(world_state['C'])
    elapsed_days += 1

plt.plot(X,D,'.',label='Death')
plt.plot(X,M,'.',label='Sick')
plt.plot(X,S,'.',label='Safe')
plt.plot(X,R,'.',label='Immunity')
if low_confinement or high_confinement:
    plt.plot(X,C,'.',label="Confined")

plt.xlabel("Days")
plt.ylabel("ID of people")
plt.title("Modelisation of the Covid-19")
plt.legend()
plt.show()

print(world_state)
