from videotrackr.__init__ import __version__ as version
from videotrackr.about_ui import Ui_Dialog
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

class about_controller(Ui_Dialog, QDialog):
    def __init__(self):
        super(about_controller, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        
        self.ui.version.setText("<html><head/><body><p><span style=\" font-size:14pt;\">" + version + "</span></p></body></html>")