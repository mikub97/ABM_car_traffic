import pandas as pd

from src.traffic.analysis_utils import collect_data
from src.traffic.model import TrafficModel

class RepetitiveTrafficModel(TrafficModel):

    def __init__(self, experiment,measure_settings, sessions):
        super().__init__(experiment,
                         measure_settings=measure_settings,
                         read_agents=False, read_nodes=True)
        self.measures_file = "output_files/" + experiment + "/measures.csv"
        self.collected_measures_file = "output_files/"+experiment+"/collected_measures.csv"
        self.finished = False
        self.sessions = sessions
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
        print(f"Running session nr {self.session_counter-1}")
        print(session)

    def data_collector_save(self):
        agent_data = self.datacollector.get_agent_vars_dataframe().reset_index()
        agent_data["Velocity"] = agent_data["Velocity"].apply(lambda x: float(x[0]))
        agent_data["Velocity"] = agent_data["Velocity"].astype(float)
        measures_data = collect_data(agent_data=agent_data,
                                     sessions=self.sessions,
                                     measure_times=self.time_measures,
                                     measure_settings=self.measure_settings,
                                     session_counter=self.session_counter)
        agent_data.to_csv(self.agent_data_file)
        measures_data.to_csv(self.measures_file)
        try:
            big_frame = pd.read_csv(self.collected_measures_file, header=0)
            big_frame = pd.concat([big_frame, measures_data], ignore_index=True)
        except:
            big_frame = measures_data
        big_frame.to_csv(self.collected_measures_file, index=False)
