from videotrackr.main_ui import Ui_MainWindow
from PySide6.QtCore import QSize, Qt, Signal, QThread
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
import videotrackr.strings.ui_strings as ui_strings
from videotrackr.video import video_tracker
from videotrackr.enums.state import State
from videotrackr.logger import logger
from videotrackr.widgets.progressbarlabel import ProgressBarLabel
from videotrackr.pe_controller import pe_controller
from videotrackr.about_controller import about_controller

class main_controller(Ui_MainWindow, QMainWindow):
    def __init__(self, DEBUG):
        super(main_controller, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.debugging = False

        self.debug_init(DEBUG)

        self.ui.actionAbout_Qt.triggered.connect(lambda: self.open_about_qt())
        self.ui.actionOpen.triggered.connect(lambda: self.open_file())
        self.ui.actionClose.triggered.connect(lambda: self.prepare_destroy_tracker())
        self.ui.playPauseButton.clicked.connect(lambda: self.play_pause())
        self.ui.actionQuit.triggered.connect(lambda: self.close())
        self.ui.actionProperty_Editor.toggled.connect(self.show_hide_pe)
        self.ui.actionAbout.triggered.connect(lambda: self.open_about())

        #Connect playhead signals and slots
        self.ui.playHeadSlider.sliderMoved.connect(lambda: self.update_playHead())
        self.ui.playHeadSlider.sliderReleased.connect(lambda: self.playHead_sliderUp())
        self.ui.playHeadSlider.sliderPressed.connect(lambda: self.playHead_sliderDown())

        self.playHeadChanged = False
        self.sliderIgnoreUpdates = False
        self.destroyOnLoad = False
        self.tempVideoFile = None
        self.tracker = None
        self.tracker_thread = None
        self.current_state = State.Nothing_Loaded
        self.pe = None

    def open_about_qt(self):
        QMessageBox.aboutQt(self, ui_strings.TITLE)

    def init_tracker(self, video_file):
        if self.current_state != State.Nothing_Loaded:
            self.prepare_destroy_tracker()
            self.destroyOnLoad = True
            self.tempVideoFile = video_file
        else:
            self.current_state = State.Initializing

            #Init tracker
            self.tracker = video_tracker(video_file, self.debugging)

            #Setup tracker thread
            self.tracker_thread = QThread(self)
            self.tracker.moveToThread(self.tracker_thread)

            #Setup Property Editor
            self.pe = pe_controller(self.ui.propertyEditor, self.tracker, self.debugging)

            #Connect signals and slots
            self.tracker.gen_start.connect(self.tracker.receive_signal)
            self.tracker.finished.connect(self.tracker_thread.quit)
            self.tracker.FrameSignal.connect(self.update_frames)
            self.tracker.stopped.connect(self.tracker_stopped)
            self.tracker.gen_history.connect(self.tracker.render_history)

            self.tracker_thread.start()
            self.current_state = State.Idle

            self.init_controls(self.tracker.video_data.num_frames)

    def open_file(self):
        video_file = str(QFileDialog.getOpenFileName(self, ui_strings.OPEN_VIDEO_FILE)[0])
        if video_file != "":
            self.init_tracker(video_file)

    def convert_frame(self, frame):
        qImage = None

        if len(frame.shape) == 3:
            height, width, byteValue = frame.shape
            byteValue = byteValue * width

            qImage = QImage(frame, width, height, byteValue, QImage.Format_BGR888)
        else:
            #This is a mask
            height, width = frame.shape

            qImage = QImage(frame, width, height, QImage.Format_Grayscale8)

        return QPixmap(qImage)

    def update_frames(self, frame_num):
        if self.current_state == State.Preparing_History:
            self.pb.set_progress(self.pb.bar.value() + 1)
        else:
            self.debug_logger.print_debug_info(12, frame_num)
            self.ui.rawFrame.changePixmap(self.convert_frame(self.tracker.frame_cnt))
            self.ui.maskFrame.changePixmap(self.convert_frame(self.tracker.mask))

            if self.tracker.final is not None:
                self.ui.outputFrame.changePixmap(self.convert_frame(self.tracker.final))

            if not self.sliderIgnoreUpdates:
                self.ui.playHeadSlider.setValue(self.tracker.video_data.current_frame)

    def prepare_destroy_tracker(self):
        if self.current_state == State.Running:
            self.debug_logger.print_debug_info(13)
            self.current_state = State.Destroying
            self.tracker.running = False
        else:
            self.current_state = State.Destroying
            self.destroy_tracker()
        
    def destroy_tracker(self):
        self.tracker.destroy()
        self.tracker = None
        self.tracker_thread = None

        self.debug_logger.print_debug_info(15)

        #Clear image labels
        self.ui.rawFrame.clearPixmap()
        self.ui.maskFrame.clearPixmap()
        self.ui.outputFrame.clearPixmap()

        self.current_state = State.Nothing_Loaded
        self.reset_controls()

    def tracker_stopped(self):
        if self.current_state == State.Destroying:
            self.destroy_tracker()
            self.init_tracker(self.tempVideoFile)
            self.destroyOnLoad = False
            self.tempVideoFile = None
        elif self.current_state == State.Running:
            self.current_state = State.Stopped
            self.update_play_button()
        elif self.current_state == State.Preparing_History:
            self.pb.hide()
            self.pb.destroy()
            self.pb = None

            self.current_state == State.Stopped
            self.ui.playHeadSlider.setEnabled(True)
            self.play_pause()
        elif self.current_state == State.Slider_Moved_While_Running:
            self.sliderIgnoreUpdates = False
            self.update_history()

#region DEBUG_FUNCTIONS
    def debug_init(self, debug):
        self.debug_logger = logger(debug)

        if not debug:
            self.ui.menuDEBUG.setEnabled(False)
            self.ui.menuDEBUG.menuAction().setVisible(False)
        else:
            self.ui.actionRender_next_frame.triggered.connect(lambda: self.debug_render_next())
            self.ui.actionPrint_current_state.triggered.connect(lambda: self.debug_print_cur_state())
            self.ui.actionPrint_tracker_video_data.triggered.connect(lambda: self.debug_print_tracker_video_data())
            self.ui.actionPrint_tracker_data.triggered.connect(lambda: self.debug_print_tracker_data())
            self.ui.actionInit.triggered.connect(lambda: self.create_pb())
            self.ui.actionDestroy.triggered.connect(lambda: self.destroy_pb())
            self.ui.actionIncrement_5.triggered.connect(lambda: self.debug_pb_increment_5())
            self.ui.actionIncrement_50.triggered.connect(lambda: self.debug_pb_increment_50())
            self.ui.actionSet_Label_Message_1.triggered.connect(lambda: self.debug_pb_set_message_1())
            self.ui.actionSet_Label_Message_2.triggered.connect(lambda: self.debug_pb_set_message_2())
            self.ui.actionRemove_Label_Message.triggered.connect(lambda: self.pb.remove_message())
            self.ui.actionPrint_real_current_frame.triggered.connect(lambda: self.debug_print_real_current_frame())
            self.debug_logger.print_debug_info(0)
            self.debugging = True

    def debug_render_next(self):
        if not self.current_state.Running:
            self.debug_logger.print_debug_info(18)
            self.tracker.gen_start.emit(False)

    def debug_print_cur_state(self):
        self.debug_logger.print_debug_info(1, self.current_state)

    def debug_print_tracker_video_data(self):
        self.debug_logger.print_debug_info(2, self.tracker.video_data)

    def debug_print_tracker_data(self):
        self.debug_logger.print_debug_info(3, self.tracker.data)

    def destroy_pb(self):
        self.pb.hide()
        self.pb.destroy()
        self.pb = None

    def create_pb(self):
        self.pb = ProgressBarLabel(self)
        self.ui.verticalLayout_2.addWidget(self.pb)

    def debug_pb_increment_5(self):
        self.pb.set_progress(self.pb.bar.value() + 5)

    def debug_pb_increment_50(self):
        self.pb.set_progress(self.pb.bar.value() + 50)

    def debug_pb_set_message_1(self):
        self.pb.set_message("Hello World!")

    def debug_pb_set_message_2(self):
        self.pb.set_message("This is the second debug message")

    def debug_print_real_current_frame(self):
        self.debug_logger.print_debug_info(23, self.tracker.get_real_current_frame())

#endregion

    def reset_controls(self):
        self.ui.playHeadSlider.setValue(0)
        self.ui.playHeadSlider.setEnabled(False)
        self.update_play_button()
        self.ui.playPauseButton.setEnabled(False)

        self.pe.destroy()
        self.pe = None

        #Check if we have a progress bar
        try:
            self.pb.hide()
            self.pb.destroy()
            self.pb = None
        except:
            #Do nothing
            pass

    def closeEvent(self, event):
        if self.current_state is not State.Nothing_Loaded:
            self.current_state = State.Destroying
            self.destroy_tracker()

    def play_pause(self):
        if self.current_state == State.Running:
            self.ui.playPauseButton.setEnabled(False)
            self.ui.playPauseButton.setText(ui_strings.PAUSING)
            self.tracker.running = False
        else:
            self.current_state = State.Running
            self.update_play_button()
            if self.playHeadChanged:
                self.update_history()
            else:
                self.debug_logger.print_debug_info(16, int(self.ui.playHeadSlider.value()))
                self.tracker.video_data.current_frame = int(self.ui.playHeadSlider.value())
                self.debug_logger.print_debug_info(18)
                self.tracker.gen_start.emit(True)

    def update_play_button(self):
        if self.current_state == State.Running:
            self.ui.playPauseButton.setEnabled(True)
            self.ui.playPauseButton.setText(ui_strings.PAUSE)
        else:
            if self.current_state == State.Stopped:
                self.ui.playPauseButton.setEnabled(True)
                self.ui.playPauseButton.setText(ui_strings.PLAY)
            if self.current_state == State.Nothing_Loaded:
                self.ui.playPauseButton.setText(ui_strings.PLAY)

    def init_controls(self, video_length):
        self.ui.playHeadSlider.setMaximum(video_length)
        self.ui.playHeadSlider.setEnabled(True)
        self.ui.playPauseButton.setEnabled(True)

    def update_history(self):
        self.ui.playHeadSlider.setEnabled(False)
        self.ui.playPauseButton.setEnabled(False)
        self.playHeadChanged = False

        self.current_state = State.Preparing_History
        self.pb = ProgressBarLabel(self)
        self.ui.verticalLayout_2.addWidget(self.pb)
        self.pb.bar.setMaximum(self.tracker.data.history_frames)
        self.pb.set_message(ui_strings.PREPARE_HISTORY)
        self.tracker.gen_history.emit(self.ui.playHeadSlider.value())

    def update_playHead(self):
        self.playHeadChanged = True

    def playHead_sliderUp(self):
        if self.current_state == State.Running:
            self.current_state = State.Slider_Moved_While_Running
            self.tracker.running = False
        else:
            self.sliderIgnoreUpdates = False

    def playHead_sliderDown(self):
        self.sliderIgnoreUpdates = True

    def show_hide_pe(self, checked):
        if checked:
            self.ui.propertyDockWidget.show()
        else:
            self.ui.propertyDockWidget.hide()

    def open_about(self):
        about = about_controller()
        about.exec_()