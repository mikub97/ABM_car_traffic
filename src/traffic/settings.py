experiment = "experiment-traffic-lights"
measure_settings={
  "x_start": 200,
  "x_end": 800,
  "measure_point_x": 500,
  "accepted_dist_delta": 10,
  "window_size": 100,
  "rolling_average_density_running_step": 5,
  "rolling_average_flow_running_step": 100
}
sessions = [
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
    for v in [1.5,1.8, 2, 2.2]]