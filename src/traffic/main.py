import json

from src.traffic.gui import GUI
from src.traffic.model import TrafficModel
import os


experiment = "experiment_trafficlights"
os.makedirs(os.path.dirname("output_files/" + experiment+"/"), exist_ok=True)
gui = GUI(TrafficModel(
         experiment=experiment
    ))
gui.run()