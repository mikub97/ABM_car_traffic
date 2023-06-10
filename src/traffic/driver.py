import random

import mesa
import numpy as np


class Driver(mesa.Agent):
    """
    A Driver agent.

    The agent follows N behaviors :

    """

    def __init__(
            self,
            driver_id,
            model,
            pos,
            car_size,
            velocity,
            max_speed,
            acceleration,
            desired_distance,
            current_lane,
            start_node,
            end_node,
            strategy
    ):
        """
        Create a new Driver  agent.

        Args:

        """
        super().__init__(driver_id, model)
        self.is_alive = False
        self.pos = pos,
        self.car_size = car_size
        self.max_speed = max_speed,
        self.acceleration = acceleration,
        self.velocity = velocity
        self.desired_distance = desired_distance
        self.current_lane = current_lane,
        self.start_node = start_node
        self.end_node = end_node
        self.delay = 0
        self.longlive = 0
        self.checkpoint_timestamps = []

        # marking all previous nodes as already passed
        # and the rest that are still to be reached
        self.node_checkpoints = [True for _ in range(0, start_node + 1)]
        self.node_checkpoints += [False for _ in range(start_node + 1, model.n_nodes)]

        self.strategy = strategy

    def node_ahead(self):
        try:
            return self.model.nodes[self.node_checkpoints.index(False)]  ## error TODO
        except ValueError:
            return None  # we have arrived the destination

    def driver_ahead(self):
        min_distance = float("inf")
        ahead = None
        for d in self.model.schedule.agents:
            if (d.unique_id != self.unique_id) & (d.current_lane[0] is self.current_lane[0]):
                dist = d.pos[0] - self.pos[0]
                if min_distance > dist > 0:
                    min_distance = dist
                    ahead = d
        return ahead

    def step(self):
        """
        Get move accordingly.
        First check if you have just passed a new checkpoint(node) in the step.
        If so, mark it and check the lane according to your strategy
        """
        self.longlive += 1
        if self.longlive < self.delay:
            return
        elif not self.is_alive:
            self.is_alive = True
            self.model.checkpoint_stamps.append({
                "DriverID": self.unique_id,
                "NodeID" : 0,
                'X': self.pos[0],
                'current_lane': self.current_lane[0],
                'time': self.longlive})

        node_ahead = self.node_ahead()
        driver_ahead = self.driver_ahead()

        # (re)calculate velocity and the new position
        self.calc_v(node_ahead, driver_ahead)
        new_pos = self.pos + self.velocity

        if new_pos[0] <= self.model.nodes[-1].pos[0]:
            self.model.space.move_agent(self, new_pos)

        # check if a checkpoint is reached
        if node_ahead.pos[0] <= new_pos[0]:  # next_node is reached
            self.node_checkpoints[node_ahead.unique_id] = True  # set that checkpoint as reached
            # if the checkpoint is the last node in the model, kill the agent
            self.model.checkpoint_stamps.append({
                "DriverID": self.unique_id,
                "NodeID": node_ahead.unique_id,
                'X': self.pos[0],
                'current_lane': self.current_lane[0],
                'time': self.longlive})

            if node_ahead.unique_id == self.end_node or node_ahead.unique_id == self.model.n_nodes - 1:
                self.kill()
                return
            # self.switch_lane()

    def kill(self):
        self.model.kill_driver(self.unique_id)
        self.is_alive = False

    def calc_v(self, node_ahead, driver_ahead):
        """

        """
        is_freeway = False
        if driver_ahead is None:
            closer_obj_ahead = node_ahead
            if closer_obj_ahead.state == "green":
                is_freeway = True
        elif node_ahead.pos[0] < driver_ahead.pos[0]:
            closer_obj_ahead = node_ahead
            if closer_obj_ahead.state == "green":
                closer_obj_ahead = driver_ahead
        else:
            closer_obj_ahead = driver_ahead

        if is_freeway:
            if self.velocity[0] < self.max_speed[0]:
                self.velocity[0] += self.acceleration[0]
            if self.velocity[0] > self.max_speed[0]:
                self.velocity[0] = self.max_speed[0]
            return

        actual_distance = closer_obj_ahead.pos[0] - self.pos[0]
        if self.velocity[0] < self.max_speed[0]:
            max_speed = self.velocity[0] + self.acceleration[0]
            if max_speed > self.max_speed[0]:
                max_speed = self.max_speed[0]
        else:
            max_speed = self.max_speed[0]
        self.velocity[0] = max_speed * 0.5 * (
                np.tanh(actual_distance - self.desired_distance) + np.tanh(self.desired_distance))

    def accelerate(self):
        if self.velocity < self.max_speed[0]:
            self.velocity += self.acceleration[0]

    def switch_lane(self):
        """
        For now, 'teleports' to a random lane
        """
        if self.current_lane[0] == 0:
            self.teleport_right()
        elif self.current_lane[0] == self.model.n_lanes - 1:
            self.teleport_left()
        else:
            if random.choice([True, False]):
                self.teleport_left()
            else:
                self.teleport_right()

    def teleport_left(self):
        self.current_lane = (self.current_lane[0] - 1,)
        new_pos = self.pos - (0, self.model.lane_width)  # TODO add 'if there is a free space in the lane'
        self.model.space.move_agent(self, new_pos)

    def teleport_right(self):
        self.current_lane = (self.current_lane[0] + 1,)
        new_pos = (self.pos[0], self.pos[1] + self.model.lane_width)  # TODO add 'if there is a free space in the lane'
        self.model.space.move_agent(self, new_pos)

    def __str__(self):
        return f"Driver {self.unique_id} at pos({self.pos}),\n lane({self.current_lane[0]}), start_node({self.start_node})" \
               f", end_node({self.end_node}), velocity({self.velocity})"

    # def to_dict(self):
    #     return {
    #         "pos":self.pos,
    #         "car_size":self.car_size,
    #         "max_speed":self.max_speed,
    #         "factorisation":self.acceleration,
    #         "velocity":self.velocity,
    #         "desired_distance":self.desired_distance,
    #         "current_lane":self.current_lane,
    #         "start_node":self.start_node,
    #         "end_node":self.end_node
    #     }
