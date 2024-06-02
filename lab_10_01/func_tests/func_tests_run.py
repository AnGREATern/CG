from PyQt5.QtWidgets import QApplication
from datetime import datetime

from sys import path, argv
from json import load

path.append("./src")
from main import Main

app = QApplication(argv)
with open("./func_tests/func_tests.json") as input_file:
    sr = load(input_file)
    for data in sr:
        main = Main()
        main.cb_func.setCurrentText(str(data["function"]))
        main.le_x_from.setText(str(data["start_x"]))
        main.le_x_to.setText(str(data["end_x"]))
        main.le_x_step.setText(str(data["step_x"]))
        main.le_z_from.setText(str(data["start_z"]))
        main.le_z_to.setText(str(data["end_z"]))
        main.le_z_step.setText(str(data["step_z"]))
        main.cb_axis.setCurrentText(str(data["axis"]))
        main.le_phi.setText(str(data["angle"]))
        start_time = datetime.now()
        main.buildFigure()
        total_time = (datetime.now() - start_time).microseconds // 1000
        main.savePicture("results/" + data["name"])
        with open("temp", "a") as output_file:
            output_file.write(data["name"] + "\t" + str(total_time) + "\n")
