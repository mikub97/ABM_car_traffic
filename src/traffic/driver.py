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
        max_speed,
        acceleration,
        current_lane,
        start_node,
        end_node
    ):
        """
        Create a new Driver  agent.

        Args:

        """
        super().__init__(driver_id, model)
        self.pos = pos,
        self.max_speed = max_speed,
        self.acceleration = acceleration,
        self.current_lane = current_lane,
        self.start_node = start_node
        self.end_node = end_node
        strategy = None


    def step(self):
        """
        Get move accordingly.
        """

        self.pos[0]+=self.max_speed[0]

        self.model.space.move_agent(self, self.pos)



    def __str__(self):
        return f"Driver {self.unique_id} at pos({self.pos}), lane({self.current_lane[0]}), node({self.start_node})"
