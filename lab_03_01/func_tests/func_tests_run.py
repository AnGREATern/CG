from PyQt5.QtWidgets import QApplication
from datetime import datetime

from sys import path, argv
from json import load

path.append("./src")
from main import Main
from line_window import LineWindow

app = QApplication(argv)
with open("./func_tests/func_tests.json") as input_file:
    sr = load(input_file)
    for data in sr:
        graph_win = Main()
        graph_win.ui_graph()
        total_time = 0
        for elem in data["data"]:
            if elem["operation"] == "spectrum":
                draw_win = LineWindow(graph_win, True)
                draw_win.le_x_start.setText(str(elem["centerX"]))
                draw_win.le_y_start.setText(str(elem["centerY"]))
                draw_win.le_x_end.setText(str(elem["step"]))
                draw_win.le_y_end.setText(str(elem["length"]))
                draw_win.cb_build.setCurrentText(elem["algorithm"])
                start_time = datetime.now()
                draw_win.make_spectrum()
            else:
                draw_win = LineWindow(graph_win, False)
                draw_win.le_x_start.setText(str(elem["startX"]))
                draw_win.le_y_start.setText(str(elem["startY"]))
                draw_win.le_x_end.setText(str(elem["endX"]))
                draw_win.le_y_end.setText(str(elem["endY"]))
                draw_win.cb_build.setCurrentText(elem["algorithm"])
                start_time = datetime.now()
                draw_win.make_line()
            total_time += (datetime.now() - start_time).microseconds // 1000
        graph_win.draw_picture("results/" + data["name"])
        with open("temp", "a") as output_file:
            output_file.write(data["name"] + "\t" + str(total_time) + "\n")
