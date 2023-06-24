from random import random

from src.traffic.driver import Driver
from src.traffic.model import TrafficModel


class RepetitiveTrafficModel(TrafficModel):

    def __init__(self, experiment):
        super().__init__(experiment, read_agents=False)

        self.finished = False
        self.sessions = [
            {
                "n_agents": 10,
                "max_speed_avg": 1.5,
                "max_speed_dev": 0.3,

                "desired_distance_avg": 30,
                "desired_distance_dev": 3,

                "acceleration_avg": 1.5,
                "acceleration_dev": 0,
                "n_lanes":3
            },
            {
                "n_agents": 20,
                "max_speed_avg": 1,
                "max_speed_dev": 0.7,

                "desired_distance_avg": 30,
                "desired_distance_dev": 0,

                "acceleration_avg": 1.5,
                "acceleration_dev": 0.3,
                "n_lanes":2
            },
        ]
        self.session_times = []
        self.agentID_counter = 0
        self.session_counter = 0
        self.next_session()

    def step(self):
        if not self.finished:
            super().step()
            if len(self.schedule.agents) == 0:
                self.next_session()

    def next_session(self):
        if len(self.session_times)>0:
            self.session_times[-1]["end"]=self.time
        if self.session_counter > len(self.sessions)-1:
            self.finished = True
            print(self.session_times)
            return
        session = self.sessions[self.session_counter]
        self.session_times.append({"session_counter":self.session_counter,
                                   "start": self.time})
        self.session_counter += 1
        self.n_lanes = session["n_lanes"]
        super().make_random_agents(session["n_agents"], session["max_speed_avg"],
                                   session["max_speed_dev"], session["desired_distance_avg"],
                                   session["desired_distance_dev"], session["acceleration_avg"],
                                   session["acceleration_dev"], starting_id=self.agentID_counter)
        self.agentID_counter += session["n_agents"]
