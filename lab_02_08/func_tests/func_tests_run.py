from PyQt5.QtWidgets import QApplication
from datetime import datetime

from sys import path, argv
from json import load

path.append("./src")
from main import Main
from geom import Point

app = QApplication(argv)
with open("./func_tests/func_tests.json") as input_file:
    sr = load(input_file)
    for data in sr:
        rvr = Main()
        rvr.ui_graph()
        start_time = datetime.now()
        for elem in data["data"]:
            if elem["operation"] == "scale":
                center = Point(elem["centerX"], elem["centerY"])
                rvr.picture.scale(elem["kX"], elem["kY"], center)
            elif elem["operation"] == "move":
                rvr.picture.move(elem["dX"], elem["dY"])
            elif elem["operation"] == "rotate":
                center = Point(elem["centerX"], elem["centerY"])
                rvr.picture.rotate(elem["phi"], center)
        rvr.draw_picture("results/" + data["name"])
        with open("temp", "a") as output_file:
            dt = (datetime.now() - start_time).microseconds // 1000
            output_file.write(data["name"] + "\t" + str(dt) + "\n")
