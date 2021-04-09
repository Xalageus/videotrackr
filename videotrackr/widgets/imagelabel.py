from PySide6.QtGui import QPainter, QPixmap
import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui

class ImageLabel(QtWidgets.QLabel):
    ResizeSignal = QtCore.Signal(int)

    def __init__(self, parent):
        super(ImageLabel, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.setText("")
        self.pix = QPixmap()
        self.setPixmap(self.pix)
        self.ResizeSignal.connect(self.resizeEvent)
        self.installEventFilter(self)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if(event.type() == QtCore.QEvent.Resize):
            if not self.pix.isNull():
                pixmap = self.pix.scaled(self.width(), self.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                if pixmap.width()!=self.width() or pixmap.height()!=self.height():
                    self.ResizeSignal.emit(0)
        return super().eventFilter(watched, event)

    def resizeEvent(self, _):
        if not self.pix.isNull():
            size = self.size()
            self.setPixmap(self.pix.scaled(size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))

    #Paint event that is currently not needed
    # def paintEvent(self, event):
    #     if not self.pix.isNull():
    #         size = self.size()
    #         painter = QPainter()
    #         point = QtCore.QPoint(0, 0)
    #         scaledPix = self.setPixmap(self.pix.scaled(size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
    #         point.setX((size.width() - scaledPix.width() / 2))
    #         point.setY((size.height() - scaledPix.height() / 2))
    #         painter.drawPixmap(point, scaledPix)

    def changePixmap(self, img):
        self.pix = img
        self.repaint()
        self.ResizeSignal.emit(1)

    def clearPixmap(self):
        self.pix = QPixmap()
        self.setPixmap(self.pix)
        self.repaint()