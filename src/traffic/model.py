import random
import warnings

import mesa
import json
import numpy as np
from mesa import DataCollector

from src.traffic.node import Node
from src.traffic.driver import Driver


class TrafficModel(mesa.Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
            self,
            experiment
    ):
        """
        Create a new Traffic model.

        Args:

        """
        drivers_json_file = "input_files/" + experiment + "/drivers.json"
        nodes_json_file = "input_files/" + experiment + "/lights.json"
        traffic_json_file = "input_files/" + experiment + "/traffic.json"
        self.agent_data_file = "output_files/" + experiment + "_AGENT_DATA.csv"

        # Reading traffic_json config file or using the defaults
        with open(traffic_json_file, "r") as read_file:
            data = json.load(read_file)
            self.width = data["width"]
            self.height = data["height"]
            self.n_lanes = data["n_lane"]
            self.torus = data["torus"]
            self.fps = data["fps"]
            self.delay_time = data["delay_time"]

        self.lane_width = self.height / self.n_lanes
        self.height_unit = self.height / (self.n_lanes * 2)  # used to calc where to put an agent (lane-based)
        self.nodes = []
        self.killed_drivers = []
        self.drivers_schedule = mesa.time.BaseScheduler(self)
        self.schedule = self.drivers_schedule # for datacollector to work
        self.lights_schedule = mesa.time.StagedActivation(self)
        self.space = mesa.space.ContinuousSpace(self.width, self.height, self.torus)

        with open(nodes_json_file, "r") as read_file:
            data = json.load(read_file)
            for i, node_json in enumerate(data):
                node = Node(model=self,
                            unique_id=i,
                            pos=(node_json["pos"], 0),
                            durations=node_json["durations"],  # red,yellow,green
                            state=node_json["state"]
                            )
                self.nodes.append(node)
                self.lights_schedule.add(node)
            node = Node(model=self,
                        unique_id=i + 1,
                        pos=(self.width, 0),
                        durations=[0, 0, 1],  # red,yellow,green
                        state="green")

            self.nodes.append(node)
            self.n_nodes = len(self.nodes)
            self.lights_schedule.add(node)

        with open(drivers_json_file, "r") as read_file:
            data = json.load(read_file)
            for driver_json in data:
                driver = self.create_agent(unique_id=driver_json["unique_id"],
                                           # start=driver_json["start"],
                                           # end=driver_json["end"],
                                           start=0,  # all drivers starts at 0, finishes at the last node
                                           end=len(self.nodes) - 1,
                                           lane=driver_json["lane"],
                                           velocity=np.array(driver_json["velocity"]),
                                           max_speed=driver_json["max_speed"],
                                           acceleration=driver_json["acceleration"],
                                           desired_distance=driver_json["desired_distance"],
                                           strategy=driver_json["strategy"])
                self.space.place_agent(driver, driver.pos[0])
                self.drivers_schedule.add(driver)
            self.n_agents = len(self.drivers_schedule.agents)
            self.setup_delays()

        self.data_collector_init()


    # Creates a node with equal distances
    def make_nodes(self):
        self.nodes.append(Node(model=self, unique_id=0, pos=(0, 0)))
        self.lights_schedule.add(self.nodes[-1])
        for i in range(1, self.n_nodes):
            node = Node(model=self, unique_id=i, pos=(i * self.width / (self.n_nodes - 1), 0))
            self.nodes.append(node)
            self.lights_schedule.add(node)

    def make_random_agents(self):
        print("MAKE RANDOM AGENTS NOT IMPLEMENTED")
        return
        """
        Create self.n_agents agents
        """
        for i in range(self.n_agents):
            start_node = 0  # random.randint(0, 3)
            end_node = self.n_nodes - 1  # random.randint(start_node + 1, self.n_nodes - 1)
            current_lane = random.randint(0, self.n_lanes - 1)
            height_unit = self.height / (self.n_lanes * 2)  # used to calc where to put an agent (lane-based)
            pos = [self.nodes[start_node].pos[0], height_unit + current_lane * height_unit * 2]
            driver = Driver(driver_id=i,
                            model=self,
                            pos=pos,
                            car_size=20,
                            velocity=np.array([random.random() * 3, 0]),
                            max_speed=0.01 + (random.random() + 0.2),
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
        if lane > self.n_lanes-1:
            raise Exception("The driver can not be on line",lane)
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
        self.datacollector.collect(self)



    def kill_driver(self, unique_id):
        for d in self.drivers_schedule.agents:
            if d.unique_id is unique_id:
                self.killed_drivers.append(d)
                self.drivers_schedule.remove(self.killed_drivers[-1])
                self.space.remove_agent(self.killed_drivers[-1])
                return

    def setup_delays(self):
        delays_on_lanes = [0] * self.n_lanes
        for driver in self.drivers_schedule.agents:
            driver.delay = delays_on_lanes[driver.current_lane[0]]
            delays_on_lanes[driver.current_lane[0]] += self.delay_time

    def data_collector_save(self):
        # model_data = self.datacollector.get_model_vars_dataframe()
        agent_data = self.datacollector.get_agent_vars_dataframe()
        # model_data.to_csv("output_files/model_data.csv")
        agent_data.to_csv(self.agent_data_file)

    def data_collector_init(self):
        self.datacollector = DataCollector(
            # model_reporters={"agents_count": lambda m: m.n_agents-len(self.killed_drivers)},
            agent_reporters={
                "X": lambda a: a.pos[0],
                "Y":lambda a : a.pos[1],
                "velocity":lambda a: a.velocity,
                "current_lane": lambda a: a.current_lane[0],
            }
        )


