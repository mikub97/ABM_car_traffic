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


def collect_data(agent_data,sessions, measure_times):
    measures = []

    x_start = 500
    x_end = 600
    measure_point_x = 500
    accepted_dist_delta = 10
    window_size = 100

    for i,session in enumerate(sessions):
        t_start = measure_times[i*2]
        t_end = measure_times[i*2+1]
        measure = session
        measure.update({
            't_start':t_start,
            't_end':t_end,
            'x_start':x_start,
            'x_end':x_end,
            'measure_point_x':measure_point_x,
            'accepted_dist_delta':accepted_dist_delta,
            'window_size': window_size,
            'average_velocity': calc_mean_velocity(agent_data, t_start, t_end, x_start, x_end),
            'rolling_average_density': density_running_avg(agent_data,x_start, x_end, t_start, t_end, running_step=5),
            'rolling_average_flow': flow_rate_running_avg(agent_data,t_start, t_end, measure_point_x, accepted_dist_delta, window_size,
                                                          running_step=100)
        })
        measures.append(measure)
    return pd.DataFrame(measures)
