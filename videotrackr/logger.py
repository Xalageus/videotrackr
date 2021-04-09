from videotrackr import video
from videotrackr.__init__ import __version__ as version
from videotrackr.__init__ import __name__ as videotrackr_name

class logger():
    def __init__(self, debug):
        self.DEBUG = debug

    def print_debug_info(self, msg, arg=""):
        if(self.DEBUG):
            if msg == 0:
                print("Starting up " + videotrackr_name + " " + version + " ...")
            if msg == 1:
                print("Current GUI state " + str(arg) + " (" + str(arg.value) + ")")
            if msg == 2:
                self.print_video_data(arg)
            if msg == 3:
                self.print_tracker_data(arg)
            if msg == 4:
                print("Start generate_all_frames()")
            if msg == 5:
                print("Generating frames at " + str(arg))
            if msg == 6:
                print("Getting frame from file at " + str(arg))
            if msg == 7:
                print("Generating mask at " + str(arg))
            if msg == 8:
                print("Apply contours at " + str(arg))
            if msg == 9:
                print("Rendering final frame at " + str(arg))
            if msg == 10:
                print("Updating GUI at " + str(arg))
            if msg == 11:
                print("Initalizing video tracker with file " + str(arg))
            if msg == 12:
                print("Receiving frames at " + str(arg)) 
            if msg == 13:
                print("Preparing to destroy tracker...")     
            if msg == 14:
                print("Tracker stopped")
            if msg == 15:
                print("Tracker destroyed successfully")
            if msg == 16:
                print("Updating current_frame with value " + str(arg))
            if msg == 18:
                print("Starting tracker thread")
            if msg == 19:
                print("Current tracker thread: " + str(arg))
            if msg == 20:
                print("Releasing OpenCV cap...")
            if msg == 21:
                print("Received tracker start")
            if msg == 22:
                print("Filling entries in list with None until " + str(arg))
            if msg == 23:
                print("Real current frame: " + str(arg))
            if msg == 24:
                print("Recived property row " + str(arg))
            
    def print_video_data(self, video_data):
        print("filename=" + video_data.filename)
        print("length of obj_points=" + str(len(video_data.obj_points)))
        print("current_frame=" + str(video_data.current_frame))
        print("fps=" + str(video_data.fps))
        print("num_frames=" + str(video_data.num_frames))
        print("total_time_in_secs=" + str(video_data.total_time_in_secs))

    def print_tracker_data(self, data):
        print("history_frames=" + str(data.history_frames))
        print("dist_threshold=" + str(data.dist_threshold))
        print("shadows=" + str(data.shadows))
        print("min_area=" + str(data.min_area))
        print("max_area=" + str(data.max_area))
        print("zoom_level=" + str(data.zoom_level))