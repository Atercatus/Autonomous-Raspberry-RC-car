import cv2
import os
import numpy as np
from datetime import datetime

class Camera:
    def __init__(self):
        self.left_video_capture = cv2.VideoCapture(0)
        self.middle_video_capture = cv2.VideoCapture(2) 
<<<<<<< HEAD:Camera.py
        self.right_video_capture = cv2.VideoCapture(1) 
=======
        self.right_video_capture = cv2.VideoCapture(3) 
>>>>>>> feature/autonomous_driving:behavior_cloning/Camera.py
        self.path = os.path.join(os.getcwd(), "images")
   
    def oneshot(self):
        ret, frame = self.middle_video_capture.read()
        assert ret == True, "Video Capture Fail"
        return frame

    def shot(self):
        ret1, frame1 = self.left_video_capture.read() 
        ret2, frame2 = self.middle_video_capture.read() 
        ret3, frame3 = self.right_video_capture.read() 
        assert ret1 == True , "Video1 Capture Fail"
        assert ret2 == True , "Video2 Capture Fail"
        assert ret3 == True , "Video3 Capture Fail"
        frames = [frame1, frame2, frame3]
        
        return frames

    def record(self, frames):
        now = datetime.now()
        suffix = "-" + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + str(now.microsecond) +  ".bmp"
        
        left_img_filename = os.path.join(self.path, "left" + suffix)
        mid_img_filename = os.path.join(self.path, "mid" + suffix)
        right_img_filename = os.path.join(self.path, "right" + suffix)

        #left_img_filename = self.path, "left" + suffix
        #mid_img_filename = self.path, "mid" + suffix
        #right_img_filename = self.path, "right" + suffix


        cv2.imwrite(left_img_filename, frames[0])
        cv2.imwrite(mid_img_filename, frames[1])
        cv2.imwrite(right_img_filename, frames[2])

        image_pathes = [left_img_filename, mid_img_filename, right_img_filename]
        return image_pathes


if __name__ == "__main__":
    print("Record one shot image")
    camera = Camera()
    paths = camera.record(camera.shot())
    print(paths)
