import cv2
import sys
import threading
import time
import numpy as np
import pandas as pd
from datetime import datetime
import pickle
import os
    
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
recipe_name = sys.argv[2]
start_points = None
end_points = None
start_points = pickle.load(open("{}/{}_start_points.pickle".format(recipe_name, ip), "rb"))
end_points = pickle.load(open("{}/{}_end_points.pickle".format(recipe_name, ip), "rb"))
        
cv2.namedWindow(ip, cv2.WINDOW_NORMAL)
cv2.resizeWindow(ip, 300, 300)
ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
ipcam.start()
time.sleep(1)
while True:
    img = ipcam.getframe()
    # double check
    if type(img) is not np.ndarray:
        ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
        ipcam.start()
        time.sleep(1)
        img = ipcam.getframe()

    for i in range(len(start_points)): 
        cv2.rectangle(img, tuple(start_points[i]), tuple(end_points[i]), (0, 0, 255), 5)
    cv2.imshow(ip, img)
    k = cv2.waitKey(1)
    if(k == -1):
        pass
    elif(k == ord('q')):
        break

cv2.destroyAllWindows()
ipcam.release()    
