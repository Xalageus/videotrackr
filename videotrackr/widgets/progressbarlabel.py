import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore

class ProgressBarLabel(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ProgressBarLabel, self).__init__(parent)
        grid = QtWidgets.QGridLayout()

        self.bar = QtWidgets.QProgressBar()
        self.bar.setMaximum(100)
        self.bar.setMinimum(0)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)

        self.label=QtWidgets.QLabel("0%")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        grid.addWidget(self.bar, 0,0)
        grid.addWidget(self.label, 0,0)
        self.setLayout(grid)

        self.message = ""

    def set_message(self, message):
        self.message = message

    def remove_message(self):
        self.message = ""

    def set_progress(self, progress):
        self.bar.setValue(progress)
        progressLabel = int((progress / self.bar.maximum()) * 100)
        
        if self.message == "":
            self.label.setText(str(progressLabel) + "%")
        else:
            self.label.setText(str(self.message) + " - " + str(progressLabel) + "%")