from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint
from datetime import datetime

from sys import path, argv
from json import load

path.append("./src")
from main import Main

app = QApplication(argv)
with open("./func_tests/func_tests.json") as input_file:
    sr = load(input_file)
    for data in sr:
        picture = Main()
        picture.ui_graph()
        total_time = 0
        picture.rectangle.setTopLeft(
            QPoint(data["rectangle"]["topLeft"]["x"], data["rectangle"]["topLeft"]["y"])
        )
        picture.rectangle.setBottomRight(
            QPoint(
                data["rectangle"]["bottomRight"]["x"],
                data["rectangle"]["bottomRight"]["y"],
            )
        )
        picture.segment.setP1(
            QPoint(data["line"]["start"]["x"], data["line"]["start"]["y"])
        )
        picture.segment.setP2(
            QPoint(data["line"]["end"]["x"], data["line"]["end"]["y"])
        )
        start_time = datetime.now()
        picture.clip_segment()
        total_time = (datetime.now() - start_time).microseconds // 1000
        picture.draw_picture("results/" + data["name"])
        with open("temp", "a") as output_file:
            output_file.write(data["name"] + "\t" + str(total_time) + "\n")
