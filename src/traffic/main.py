import json

from src.traffic.gui import GUI
from src.traffic.model import TrafficModel


experiment = "2_lane_no_lights_20_cars"

gui = GUI(TrafficModel(
         experiment=experiment
    ))
gui.run()