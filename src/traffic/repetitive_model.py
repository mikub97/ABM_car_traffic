from random import random

import pandas as pd

from src.traffic.analysis_utils import collect_data
from src.traffic.driver import Driver
from src.traffic.model import TrafficModel
x_sessions =  [{
                "n_agents": 25,
                "max_speed_avg": v,
                "max_speed_dev": 0.4,

                "desired_distance_avg": 30,
                "desired_distance_dev": 0,

                "acceleration_avg": 1.5,
                "acceleration_dev": 0.3,
                "n_lanes":3

            } for v in [0.75,1,1.25,1.5,1.75,2]]
class RepetitiveTrafficModel(TrafficModel):

    def __init__(self, experiment):
        super().__init__(experiment, read_agents=False)
        self.measures_files = "output_files/" + experiment + "/measures_files.csv"
        self.finished = False
        self.sessions = x_sessions
        # [
        #     {
        #         "n_agents": 20,
        #         "max_speed_avg": 1.5,
        #         "max_speed_dev": 0.3,
        #
        #         "desired_distance_avg": 30,
        #         "desired_distance_dev": 3,
        #
        #         "acceleration_avg": 1.5,
        #         "acceleration_dev": 0,
        #         "n_lanes":3
        #     }
        # ]
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
        print(session)
        self.session_times.append({"session_counter":self.session_counter,
                                   "start": self.time})
        self.session_counter += 1
        self.n_lanes = session["n_lanes"]
        super().make_random_agents(session["n_agents"], session["max_speed_avg"],
                                   session["max_speed_dev"], session["desired_distance_avg"],
                                   session["desired_distance_dev"], session["acceleration_avg"],
                                   session["acceleration_dev"], starting_id=self.agentID_counter)
        self.agentID_counter += session["n_agents"]


    def data_collector_save(self,tm):
        agent_data = self.datacollector.get_agent_vars_dataframe()
        agent_data.to_csv(self.agent_data_file)
        agent_data = pd.read_csv(self.agent_data_file)
        agent_data["Velocity"] = agent_data["Velocity"].apply(lambda x: float(x.split(" ")[0].replace("[", "")))
        agent_data["Velocity"] = agent_data["Velocity"].astype(float)
        measures_data =collect_data(agent_data,sessions=self.sessions,measure_times=tm)
        measures_data.to_csv(self.measures_files)




