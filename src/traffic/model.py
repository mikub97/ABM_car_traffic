"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""
import random

import mesa
import warnings

from src.traffic.node import Node
from src.traffic.driver import Driver

import json
import numpy as np


class TrafficModel(mesa.Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
            self,
            traffic_json_file=None,
            nodes_json_file=None,
            drivers_json_file=None
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
            self.fps = 60
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

        self.drivers_schedule = mesa.time.BaseScheduler(self)
        self.lights_schedule = mesa.time.StagedActivation(self)
        self.space = mesa.space.ContinuousSpace(self.width, self.height, self.torus)
        self.killed_drivers = []
        self.nodes = []

        if nodes_json_file is None:
            self.make_nodes()
        else:
            with open(nodes_json_file, "r") as read_file:
                data = json.load(read_file)
                for i,node_json in enumerate(data):
                    node = Node(model=self,
                                unique_id=i,
                                pos=(node_json["pos"],0),
                                durations=node_json["durations"],  # red,yellow,green
                                state=node_json["state"]
                                )
                    self.nodes.append(node)
                    self.lights_schedule.add(node)

                node = Node(model=self,
                            unique_id=i+1,
                            pos=(self.width, 0),
                            durations=[0, 0, 1],  # red,yellow,green
                            state="green"
                            )
                self.nodes.append(node)
                if self.n_nodes != len(self.nodes):
                    warnings.warn(f"\nThe number of nodes in the '{nodes_json_file}' differs from"
                                  f"the one in the {traffic_json_file},\n"
                                  f"Setting model.n_agents to {len(self.nodes)}(the value from '{nodes_json_file}') ")
                    self.n_nodes = len(self.nodes)
                self.lights_schedule.add(node)

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
                                               strategy=driver_json["strategy"])
                    self.space.place_agent(driver, driver.pos)
                    self.drivers_schedule.add(driver)
                if self.n_agents is not len(self.drivers_schedule.agents):
                    warnings.warn(f"\nThe number of agents in the '{drivers_json_file}' differs from"
                                  f"the one in the config file,\n"
                                  f"Setting model.n_agents to {len(self.drivers)}(the value from '{drivers_json_file}') ")
                    self.n_agents = len(self.drivers)

                    for d in self.drivers:
                        print(d)

    # Creates a node with equal distances
    def make_nodes(self):
        self.nodes.append(Node(model=self, unique_id=0, pos=(0,0)))
        self.lights_schedule.add(self.nodes[-1])
        for i in range(1, self.n_nodes):
            node = Node(model=self, unique_id=i, pos=(i * self.width / (self.n_nodes - 1),0))
            self.nodes.append(node)
            self.lights_schedule.add(node)

    def make_random_agents(self):
        """
        Create self.n_agents agents
        """
        for i in range(self.n_agents):
            start_node = random.randint(0, 3)
            end_node = random.randint(start_node + 1, self.n_nodes - 1)
            current_lane = random.randint(0, self.n_lanes - 1)
            height_unit = self.height / (self.n_lanes * 2)  # used to calc where to put an agent (lane-based)
            pos = [self.nodes[start_node].pos[0], height_unit + current_lane * height_unit * 2]
            driver = Driver(driver_id=i,
                            model=self,
                            pos=pos,
                            car_size=20,
                            velocity=np.array([random.random() * 3, 0]),
                            max_speed=0.01+(random.random()+0.2),
                            acceleration=0.001,
                            desired_distance=40,
                            current_lane=current_lane,
                            start_node=start_node,
                            end_node=end_node,
                            strategy=None)
            self.space.place_agent(driver, pos)
            self.drivers_schedule.add(driver)

    def create_agent(self, unique_id, start, end, lane, velocity, max_speed, acceleration, desired_distance, strategy):
        pos = (self.nodes[start].pos[0], self.height_unit + lane * self.height_unit * 2)
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
        self.drivers_schedule.step()
        self.lights_schedule.step()

    def kill_driver(self, unique_id):
        for d in self.drivers_schedule.agents:
            if d.unique_id is unique_id:
                self.killed_drivers.append(d)
                self.drivers_schedule.remove(self.killed_drivers[-1])
                self.space.remove_agent(self.killed_drivers[-1])
                return
