from videotrackr.select_region_ui import Ui_Dialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox
from PySide6.QtCore import Qt
import videotrackr.strings.ui_strings as ui_strings

class sr_controller(Ui_Dialog, QDialog):
    def __init__(self, pixmap):
        super(sr_controller, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        self.ui.rawFrame.changePixmap(pixmap)
        self.ui.rawFrame.setClickable(True)
        self.ui.rawFrame.MousePressSignal.connect(self.receiveMousePress)
        self.ui.rawFrame.MouseReleaseSignal.connect(self.receiveMouseRelease)
        
        self.ui.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(lambda: self.resetRegion())

        self.start_point = None
        self.end_point = None

    def receiveMousePress(self, click_pos):
        self.start_point = click_pos
        self.end_point = None
        self.updateStatus()

    def receiveMouseRelease(self, click_pos):
        self.end_point = click_pos
        self.updateStatus()

    def updateStatus(self):
        if self.start_point == None and self.end_point == None:
            self.ui.status.setText(ui_strings.NO_REGION)
        elif self.start_point != None and self.end_point == None:
            self.ui.status.setText(ui_strings.FROM_REGION + " (" + str(self.start_point.x()) + ", " + str(self.start_point.y()) + ")")
        else:
            self.ui.status.setText(ui_strings.FROM_REGION + " (" + str(self.start_point.x()) + ", " + str(self.start_point.y()) + ") " + ui_strings.TO_REGION + " (" + str(self.end_point.x()) + ", " + str(self.end_point.y()) + ")")

    def resetRegion(self):
        self.start_point = None
        self.end_point = None
        self.updateStatus()