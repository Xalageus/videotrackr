import videotrackr.video
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox
from PySide6.QtCore import Qt
from videotrackr.logger import logger
import videotrackr.strings.ui_strings as ui_strings

class pe_controller():
    def __init__(self, propEditorWidget: QTableWidget, tracker: videotrackr.video.video_tracker, DEBUG):
        self.debug_logger = logger(DEBUG)

        self.editor = propEditorWidget
        self.tracker = tracker
        
        self.editor.setRowCount(6)

        hframesLabel = QTableWidgetItem(ui_strings.HISTORY_FRAMES)
        hframesLabel.setFlags(Qt.ItemIsEnabled)
        self.editor.setItem(0, 0, hframesLabel)
        hframes = QTableWidgetItem(str(self.tracker.data.history_frames))
        hframes.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
        self.editor.setItem(0, 1, hframes)

        distLabel = QTableWidgetItem(ui_strings.DIST_THRESHOLD)
        distLabel.setFlags(Qt.ItemIsEnabled)
        self.editor.setItem(1, 0, distLabel)
        dist = QTableWidgetItem(str(self.tracker.data.dist_threshold))
        dist.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
        self.editor.setItem(1, 1, dist)

        shadowsLabel = QTableWidgetItem(ui_strings.SHADOWS)
        shadowsLabel.setFlags(Qt.ItemIsEnabled)
        self.editor.setItem(2, 0, shadowsLabel)
        shadows = QTableWidgetItem()
        shadows.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        if self.tracker.data.shadows:
            shadows.setCheckState(Qt.Checked)
        else:
            shadows.setCheckState(Qt.Unchecked)
        self.editor.setItem(2, 1, shadows)

        minareaLabel = QTableWidgetItem(ui_strings.MIN_AREA)
        minareaLabel.setFlags(Qt.ItemIsEnabled)
        self.editor.setItem(3, 0, minareaLabel)
        minarea = QTableWidgetItem(str(self.tracker.data.min_area))
        minarea.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
        self.editor.setItem(3, 1, minarea)

        maxareaLabel = QTableWidgetItem(ui_strings.MAX_AREA)
        maxareaLabel.setFlags(Qt.ItemIsEnabled)
        self.editor.setItem(4, 0, maxareaLabel)
        maxarea = QTableWidgetItem(str(self.tracker.data.max_area))
        maxarea.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
        self.editor.setItem(4, 1, maxarea)

        zoomLabel = QTableWidgetItem(ui_strings.ZOOM_LEVEL)
        zoomLabel.setFlags(Qt.ItemIsEnabled)
        self.editor.setItem(5, 0, zoomLabel)
        zoom = QTableWidgetItem(str(self.tracker.data.zoom_level))
        zoom.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
        self.editor.setItem(5, 1, zoom)

        self.editor.itemChanged.connect(self.update_properties)

    def destroy(self):
        self.editor.setRowCount(0)
        self.editor.itemChanged.disconnect()

    def update_properties(self, item):
        row = item.row()
        self.debug_logger.print_debug_info(24, row)

        if row == 0:
            self.tracker.data.history_frames = int(item.text())
        elif row == 1:
            self.tracker.data.dist_threshold = int(item.text())
        elif row == 2:
            self.tracker.data.shadows = bool(item.checkState())
        elif row == 3:
            self.tracker.data.min_area = int(item.text())
        elif row == 4:
            self.tracker.data.max_area = int(item.text())
        elif row == 5:
            self.tracker.update_zoom_level(int(item.text()))