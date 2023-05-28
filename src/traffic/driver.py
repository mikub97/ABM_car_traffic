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
        self.pos = pos,
        self.car_size = car_size
        self.max_speed = max_speed,
        self.acceleration = acceleration,
        self.velocity = velocity
        self.desired_distance = desired_distance
        self.current_lane = current_lane,
        self.start_node = start_node
        self.end_node = end_node

        # marking all previous nodes as already passed
        # and the rest that are still to be reached
        self.node_checkpoints = [True for _ in range(0, start_node + 1)]
        self.node_checkpoints += [False for _ in range(start_node + 1, model.n_nodes)]

        self.strategy = strategy


    def driver_ahead(self):
        min_distance = float("inf")
        ahead = None
        for d in self.model.drivers:
            if d.unique_id is not self.unique_id & d.current_lane[0] is self.current_lane[0]:
                dist = d.pos[0]-self.pos[0]
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

        # if there is a node to still to be reached, give me the index of the closest,
        # save it as next_node
        try:
            next_node = self.node_checkpoints.index(False)
        except ValueError:
            return  # the destination

        # calculate the new position
        v = self.calc_v()
        new_pos = self.pos + v #self.velocity + sep

        # check if a checkpoint is reached
        if self.model.nodes_distances[next_node] <= new_pos[0]:  # next_node is reached
            self.node_checkpoints[next_node] = True  # set that checkpoint as reached
            if next_node == self.end_node or next_node == self.model.n_nodes - 1:  # the checkpoint is the last node in the model
                return

        self.model.space.move_agent(self, new_pos)

    def calc_v(self):
        """

        """
        ahead = self.driver_ahead()
        if ahead is None:
            if self.velocity[0]<self.max_speed[0]:
                self.velocity[0]+=self.acceleration[0]
            return self.velocity

        v = np.zeros(2)
        actual_distance = self.model.space.get_distance(self.pos, ahead.pos)
        if self.velocity[0]<=self.max_speed[0]:
            max_speed = self.velocity[0]+self.acceleration[0]
        else:
            max_speed = self.max_speed[0]
        v[0] = max_speed*self.model.separation_k*(np.tanh(actual_distance-self.desired_distance)+np.tanh(self.desired_distance))
        self.velocity+=v[0]
        return v

    def accelerate(self):
        if self.velocity<self.max_speed[0]:
            self.velocity+=self.acceleration[0]
    def switch_lane(self):
        """
        For now, 'teleports' to a random lane
        TODO - not working properly yet
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
        self.current_lane = (self.current_lane[0] + 1,)
        new_pos = self.pos - (0, self.model.lane_width)
        self.model.space.move_agent(self, new_pos)

    def teleport_right(self):
        self.current_lane = (self.current_lane[0] - 1,)
        new_pos = self.pos + (0, self.model.lane_width)
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
