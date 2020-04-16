import os
os.chdir("/home/celaglae/Documents/ALGO_GRAPH_projet_COVID19/graph")

from World import *
from Person import *
from Graph import *
from SubGraph import *

import random as rd
import matplotlib.pyplot as plt
rd.seed()


## Parameters of the disease
death_rate=0.03
spread_rate=0.01
disease_time=14

## Size of the population :
population=1000

## Creation of the population
p=[]
for k in range(population-1):
    p.append(Person(k))
p.append(Person(population-1, state='M', disease_time=disease_time)) ## one sick person

## Creation of the graph and the world
k=50
## Partie Clément : ###
#g=Graph(p, random=True, num_contact=k)
## Partie Sophie : ###
#g=Graph(p, circular=True)
g=Graph(p,circular=True, random=True, num_contact=k)
k_prime=5
subg=SubGraph(g,k_prime)

## Low confinement
low_confinement=False

## High confinement
high_confinement=True



w=World(death_rate, spread_rate, disease_time, low_confinement, high_confinement)

## Number of days
days=6*30

## Static mode
static=False
## Dynamic mode
dynamic=False
## Containment mode (when 5% of the population is sick the dynamic mode is automatically enable and when it 10% of the population the static mode is enable)
containment=True



###############
## Main loop ##
###############

X=[]
D=[]
M=[]
S=[]
R=[]
k=1
state={'S':population-1,'R':0,'D':0,'M':1}
#for k in range(days):
while state['M']!=0:
    if dynamic or static:
        state=w.update_all(subg, p)
    else:
        state=w.update_all(g,p)
    if state['M'] > 0.05*population and not(dynamic) and not(static) and containment:
        dynamic=True
        plt.plot([k,k],[0,population],label="Dynamic mode enable")
    if state['M'] > 0.1*population and dynamic and not(static) and containment:
        dynamic=False
        static=True
        plt.plot([k,k],[0,population],label="Static mode enable")
    if dynamic:
        subg=SubGraph(g,k_prime)
    X.append(k)
    D.append(state['D'])
    M.append(state['M'])
    S.append(state['S'])
    R.append(state['R'])
    k+=1

plt.plot(X,D,'.',label='Death')
plt.plot(X,M,'.',label='Sick')
plt.plot(X,S,'.',label='Safe')
plt.plot(X,R,'.',label='Immunity')

plt.xlabel("Days")
plt.ylabel("Number of people")
plt.title("Modelisation of the Covid-19")
plt.legend()
plt.show()

print(state)


