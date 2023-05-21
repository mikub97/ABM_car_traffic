"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""
import random

import mesa

from src.traffic.driver import Driver


class Node():
    def __init__(
            self,
            nodeID,
            position):

        self.nodeID = nodeID,
        self.position = position
        self.state = "RED"

    def change_state(self):
        pass



class TrafficModel(mesa.Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
        self,
        width=1000,
        height=500,
        n_lines=3,
        n_nodes=10,
        n_agents=10,
    ):
        """
        Create a new Traffic model.

        Args:

        """
        self.width = width
        self.height = height
        self.n_agents = n_agents
        self.n_lines = n_lines
        self.n_nodes = n_nodes
        self.schedule = mesa.time.RandomActivation(self)
        self.space = mesa.space.ContinuousSpace(width, height, False)
        self.make_nodes()
        self.make_agents()
        self.running = True


    # Creates a node with equal distances
    def make_nodes(self):
        self.nodes = []
        self.nodes.append(Node(0,0))
        for i in range(1,self.n_nodes):
            node = Node(i,i*self.width/(self.n_nodes-1))
            self.nodes.append(node)

    def make_agents(self):
        """
        Create self.n_agents agents
        """
        self.drivers = []
        for i in range(self.n_agents):
            start_node = random.randint(0,self.n_nodes-2)
            end_node = random.randint(start_node+1,self.n_nodes-1)
            current_lane = random.randint(0, self.n_lines-1)
            height_unit = self.height/(self.n_lines*2) # used to calc where to put an agent (lane-based)
            pos = [self.nodes[start_node].position,current_lane*height_unit]

            driver = Driver(driver_id=i,
                            model=self,
                            pos=pos,
                            max_speed=2,
                            acceleration=10,
                            current_lane=current_lane,
                            start_node=start_node,
                            end_node=end_node)
            self.space.place_agent(driver,pos)
            self.schedule.add(driver)
            self.drivers.append(driver)

    def step(self):
        self.schedule.step()
