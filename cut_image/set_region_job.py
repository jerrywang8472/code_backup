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
        
def draw_rectangle(event, x, y, flags, param):
    global start_points, end_points, temp_img
    if(event == cv2.EVENT_LBUTTONDOWN):
        if(len(start_points) == len(end_points)):
            start_points.append(np.array([x, y]))
            temp_img = img.copy()
            for i in range(len(end_points)):
                cv2.rectangle(temp_img, tuple(start_points[i]), tuple(end_points[i]), (0,0,255), 3)
            cv2.circle(temp_img, tuple(start_points[-1]), 11, (0, 0, 255), -1)
            cv2.putText(temp_img, 'please click end point', (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 255, 0), 5, cv2.LINE_AA)
        else:
            temp_img = img.copy()
            for i in range(len(end_points)):
                cv2.rectangle(temp_img, tuple(start_points[i]), tuple(end_points[i]), (0,0,255), 3)
            end_points.append(np.array([x, y]))
            cv2.circle(temp_img, tuple(start_points[-1]), 11, (0, 0, 255), -1)
            cv2.circle(temp_img, tuple(end_points[-1]), 11, (0, 0, 255), -1)
            cv2.putText(temp_img, 'click "q" for quit. click "c" for continue.', (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 255, 0), 5, cv2.LINE_AA)
        
ip = sys.argv[1]
recipe_name =  sys.argv[2]
cv2.namedWindow("set_{}".format(ip), cv2.WINDOW_NORMAL)
ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
ipcam.start()
time.sleep(1)

terminate_loop = True
img = ipcam.getframe()
if type(img) is not np.ndarray:
    ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
    ipcam.start()
    time.sleep(1)
    img = ipcam.getframe()
    
while terminate_loop:       
    temp_img = img.copy()
    for i in range(len(end_points)):
        cv2.rectangle(temp_img, tuple(start_points[i]), tuple(end_points[i]), (0,0,255), 3)
    cv2.putText(temp_img, 'please click start point', (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 255, 0), 5, cv2.LINE_AA)
    cv2.setMouseCallback("set_{}".format(ip), draw_rectangle)
    
    while True:
        cv2.imshow("set_{}".format(ip), temp_img)
        k = cv2.waitKey(1)
        if(k == -1):
            continue
        elif(k == ord('q')):
            terminate_loop = False
            break
        elif(k == ord('c')):
            break
        
if(len(start_points) == 0 or len(start_points) != len(end_points)):
    pass
else:
    pickle.dump(start_points, open("{}/{}_start_points.pickle".format(recipe_name, ip), "wb"))
    pickle.dump(end_points, open("{}/{}_end_points.pickle".format(recipe_name, ip), "wb"))