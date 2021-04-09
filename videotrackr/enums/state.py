import enum

class State(enum.Enum):
    Nothing_Loaded = 0
    Initializing = 1
    Idle = 2
    Running = 3
    Stopping = 4
    Destroying = 5
    Stopped = 6
    Preparing_History = 7
    Slider_Moved_While_Running = 8