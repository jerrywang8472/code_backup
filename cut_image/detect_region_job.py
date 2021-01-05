import cv2
import sys
import threading
import time
import numpy as np
from datetime import datetime
import pickle
import os
import gc
    
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False
              
        # vsC
        self.capture = cv2.VideoCapture(URL)
 
    def start(self):
        # {ilAdaemon=True |HDC
        print('ipcam started!', flush=True)
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()
 
    def stop(self):
        # Oon]pLj}C
        self.isstop = True
        print('ipcam stopped!', flush=True)
 
    def getframe(self):
        # nvAA^svC
        return self.Frame
      
    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()
      
        self.capture.release()


ip = sys.argv[1]
recipe_name =  sys.argv[2]
detect_region_dilation = int(sys.argv[3])
detect_region_low_threshold = int(sys.argv[4])
detect_region_high_threshold = int(sys.argv[5])
complete_region_dilation = int(sys.argv[6])
complete_region_low_threshold = int(sys.argv[7])
complete_region_high_threshold = int(sys.argv[8])
complete_ratio = float(sys.argv[9])
second_detect_region_dilation = int(sys.argv[10])
second_detect_region_low_threshold = int(sys.argv[11])
second_detect_region_high_threshold = int(sys.argv[12])

save_disk = "E:\\"
start_points = None
end_points = None

if os.path.isdir(os.path.join(save_disk, ip, "ok")):
    pass
else:
    os.makedirs(os.path.join(save_disk, ip, "ok"))
    
if os.path.isdir(os.path.join(save_disk, ip, "ng")):
    pass
else:
    os.makedirs(os.path.join(save_disk, ip, "ng"))

window_position = {"192.168.1.205":(0, 0), "192.168.1.236":(300, 0), "192.168.1.219":(600, 0), "192.168.1.198":(900, 0),
                   "192.168.1.194":(0, 300), "192.168.1.151":(300, 300), "192.168.1.247":(600, 300), "192.168.1.130":(900, 300),
                   "192.168.1.187":(0, 600), "192.168.1.51":(300, 600), "192.168.1.33":(600, 600), "192.168.1.211":(900, 600)}

start_points = pickle.load(open("{}/{}_start_points.pickle".format(recipe_name, ip), "rb"))
end_points = pickle.load(open("{}/{}_end_points.pickle".format(recipe_name, ip), "rb"))
is_complete_cam_ip = ["192.168.1.151"]
if(ip in is_complete_cam_ip):
    file = open("{}/{}_sigenl.txt".format(recipe_name, ip), "w")
    file.write(str(datetime.today()))
    file.close()

cv2.namedWindow(ip, cv2.WINDOW_NORMAL)
cv2.moveWindow(ip, window_position[ip][0], window_position[ip][1])
cv2.resizeWindow(ip, 300, 300)
ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
ipcam.start()
time.sleep(3)
signal_times = dict()
for complete_ip in is_complete_cam_ip:
    signal_times[complete_ip] = str(time.ctime(os.path.getmtime("{}/{}_sigenl.txt".format(recipe_name, complete_ip))))
# while True:
#     frame = ipcam.getframe()
#     cv2.imshow(ip, frame)
#     k = cv2.waitKey(1)
#     if(k == -1):
#         pass
#     else:
#         break
while True:
    gc.collect()
    img = ipcam.getframe()
    # double check
    if type(img) is not np.ndarray:
        print("{} second try...".format(ip), flush=True)
        ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
        ipcam.start()
        time.sleep(1)
        img = ipcam.getframe()
        if type(img) is not np.ndarray:
            print("{} third try...".format(ip), flush=True)
            ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
            ipcam.start()
            time.sleep(1)
            img = ipcam.getframe()
            if type(img) is not np.ndarray:
                print("{} failed...".format(ip), flush=True)
                break
        
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]

    lc_found = False
    if(ip in is_complete_cam_ip):
        complete_start_points = pickle.load(open("{}/{}_complete_start_points.pickle".format(recipe_name, ip), "rb"))
        complete_end_points = pickle.load(open("{}/{}_complete_end_points.pickle".format(recipe_name, ip), "rb"))
        for i in range(len(complete_start_points)):
            cut = v[complete_start_points[i][1]:complete_end_points[i][1], complete_start_points[i][0]:complete_end_points[i][0]]
            
            kernel_size = 15
            blur = cv2.GaussianBlur(cut, (kernel_size, kernel_size), 0)
            
            low_threshold = complete_region_low_threshold
            high_threshold = complete_region_high_threshold
            masked_edges = cv2.Canny(blur, low_threshold, high_threshold)
            
            kernel = np.ones((3, 3), np.uint8)
            dilation = cv2.dilate(masked_edges, kernel, iterations = complete_region_dilation)    
            total = np.sum(np.ones_like(dilation) * 255)
            print("total: {}  region: {}".format(total, np.sum(dilation)), flush=True)
            if(np.sum(dilation) > total * complete_ratio):
                lc_found = True
                break
    
        if(lc_found):
            file = open("{}/{}_sigenl.txt".format(recipe_name, ip), "w")
            file.write(str(datetime.today()))
            file.close()
    
    lc_found_list = []
    for complete_ip in is_complete_cam_ip:
        if(signal_times[complete_ip] != str(time.ctime(os.path.getmtime("{}/{}_sigenl.txt".format(recipe_name, complete_ip))))):
            signal_times[complete_ip] = str(time.ctime(os.path.getmtime("{}/{}_sigenl.txt".format(recipe_name, complete_ip))))
            lc_found_list.append(True)
        else:
            lc_found_list.append(False)
            
    if(any(lc_found_list)):
        print("LC complete!", flush=True)
        pass
    else:
        print("waiting for LC complete...", flush=True)
        time.sleep(1)
        continue
       
    dilation_check_iamges = []
    gray_check_iamges = []
    bounding_check_iamges = []
    isok_list = []    
    for i in range(len(start_points)):
        isok_list.append(False)
        cut = v[start_points[i][1]:end_points[i][1], start_points[i][0]:end_points[i][0]]
        
        kernel_size = 15
        blur = cv2.GaussianBlur(cut, (kernel_size, kernel_size), 0)
        
        low_threshold = detect_region_low_threshold
        high_threshold = detect_region_high_threshold
        masked_edges = cv2.Canny(blur, low_threshold, high_threshold)
        
        kernel = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(masked_edges, kernel, iterations = detect_region_dilation)
        #opening = cv2.morphologyEx(masked_edges, cv2.MORPH_OPEN, kernel, iterations = 1)
        
        rect_image = np.zeros((masked_edges.shape[0], masked_edges.shape[1], 3))
        
        countours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
        width_threshold = 70
        ng_threshold = 10
        for countour in countours: 
            x, y, w, h = cv2.boundingRect(countour)
            if(w > width_threshold):
                if(w > end_points[i][0] - start_points[i][0] - ng_threshold):
                    cv2.rectangle(rect_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    isok_list[i] = True
                else:
                    cv2.rectangle(rect_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        dilation_check_iamges.append(dilation)
        gray_check_iamges.append(cut)
        bounding_check_iamges.append(rect_image)
    
    datetime_dt = datetime.today()
    timestep = "{}_{}_{}_{}_{}_{}".format(datetime_dt.year, datetime_dt.month, datetime_dt.day, 
                                          datetime_dt.hour, datetime_dt.minute, datetime_dt.second)
    
    is_ok = None
    is_first_ok = False
    if(all(isok_list)):
        is_ok = True
        is_first_ok = True
    else:
        isok_list = []    
        for i in range(len(start_points)):
            isok_list.append(False)   
            cut = v[start_points[i][1]:end_points[i][1], start_points[i][0]:end_points[i][0]]           
            
            kernel_size = 15
            blur = cv2.GaussianBlur(cut, (kernel_size, kernel_size), 0)
            
            low_threshold = second_detect_region_low_threshold
            high_threshold = second_detect_region_high_threshold
            masked_edges = cv2.Canny(blur, low_threshold, high_threshold)
            
            kernel = np.ones((3, 3), np.uint8)
            dilation = cv2.dilate(masked_edges, kernel, iterations = second_detect_region_dilation)
            #opening = cv2.morphologyEx(masked_edges, cv2.MORPH_OPEN, kernel, iterations = 1)
            
            rect_image = np.zeros((masked_edges.shape[0], masked_edges.shape[1], 3))
            
            countours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for countour in countours: 
                x, y, w, h = cv2.boundingRect(countour)
                if(w > width_threshold):
                    if(w > end_points[i][0] - start_points[i][0] - ng_threshold):
                        isok_list[i] = True  
        if(all(isok_list)):
            is_ok = True
        else:
            is_ok = False
    
    if(is_ok):
        cv2.putText(img, 'OK', (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 255, 0), 5, cv2.LINE_AA)
        os.makedirs(os.path.join(save_disk, ip, "ok", timestep))
    else:
        cv2.putText(img, 'NG', (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 0, 255), 5, cv2.LINE_AA)
        os.makedirs(os.path.join(save_disk, ip, "ng", timestep))
        
        for i in range(len(dilation_check_iamges)):
            dilation_image_name = os.path.join(save_disk, ip, "ng", timestep, "dilation_{}.jpg".format(i))
            cv2.imwrite(dilation_image_name, dilation_check_iamges[i])
            gray_image_name = os.path.join(save_disk, ip, "ng", timestep, "gray_{}.jpg".format(i))
            cv2.imwrite(gray_image_name, gray_check_iamges[i])
            bounding_image_name = os.path.join(save_disk, ip, "ng", timestep, "bounding_{}.jpg".format(i))
            cv2.imwrite(bounding_image_name, bounding_check_iamges[i])
    
    
    for i in range(len(start_points)): 
        cv2.rectangle(img, tuple(start_points[i]), tuple(end_points[i]), (0, 0, 255), 5)
    if(ip in is_complete_cam_ip):
        for i in range(len(complete_start_points)): 
            cv2.rectangle(img, tuple(complete_start_points[i]), tuple(complete_end_points[i]), (0, 255, 0), 5)
    cv2.imshow(ip, img)
    
    if(is_ok):
        if(is_first_ok):
            cv2.imwrite(os.path.join(save_disk, ip, "ok", timestep,"origin_ok1.jpg"), img)
        else:
            cv2.imwrite(os.path.join(save_disk, ip, "ok", timestep,"origin_ok2.jpg"), img)
    else:
        cv2.imwrite(os.path.join(save_disk, ip, "ng", timestep,"origin.jpg"), img)
    
    # cv2.imshow("output", dilation)
    # cv2.imshow("rect_image", rect_image)
    k = cv2.waitKey(1)
    if(k == -1):
        time.sleep(30)
    elif(k == ord('q')):
        break

cv2.destroyAllWindows()
ipcam.stop()    
