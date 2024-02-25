# ABM_CPMII

# Traffic Simulation Project

## Introduction

As cognitive science students, we are developing an interest in understanding the behaviors of complex systems. Complex systems, by their nature, are intricate networks of interactions and relationships, and this complexity often gives rise to fascinating phenomena that are not easily predictable by looking at individual elements of the system separately.

One of the most common examples of a complex system is traffic flow. In our daily lives, we experience frustration associated with being stuck in traffic jams, the complicated choreography of merging and lane-changing cars, sudden congestion seemingly appearing out of nowhere, and equally sudden disappearances of traffic jams. These phenomena serve as an excellent illustration of complexity, emergence, and self-organization - concepts that are at the heart of both complex systems and cognitive science.

Traffic congestion also has significant practical implications. It is estimated to cost billions of dollars annually in lost productivity, wasted fuel, and increased air pollution. Moreover, traffic jams can have serious consequences for emergency services, potentially delaying response times, which can lead to loss of life. Therefore, understanding, and ultimately mitigating traffic congestion issues, is not just a fascinating academic challenge but also a problem of crucial practical importance.

The concept of agent-based modeling struck us as an incredibly promising method for understanding complex systems such as traffic congestion. During our studies, we came across the idea of modeling traffic as a system of interacting agents, each following relatively simple rules. This way of thinking harmonizes with our cognitive science direction, as it reflects how individual cognitive processes can lead to complex behaviors.

## Model and Algorithm

In our project, we utilized a microscopic car-following model, which is one of the primary approaches in modeling traffic congestion. This model allows for simulating traffic flow at the level of individual vehicles, providing detailed insight into the dynamics of traffic on the road.

The key assumption of the microscopic car-following model is that each vehicle, or "agent" in our model, makes decisions about its speed and position on the road based on the behavior of the vehicle in front of it. This approach reflects reality, where drivers adjust their behavior on the road in response to traffic conditions, including the speed and position of other vehicles.

Our implementation of the model consists of two main components: agents representing cars and an environment representing the road. Each agent in our model has its own state, which includes its current speed, position on the road, and other relevant parameters. At each simulation step, agents update their state based on simple rules that reflect car-following principles.

The environment of our model is a road with multiple lanes of traffic. Cars can move forward, change lanes, and come to a stop, and their decisions depend on traffic conditions such as the speed of other cars, the distance between cars, and traffic regulations.

The algorithm we applied to our simulation is based on iterative updating of the states of all agents. At each simulation step, each agent analyzes its current state, the state of the road ahead, and makes a decision about its future speed and position. These decisions are then applied to update the agent's state.

Overall, our model and algorithm enable detailed simulation of traffic congestion, taking into account the dynamics of individual vehicles and their interactions. This precision makes our approach particularly useful for investigating issues such as traffic jams, traffic flow "waves," and potential strategies for optimizing traffic flow.


## GENERAL REMARKS 
- just in case, be mindful about giving nodes/agents id - unique_ids should have values from 0 to n,
this is the index of the element in the nodes/agents lists respectively
- When using lights.json file as a config for traffic lights, remember, that you don't need to add the final node (the end of the road), its added automatically
- the cars (the drivers) are in points in the space. Their graphical expression is not yet well adjusted (boundaries of a car)

The structure of the project:
- in the directory json_data/ you can find two files 'drivers.json' and 'traffic.json'(where configuration of the simulation is stored)
- in src/model.py there is a TrafficModel class, which inherits from mesa.Model class
- in src/driver.py there is a Driver class, which inherits from mesa.Agent class
- in src/gui.py there is Gui class, that uses pygame module to display a real-time simulation of the model
- in main.py, you initialise a TrafficModel class and feed it to the Gui class to run the simulation
- in boid_flockers/ directory there is an example of mesa ABM, found on internet - ignore it.

## To run the simulation:
1. Setup the config json files json_data/drivers.json and json_data/traffic.json
2. Run gui.py file


Behaviour of each agent is implemented in the Driver class. In the step() method, I implement a simple 'Microscopic car-following models'
If a car is the first in the lane, it accelerates until it reaches the max_speed value
If a car is following another car, it uses the formula:
<img src="velocity_formula.png" >

## When it comes to measures:

In a traffic flow model that incorporates the possibility of lane changing, the phases of traffic can still be understood and measured based on certain indicators and variables. Here are some commonly used metrics and techniques for identifying and characterizing the phases of traffic flow in such models:

**Density**: Density refers to the number of vehicles per unit length of road. In free flow, the density is relatively low, while in congested flow, the density is high. By monitoring the density at different locations and times, you can identify the transition points between the phases.

**Speed**: Speed is another important parameter for analyzing traffic flow. In free flow, vehicles typically travel at higher speeds, while in congested flow, the speeds are significantly reduced. By measuring the speed of vehicles and analyzing the speed distributions, you can identify the different phases of traffic.

**Flow Rate**: Flow rate represents the number of vehicles passing a particular point on the road per unit time. In free flow, the flow rate tends to be high and consistent, while in congested flow, the flow rate decreases due to reduced vehicle movement. Monitoring and analyzing the flow rate can help identify the transitions between phases.

**Traffic Waves**: Traffic waves are patterns of acceleration and deceleration that propagate backward through traffic. These waves can be observed when traffic transitions between free flow and congested flow. By studying the propagation of traffic waves and their characteristics, you can gain insights into the phase changes occurring in the traffic flow.

**Lane Changing Behavior**: Lane changing is an essential aspect of traffic flow with multiple lanes. By analyzing lane changing patterns, such as frequency, distance traveled before lane change, and time taken for lane changes, you can gain a better understanding of the synchronization and congestion phenomena associated with phase changes.

In a traffic flow model with the possibility of lane changing, these metrics can be measured and analyzed to determine the current phase of traffic flow at specific locations and times. By examining how these variables change over time and space, researchers can identify the transition points between different phases and study the dynamics of traffic flow in more detail.

It's worth noting that various modeling techniques, such as cellular automata models, agent-based models, or fluid-dynamic-based models, can be used to simulate traffic flow with lane changing and analyze the phases based on the mentioned indicators. These models take into account factors such as vehicle interactions, lane-changing rules, and road network characteristics to provide insights into the complex behavior of traffic flow
