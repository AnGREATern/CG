from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint
from datetime import datetime

from sys import path, argv
from json import load

path.append("./src")
from canvas import Canvas

app = QApplication(argv)
with open("./func_tests/func_tests.json") as input_file:
    sr = load(input_file)
    for data in sr:
        canvas = Canvas()
        for point in data["polygon"]:
            canvas.polygon.addPoint(QPoint(point["x"], point["y"]))
        canvas.closePolygon()
        for line in data["lines"]:
            canvas.segment_list.addPoint(QPoint(line["start"]["x"], line["start"]["y"]))
            canvas.segment_list.addPoint(QPoint(line["end"]["x"], line["end"]["y"]))
        start_time = datetime.now()
        canvas.clipSegments()
        total_time = (datetime.now() - start_time).microseconds
        canvas.saveImage("results/" + data["name"])
        with open("temp", "a") as output_file:
            output_file.write(data["name"] + "\t" + str(total_time) + "\n")
