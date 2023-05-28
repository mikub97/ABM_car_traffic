"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""
import random

import mesa
import numpy as np
import warnings
from src.traffic.driver import Driver

import json
import numpy as np

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
        traffic_json_file = None,

        drivers_json_file = None
    ):
        """
        Create a new Traffic model.

        Args:

        """
# Reading traffic_json config file or using the defaults
        if traffic_json_file is None:
            self.width = 1000
            self.height = 500
            self.n_agents = 10
            self.n_lanes = 3
            self.n_nodes = 10
            self.torus = True
            self.separation_k = 0.5
            self.fps=60
        else:
            with open(traffic_json_file, "r") as read_file:
                data = json.load(read_file)
                self.width = data["width"]
                self.height = data["height"]
                self.n_agents = data["n_agent"]
                self.n_lanes = data["n_lane"]
                self.n_nodes = data["n_node"]
                self.torus = data["torus"]
                self.separation_k = data["separation_k"]
                self.fps = data["fps"]



        self.lane_width = self.height / self.n_lanes
        self.height_unit = self.height / (self.n_lanes * 2)  # used to calc where to put an agent (lane-based)

        self.schedule = mesa.time.BaseScheduler(self) # check also RandomActivation and others TODO
        self.space = mesa.space.ContinuousSpace(self.width, self.height,  self.torus)
        self.make_nodes()
        self.drivers = []

# Creating random agents or reading them from a json file
        if drivers_json_file is None:
            self.make_random_agents()
        else:
            with open(drivers_json_file, "r") as read_file:
                data = json.load(read_file)
                for driver_json in data:
                    driver = self.create_agent(unique_id=driver_json["unique_id"],
                                               start=driver_json["start"],
                                               end=driver_json["end"],
                                               lane=driver_json["lane"],
                                               velocity=np.array(driver_json["velocity"]),
                                               max_speed=driver_json["max_speed"],
                                               acceleration=driver_json["acceleration"],
                                               desired_distance=driver_json["desired_distance"],
                                               strategy = driver_json["strategy"])
                    self.drivers.append(driver)
                    self.space.place_agent(driver, driver.pos[0])
                    self.schedule.add(driver)
                if self.n_agents is not len(self.drivers):
                    warnings.warn(f"\nThe number of agents in the '{drivers_json_file}' differs from"
                                  f"the one in the config file,\n"
                          f"Setting model.n_agents to {len(self.drivers)}(the value from '{drivers_json_file}') ")
                    self.n_agents = len(self.drivers)


    # Creates a node with equal distances
    def make_nodes(self):
        self.nodes = []
        self.nodes_distances =  [0]
        self.nodes.append(Node(0,0))
        for i in range(1,self.n_nodes):
            node = Node(i,i*self.width/(self.n_nodes-1))
            self.nodes.append(node)
            self.nodes_distances.append(i*self.width/(self.n_nodes-1))

    def make_random_agents(self):
        """
        Create self.n_agents agents
        """
        for i in range(self.n_agents):
            start_node = random.randint(0,3)
            end_node = random.randint(start_node+1,self.n_nodes-1)
            current_lane = random.randint(0, self.n_lanes - 1)
            height_unit = self.height/(self.n_lanes * 2) # used to calc where to put an agent (lane-based)
            pos = [self.nodes[start_node].position,height_unit+current_lane*height_unit*2]
            driver = Driver(driver_id=i,
                            model=self,
                            pos=pos,
                            car_size=20,
                            velocity= np.array([random.random()*3,0]),
                            max_speed=0.2,
                            acceleration=0.0001,
                            desired_distance=100,
                            current_lane=current_lane,
                            start_node=start_node,
                            end_node=end_node,
                            strategy=None)
            self.space.place_agent(driver,pos)
            self.schedule.add(driver)
            self.drivers.append(driver)

    def create_agent(self, unique_id, start, end, lane, velocity, max_speed, acceleration, desired_distance,strategy):
        pos = [self.nodes[start].position, self.height_unit + lane * self.height_unit * 2]
        return Driver(driver_id=unique_id,
                        model=self,
                        pos=pos,
                        car_size=20,
                        velocity=velocity,
                        max_speed=max_speed,
                        acceleration=acceleration,
                        desired_distance=desired_distance,
                        current_lane=lane,
                        start_node=start,
                        end_node=end,
                        strategy=strategy)



    def step(self):
        self.schedule.step()
