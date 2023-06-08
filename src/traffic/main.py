import json

from src.traffic.gui import GUI
from src.traffic.model import TrafficModel


experiment = "3_lanes_no_lights_5_cars"

gui = GUI(TrafficModel(
         experiment=experiment
    ))
gui.run()