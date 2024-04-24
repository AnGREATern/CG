from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor
from datetime import datetime

from sys import path, argv
from json import load

path.append("./src")
from main import Main
import consts

app = QApplication(argv)
with open("./func_tests/func_tests.json") as input_file:
    sr = load(input_file)
    for data in sr:
        picture = Main()
        picture.ui_graph()
        total_time = 0
        for elem in data["polygon"]:
            for point in elem:
                picture.points[-1].append(QPoint(point["x"], point["y"]))
                picture.front_img.setPixel(
                    picture.points[-1][-1], QColor(*consts.LINE_COLOR_DEFAULT).rgba()
                )
                if len(picture.points[-1]) > 1:
                    picture.print_line(picture.points[-1][-2], picture.points[-1][-1])
            picture.close_polyline()
        picture.base_point = QPoint(data["base_point"]["x"], data["base_point"]["y"])
        start_time = datetime.now()
        picture.fill_polygon()
        total_time = (datetime.now() - start_time).microseconds // 1000
        picture.draw_picture("results/" + data["name"])
        with open("temp", "a") as output_file:
            output_file.write(data["name"] + "\t" + str(total_time) + "\n")
