import cv2
import numpy as np

class render:
    def __init__(self, zoom_level):
        self.zoom_level = zoom_level

    def gen(self, frame, x, y):
        height, width, _ = frame.shape

        #Translate frame
        x_trans = (-x) + width / 2
        y_trans = (-y) + height / 2

        tm = np.float32([
                [1, 0, int(x_trans)],
                [0, 1, int(y_trans)]
            ])
        
        frame = cv2.warpAffine(frame, tm, (width, height))

        #Scale frame
        frame = cv2.resize(frame, (width * self.zoom_level, height * self.zoom_level), interpolation=cv2.INTER_LINEAR)

        #Crop frame
        crop_width = width
        crop_height = height
        mid_x = int(frame.shape[1] / 2)
        mid_y = int(frame.shape[0] / 2)
        w2 = int(crop_width / 2)
        h2 = int(crop_height / 2)

        #Return a contiguous frame
        return frame[mid_y - h2:mid_y + h2, mid_x - w2:mid_x + w2].copy(order='C')