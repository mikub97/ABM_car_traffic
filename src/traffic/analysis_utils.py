import numpy as np
import pandas as pd


def calc_flow_rate(df, t_start, t_end, measure_point_x, accepted_dist_delta):
    return df[
        (df["Is_alive"] == True) & (df["Step"] > t_start) & (df["Step"] < t_end) & (
                    abs(df["X"] - measure_point_x) < accepted_dist_delta)].drop_duplicates("AgentID").shape[0]


def flow_rate_running_avg(df, t_start, t_end, measure_point_x, accepted_dist_delta, window_size,
                          running_step=100):
    flow_rates = []
    for t in range(t_start, t_end + 1 - window_size, running_step):
        flow_rates.append(calc_flow_rate(df, t, t + window_size, measure_point_x, accepted_dist_delta))
    running_avg = sum(flow_rates) / len(flow_rates)
    return running_avg


def calc_density(df, x_start, x_end, time):
    return df[(df["Is_alive"] == True) & (df["X"] > x_start) & (df["X"] < x_end) & (
                df["Step"] == time)].drop_duplicates("AgentID").shape[0] / (x_end - x_start)


def density_running_avg(df, x_start, x_end, t_start, t_end, running_step=5):
    densities = []
    for t in range(t_start, t_end + 1, running_step):
        densities.append(calc_density(df, x_start, x_end, t))
    running_avg = sum(densities) / len(densities)
    return running_avg


def calc_mean_velocity(df, t_start, t_end, x_start, x_end):
    mean_velocity = np.mean(df.loc[df["Is_alive"] == True
                                           & (df['X'] > x_start)
                                           & (df['X'] < x_end)
                                           & (df["Step"] > t_start)
                                           & (df["Step"] > t_end)]["Velocity"])
    return mean_velocity


def collect_data(agent_data,sessions, measure_times,measure_settings,session_counter):
    measures = []
    if len(sessions) != len(measure_times):
        print("Something's wrong with measuring... Did you stop the simulation, during running?")
        print("Skipping measures from the last session...")
        sessions = sessions[:session_counter-1]
    for i,session in enumerate(sessions):
        measure = {
            "session_ix": i
        }
        measure.update(session)

        t_start = measure_times[i]["t_start"],
        t_end = measure_times[i]["t_end"],
        x_start = measure_settings["x_start"]
        #da fack ? I dont know
        t_end = t_end[0]
        t_start = t_start[0]
        x_end = measure_settings["x_end"]

        measure.update({
            't_start': t_start,
            't_end': t_end,
            'x_start': measure_settings["x_start"],
            'x_end': measure_settings["x_end"],
            'measure_point_x':measure_settings["measure_point_x"],
            'accepted_dist_delta':measure_settings["accepted_dist_delta"],
            'window_size': measure_settings["window_size"],
            'average_velocity': calc_mean_velocity(agent_data, t_start, t_end, x_start, x_end),
            'rolling_average_density': density_running_avg(agent_data,x_start, x_end, t_start, t_end,
                                                           running_step=measure_settings["rolling_average_density_running_step"]),
            'rolling_average_flow': flow_rate_running_avg(agent_data,t_start, t_end, measure_settings["measure_point_x"], measure_settings["accepted_dist_delta"], measure_settings["window_size"],
                                                          running_step=measure_settings["rolling_average_flow_running_step"])
        })
        measures.append(measure)
    return pd.DataFrame(measures)


