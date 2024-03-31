from PyQt5.QtWidgets import QApplication
from datetime import datetime

from sys import path, argv
from json import load

path.append("./src")
from main import Main
from line_window import LineWindow
from spectrum_window import SpectrumWindow

app = QApplication(argv)
with open("./func_tests/func_tests.json") as input_file:
    sr = load(input_file)
    for data in sr:
        graph_win = Main()
        graph_win.ui_graph()
        start_time = datetime.now()
        for elem in data["data"]:
            if elem["operation"] == "spectrum":
                draw_win = SpectrumWindow(graph_win)
                draw_win.le_x_center.setText(str(elem["centerX"]))
                draw_win.le_y_center.setText(str(elem["centerY"]))
                draw_win.le_step.setText(str(elem["step"]))
                draw_win.le_length.setText(str(elem["length"]))
                draw_win.cb_build.setCurrentText(elem["algorithm"])
                draw_win.make_spectrum()
            else:
                draw_win = LineWindow(graph_win)
                draw_win.le_x_start.setText(str(elem["startX"]))
                draw_win.le_y_start.setText(str(elem["startY"]))
                draw_win.le_x_end.setText(str(elem["endX"]))
                draw_win.le_y_end.setText(str(elem["endY"]))
                draw_win.cb_build.setCurrentText(elem["algorithm"])
                draw_win.make_line()
        graph_win.draw_picture("results/" + data["name"])
        with open("temp", "a") as output_file:
            dt = (datetime.now() - start_time).microseconds // 1000
            output_file.write(data["name"] + "\t" + str(dt) + "\n")
