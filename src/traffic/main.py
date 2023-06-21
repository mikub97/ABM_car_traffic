import json

from src.traffic.gui import GUI
from src.traffic.model import TrafficModel
import os

experiment = "2_lane_10_green_lights_20_cars"
# make sure that the directory output_files exists
os.makedirs(os.path.dirname("output_files/" + experiment + "/"), exist_ok=True)
model = TrafficModel(
    experiment=experiment
)
gui = GUI(model)
gui.run()
