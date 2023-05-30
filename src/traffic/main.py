import json

from src.traffic.gui import GUI
from src.traffic.model import TrafficModel


gui = GUI(TrafficModel(
         drivers_json_file="json_data/drivers.json",
         # nodes_json_file="json_data/lights.json",
         traffic_json_file="json_data/traffic.json"
    ))
gui.run()