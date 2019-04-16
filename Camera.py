import cv2
import os
import numpy as np

class Camera:
    path = "C:\\공부자료\\DataSet" #경로지정
    imageList = [None,None,None] # 이미지 리스트
    left_video_capture = None # 왼쪽 카메라
    middle_video_capture = None # 중간 카메라
    right_video_capture = None # 오른쪽 카메라
    def __init__(self):#생성자
        self.left_video_capture = cv2.VideoCapture(1) #1번연결
        self.middle_video_capture = cv2.VideoCapture(2) #2번연결
        self.right_video_capture = cv2.VideoCapture(3) #3번연결
    def get_image(self):
        ret1 , frame1 = self.left_video_capture.read() #순간사진찍기
        ret2 , frame2 = self.middle_video_capture.read() #순간사진찍기
        ret3 , frame3 = self.right_video_capture.read() #순간사진찍기
        self.imageList[0] = frame1 # 배열에 담기
        self.imageList[1] = frame2
        self.imageList[2] = frame3
        self.left_video_capture.release()
        self.middle_video_capture.release()
        self.right_video_capture.release()
        return self.imageList
    def record(self):
        ret1 , frame1 = self.left_video_capture.read() #순간사진찍기
        ret2 , frame2 = self.middle_video_capture.read() #순간사진찍기
        ret3 , frame3 = self.right_video_capture.read() #순간사진찍기
        cv2.imwrite(os.path.join(self.path,'leftCamera.bmp'),frame1)
        cv2.imwrite(os.path.join(self.path,'middleCamera.bmp'),frame2)
        cv2.imwrite(os.path.join(self.path,'rightCamera.bmp'),frame3)

controlCamera = Camera()
controlCamera.record()
imageList = controlCamera.get_image()
cv2.imshow("leftCamera",imageList[0])
cv2.imshow("middleCamera",imageList[1])
cv2.imshow("rightCamera",imageList[2])
cv2.waitKey(0)
cv2.destroyAllWindows()
