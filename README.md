# Pandemic
 An agent-based model of a disease, sadly inspired by recent events :/
 
 This repository contains a model based on mesa, an agent based modeling package for python.
 
 # Further development
 
 The model is currently in an early stage of development. The goal is to add more realistic behaviour (incubation times, movement, vulnerability, etc.) and certain policy levers (social distancing, quarantining known infections). The final model should allow users to gain a better understanding of epidemic spread and policy implications. 
 
 ## Current model
 
 Agents are people moving around in a grid.
 
 The model starts with a population of agents N, of whom a subset is already infected. 
 
 Infected agents are able to infect agents in neighboring cells with a pre-specified infection rate probability.
 
 After some time has passed, infected agents either become immune to the disease or die. Dead agents no longer move on the grid.
 
 ## Next steps
 
 * Add incubation times
 * Add quarantining known infected agents
 * Add social distancing 
 * Add infections from outside sources
 
 # Running an interactive server
 
 To run the model in an interactive environment, either run the file run.py or clone the repository and enter mesa runserver in a command line routed to the folder.
 
 
 
 
