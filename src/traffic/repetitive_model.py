from random import random

import pandas as pd

from src.traffic.analysis_utils import collect_data
from src.traffic.driver import Driver
from src.traffic.model import TrafficModel

x_sessions = [
    {
        "n_agents": 25,
        "max_speed_avg": v,
        "max_speed_dev": 0.4,

        "desired_distance_avg": 30,
        "desired_distance_dev": 0,

        "acceleration_avg": 1.5,
        "acceleration_dev": 0.3,
        "n_lanes": 3

    }
    for v in [2]]


class RepetitiveTrafficModel(TrafficModel):

    def __init__(self, experiment):
        super().__init__(experiment,
                         measure_settings={
                                "x_start": 500,
                                "x_end": 600,
                                "measure_point_x": 500,
                                "accepted_dist_delta": 10,
                                "window_size": 100,
                                "rolling_average_density_running_step": 5 ,
                                "rolling_average_flow_running_step": 100
                        },
                         read_agents=False)
        self.measures_files = "output_files/" + experiment + "/measures_files.csv"
        self.finished = False
        self.sessions = x_sessions
        self.agentID_counter = 0
        self.session_counter = 0
        self.next_session()

    def step(self):
        if not self.finished:
            super().step()
            if len(self.schedule.agents) == 0:
                self.add_time_measures()
                self.next_session()

    def next_session(self):

        if self.session_counter > len(self.sessions) - 1:
            self.finished = True
            return
        session = self.sessions[self.session_counter]
        self.session_counter += 1
        self.n_lanes = session["n_lanes"]
        super().make_random_agents(session["n_agents"], session["max_speed_avg"],
                                   session["max_speed_dev"], session["desired_distance_avg"],
                                   session["desired_distance_dev"], session["acceleration_avg"],
                                   session["acceleration_dev"], starting_id=self.agentID_counter)
        self.agentID_counter += session["n_agents"]

    def data_collector_save(self):
        agent_data = self.datacollector.get_agent_vars_dataframe().reset_index()
        agent_data["Velocity"] = agent_data["Velocity"].apply(lambda x: float(x[0]))
        agent_data["Velocity"] = agent_data["Velocity"].astype(float)
        measures_data = collect_data(agent_data=agent_data,
                                     sessions=self.sessions,
                                     measure_times=self.time_measures,
                                     measure_settings=self.measure_settings)
        agent_data.to_csv(self.agent_data_file)
        measures_data.to_csv(self.measures_files)
        print(measures_data.head())
