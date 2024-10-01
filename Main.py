import sys
import os
import random
import LogHours
from RunGame import GameRun, LogTime
from LogHours import read_logged_hours
from PySide6 import QtCore, QtWidgets, QtGui


log_file_path = "logged_hours.txt"
Hours = 0.00


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.app_path = None
        self.icon_path = "" # 128x128
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle("Sky Launcher")
        Total_Hours = read_logged_hours(log_file_path)


        self.addgame = QtWidgets.QPushButton("Set Game file path")
        self.GameButton = QtWidgets.QPushButton("Run Game!")
        self.gamepathtext = QtWidgets.QLabel("No Game Path", alignment=QtCore.Qt.AlignCenter)
        self.Hours_Text = QtWidgets.QLabel(Total_Hours, alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.addgame)
        self.layout.addWidget(self.GameButton)
        self.layout.addWidget(self.gamepathtext)
        self.layout.addWidget(self.Hours_Text)
        self.GameButton.clicked.connect(self.GB)
        self.addgame.clicked.connect(self.open_file_dialog)

    def GB(self):
        if self.app_path:
            widget.hide()
            elapsed_time = GameRun(self.app_path)
            LogTime(elapsed_time)
            self.Hours_Text.setText(read_logged_hours(log_file_path))
            widget.show()
        else:
            # Show a warning message box
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Please set the game file path first.",
                QtWidgets.QMessageBox.Ok
            )

    def open_file_dialog(self):
        # Open the file dialog and get the selected file path
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a File")
        if file_path:
            #Get File name and remove extention (.exe ect..)
            file_name = os.path.basename(file_path)
            game_name, _ = os.path.splitext(file_name)

            #set text for game name and sets the app_path
            self.gamepathtext.setText(game_name.capitalize())
            self.app_path = file_path

    


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())