import cv2
import sys
import threading
import time
import numpy as np
import pandas as pd
import pickle

start_points = []
end_points = []
    
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False
              
        # vsC
        self.capture = cv2.VideoCapture(URL)
 
    def start(self):
        # {ilAdaemon=True |HDC
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()
 
    def stop(self):
        # Oon]pLj}C
        self.isstop = True
        print('ipcam stopped!')
 
    def getframe(self):
        # nvAA^svC
        return self.Frame
      
    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()
      
        self.capture.release()
        
ip = sys.argv[1]
recipe_name =  sys.argv[2]
cv2.namedWindow("capture_{}".format(ip), cv2.WINDOW_NORMAL)
cv2.resizeWindow("capture_{}".format(ip), 600, 600)
ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
ipcam.start()
time.sleep(1)
    
while True:       
    img = ipcam.getframe()
    if type(img) is not np.ndarray:
        ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
        ipcam.start()
        time.sleep(1)
        img = ipcam.getframe()
    temp_img = img.copy()
    cv2.putText(temp_img, 'please click c for capture.', (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 255, 0), 5, cv2.LINE_AA)
    cv2.imshow("capture_{}".format(ip), temp_img)
    k = cv2.waitKey(1)
    if(k == -1):
        continue
    elif(k == ord('q')):
        break
    elif(k == ord('c')):
        cv2.imwrite("{}/{}.jpg".format(recipe_name, ip), img)
        break
    time.sleep(1)
