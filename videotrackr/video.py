import cv2
import copy
from PySide6.QtCore import QObject, Signal
from videotrackr.render import render
from videotrackr.logger import logger

class tracker_data():
    def __init__(self, history_frames, dist_threshold, shadows, min_area, max_area, zoom_level):
        self.history_frames = history_frames
        self.dist_threshold = dist_threshold
        self.shadows = shadows
        self.min_area = min_area
        self.max_area = max_area
        self.zoom_level = zoom_level

class tracker_video_data():
    def __init__(self, filename, cap):
        self.filename = filename
        self.obj_points = []
        self.current_frame = 0
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        self.num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.total_time_in_secs = int(self.num_frames / self.fps)

    def get_object_points(self, frame):
        return self.obj_points[frame]

class video_tracker(QObject):
    FrameSignal = Signal(int)
    finished = Signal()
    stopped = Signal()
    gen_start = Signal(bool)
    gen_history = Signal(int)

    def __init__(self, filename, DEBUG, history_frames=100, dist_threshold=50, shadows=False, min_area=75, max_area=400, zoom_level=4):
        super(video_tracker, self).__init__()
        self.debug_logger = logger(DEBUG)
        self.debug_logger.print_debug_info(11, filename)

        self.data = tracker_data(history_frames, dist_threshold, shadows, min_area, max_area, zoom_level)

        self.cap = cv2.VideoCapture(filename)
        self.obj_detector = cv2.createBackgroundSubtractorMOG2(history=self.data.history_frames, varThreshold=self.data.dist_threshold, detectShadows=self.data.shadows)
        self.render = render(self.data.zoom_level)

        self.video_data = tracker_video_data(filename, self.cap)
        self.frame = None
        self.frame_cnt = None
        self.mask = None
        self.final = None

        self.running = False

    def generate_frames(self):
        self.debug_logger.print_debug_info(5, self.video_data.current_frame)

        #Get frame from file
        self.debug_logger.print_debug_info(6, self.video_data.current_frame)
        ret, frame = self.cap.read()

        self.debug_logger.print_debug_info(7, self.video_data.current_frame)
        mask = self.obj_detector.apply(frame)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY, (100, 100))
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        frame_cnt = copy.deepcopy(frame)

        if len(self.video_data.obj_points) < self.video_data.current_frame:
            self.fill_empty(self.video_data.current_frame)

        self.video_data.obj_points.append([])

        #Apply the contours to the frame
        self.debug_logger.print_debug_info(8, self.video_data.current_frame)
        for cnt in contours:
            area = cv2.contourArea(cnt)

            if(area > self.data.min_area and area < self.data.max_area):
                x, y, w, h = cv2.boundingRect(cnt)
                self.video_data.obj_points[self.video_data.current_frame].append([x, y, w, h])
                cv2.rectangle(frame_cnt, (x, y), (x + w, y + h), (0, 255, 0), 3)

        #Set frames
        self.frame = frame
        self.frame_cnt = frame_cnt
        self.mask = mask

        #Render final frame if possible
        if(self.video_data.obj_points[self.video_data.current_frame] != []):
            self.debug_logger.print_debug_info(9, self.video_data.current_frame)
            final = render.gen(self.render, frame, self.video_data.obj_points[self.video_data.current_frame][0][0], self.video_data.obj_points[self.video_data.current_frame][0][1])
            self.final = final

        #Update UI and prepare for next frames
        self.debug_logger.print_debug_info(10, self.video_data.current_frame)
        self.FrameSignal.emit(self.video_data.current_frame)
        self.video_data.current_frame += 1

    def destroy(self):
        self.debug_logger.print_debug_info(20)
        self.cap.release()
        self.finished.emit()

    def generate_all_frames(self):
        self.debug_logger.print_debug_info(4)
        while self.running:
            self.generate_frames()

    def receive_signal(self, gen_all):
        self.debug_logger.print_debug_info(21)
        self.running = True
        if gen_all:
            self.generate_all_frames()
        else:
            self.generate_frames()

        self.running = False
        self.debug_logger.print_debug_info(14)
        self.stopped.emit()

    def render_history(self, end_frame):
        if end_frame < self.data.history_frames:
            start_frame = 0
        else:
            start_frame = end_frame - self.data.history_frames

        #Reset obj_points
        self.video_data.obj_points = []

        #Set current frame
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        self.video_data.current_frame = start_frame
        self.running = True

        while self.video_data.current_frame < end_frame:
            self.generate_frames()

        self.running=False
        self.stopped.emit()

    def fill_empty(self, end_posiiton):
        self.debug_logger.print_debug_info(22, end_posiiton)
        i = len(self.video_data.obj_points)
        while i < end_posiiton:
            self.video_data.obj_points.append(None)
            i += 1

    def get_real_current_frame(self):
        return self.cap.get(cv2.CAP_PROP_POS_FRAMES)

    def update_zoom_level(self, zoom):
        self.data.zoom_level = zoom
        self.render.zoom_level = zoom