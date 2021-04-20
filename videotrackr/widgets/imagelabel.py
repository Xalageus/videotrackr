from PySide6.QtGui import QPainter, QPixmap
import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui

class ImageLabel(QtWidgets.QLabel):
    ResizeSignal = QtCore.Signal(int)
    MousePressSignal = QtCore.Signal(QtCore.QPoint)
    MouseReleaseSignal = QtCore.Signal(QtCore.QPoint)

    def __init__(self, parent):
        super(ImageLabel, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.setText("")
        self.clickable = False
        self.pix = QPixmap()
        self.pix_origin_point = QtCore.QPoint(0, 0)
        self.pix_end_point = QtCore.QPoint(0, 0)
        self.setPixmap(self.pix)
        self.ResizeSignal.connect(self.resizeEvent)
        self.installEventFilter(self)

    def setClickable(self, clickable):
        self.clickable = clickable

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
            if(self.clickable):
                self.pix_origin_point = self.calcOriginPoint()
                self.pix_end_point = self.calcEndPoint(self.pix_origin_point)

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

    def mousePressEvent(self, event):
        if not self.pix.isNull() and self.clickable:
            if(self.isWithinImage(event.pos())):
                click_pos = self.convertPointWithinBounds(event.pos())
                self.MousePressSignal.emit(self.convertPointToFullSize(click_pos))

    def mouseReleaseEvent(self, event):
        if not self.pix.isNull() and self.clickable:
            if(self.isWithinImage(event.pos())):
                click_pos = self.convertPointWithinBounds(event.pos())
                self.MouseReleaseSignal.emit(self.convertPointToFullSize(click_pos))

    def calcOriginPoint(self):
        # (Width/Height of label - Width/Height of pixmap) / 2
        x = (self.rect().getRect()[2] - self.pixmap().rect().getRect()[2]) / 2
        y = (self.rect().getRect()[3] - self.pixmap().rect().getRect()[3]) / 2
        return QtCore.QPoint(x, y)

    def calcEndPoint(self, origin_point):
        x = origin_point.x() + self.pixmap().rect().getRect()[2]
        y = origin_point.y() + self.pixmap().rect().getRect()[3]
        return QtCore.QPoint(x, y)

    def isWithinImage(self, click_pos):
        if(click_pos.x() >= self.pix_origin_point.x() and click_pos.x() <= self.pix_end_point.x()):
            if(click_pos.y() >= self.pix_origin_point.y() and click_pos.y() <= self.pix_end_point.y()):
                return True

        return False

    def convertPointWithinBounds(self, click_pos):
        x = click_pos.x() - self.pix_origin_point.x()
        y = click_pos.y() - self.pix_origin_point.y()
        return QtCore.QPoint(x, y)

    def getScaleMult(self):
        x_mult = self.pix.rect().getRect()[2] / self.pixmap().rect().getRect()[2]
        y_mult = self.pix.rect().getRect()[3] / self.pixmap().rect().getRect()[3]
        return (x_mult, y_mult)

    def convertPointToFullSize(self, click_pos):
        scale_mult = self.getScaleMult()
        x = scale_mult[0] * click_pos.x()
        y = scale_mult[1] * click_pos.y()
        return QtCore.QPoint(x, y)