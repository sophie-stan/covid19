##################################
## Modelisation of the Covid-19 ##
##################################

This project is a modelisation of the disease of the Covid-19.
It is done in Python.


###########
## Class ##
###########

This project is using several Class :


## World (World.py)
A world is the environnment in which the modelisation take place. The world is the class which knows the parameter of the environnment.
For example : the death and spread rate of the disease, if the low/high containment is enabled...

## Person (Person.py)
A person represents an element of the population. 

## Graph (Graph.py)
A graph represents the contact between all the persons

## SubGraph (SubGraph.py)
It is a part of the Graph


##########
## Main ##  
##########

In the file main.py you can find the main loop of the modelisation. You can also change all the parameter of the disease.
When it is launched a graph is plotted which represents the evolution of the disease between the day 0 and the end of the disease.