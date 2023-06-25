import json

from src.traffic.gui import GUI
from src.traffic.model import TrafficModel
import os

from src.traffic.repetitive_model import RepetitiveTrafficModel

experiment = "experiment-traffic-lights"
os.makedirs(os.path.dirname("output_files/" + experiment + "/"), exist_ok=True)
gui = GUI(TrafficModel(
    experiment=experiment,
    # read_nodes=True,
    # read_agents=False
))
gui.run()
