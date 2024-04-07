from PyQt5.QtWidgets import QApplication
from datetime import datetime

from sys import path, argv
from json import load

path.append("./src")
from main import Main
from ellipse_window import EllipseWindow
from spectrum_window import SpectrumWindow

app = QApplication(argv)
with open("./func_tests/func_tests.json") as input_file:
    sr = load(input_file)
    for data in sr:
        graph_win = Main()
        graph_win.ui_graph()
        total_time = 0
        for elem in data["data"]:
            if elem["operation"] == "spectrum":
                draw_win = SpectrumWindow(graph_win)
                draw_win.le_x_center.setText(str(elem["centerX"]))
                draw_win.le_y_center.setText(str(elem["centerY"]))
                draw_win.le_step.setText(str(elem["step"]))
                draw_win.le_radius.setText(str(elem["radius"]))
                draw_win.le_count.setText(str(elem["count"]))
                draw_win.cb_build.setCurrentText(elem["algorithm"])
                start_time = datetime.now()
                draw_win.make_spectrum()
            else:
                draw_win = EllipseWindow(graph_win)
                draw_win.le_x_center.setText(str(elem["centerX"]))
                draw_win.le_y_center.setText(str(elem["centerY"]))
                draw_win.le_ox_len.setText(str(elem["rX"]))
                draw_win.le_oy_len.setText(str(elem["rY"]))
                draw_win.cb_build.setCurrentText(elem["algorithm"])
                start_time = datetime.now()
                draw_win.make_ellipse()
            total_time += (datetime.now() - start_time).microseconds // 1000
        graph_win.draw_picture("results/" + data["name"])
        with open("temp", "a") as output_file:
            output_file.write(data["name"] + "\t" + str(total_time) + "\n")
