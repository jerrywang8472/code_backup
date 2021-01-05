import cv2
import sys
import threading
import time
import numpy as np
from datetime import datetime
from skimage.metrics import structural_similarity
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
contours = pickle.load(open("{}/{}.pickle".format(recipe_name, ip), "rb"))

save_disk = "F:\\"

if os.path.isdir(os.path.join(save_disk, ip, "ok")):
    pass
else:
    os.makedirs(os.path.join(save_disk, ip, "ok"))
    
if os.path.isdir(os.path.join(save_disk, ip, "ng")):
    pass
else:
    os.makedirs(os.path.join(save_disk, ip, "ng"))

# window_position = {"192.168.1.205":(0, 0), "192.168.1.236":(300, 0), "192.168.1.219":(600, 0), "192.168.1.198":(900, 0),
#                    "192.168.1.194":(0, 300), "192.168.1.151":(300, 300), "192.168.1.247":(600, 300), "192.168.1.110":(900, 300),
#                    "192.168.1.187":(0, 600), "192.168.1.51":(300, 600), "192.168.1.33":(600, 600), "192.168.1.211":(900, 600)}

cv2.namedWindow("leak_{}".format(ip), cv2.WINDOW_NORMAL)
# cv2.moveWindow("leak_{}".format(ip), window_position[ip][0], window_position[ip][1])
# cv2.resizeWindow(leak_{}".format(ip), 300, 300)
ipcam = ipcamCapture("rtsp://admin:123456@" + ip + "/video1")
ipcam.start()
time.sleep(3)

is_complete_cam_ip = ["192.168.1.151"]
signal_times = dict()
for complete_ip in is_complete_cam_ip:
    signal_times[complete_ip] = str(time.ctime(os.path.getmtime("../cut_detect/{}/{}_sigenl.txt".format(recipe_name, complete_ip))))

# while True:
#     frame = ipcam.getframe()
#     cv2.imshow(ip, frame)
#     k = cv2.waitKey(1)
#     if(k == -1):
#         pass
#     else:
#         break

while True:
    lc_found_list = []
    for complete_ip in is_complete_cam_ip:
        if(signal_times[complete_ip] != str(time.ctime(os.path.getmtime("../cut_detect/{}/{}_sigenl.txt".format(recipe_name, complete_ip))))):
            signal_times[complete_ip] = str(time.ctime(os.path.getmtime("../cut_detect/{}/{}_sigenl.txt".format(recipe_name, complete_ip))))
            lc_found_list.append(True)
        else:
            lc_found_list.append(False)
            
    if(any(lc_found_list)):
        print("LC complete!", flush=True)
        time.sleep(4)
        pass
    else:
        print("waiting for LC complete...", flush=True)
        time.sleep(1)
        continue

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
    
    imageA = img.copy()
    maskA = np.zeros_like(imageA)
    outA = np.zeros_like(imageA)
    for cnt in contours:
        cv2.fillPoly(maskA, pts=[cnt], color=(255, 255, 255))
    
    outA[maskA == 255] = imageA[maskA == 255]
    
    
    imageB = cv2.imread("{}/{}.jpg".format(recipe_name, ip))
    maskB = np.zeros_like(imageB)
    outB = np.zeros_like(imageB)
    for cnt in contours:
        cv2.fillPoly(maskB, pts=[cnt], color=(255, 255, 255))
    
    outB[maskB == 255] = imageB[maskB == 255]
    
    # convert the images to grayscale
    grayA = cv2.cvtColor(outA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(outB, cv2.COLOR_BGR2GRAY)
    
    # stage 
    kernel_size = 15
    grayA = cv2.GaussianBlur(grayA, (kernel_size, kernel_size), 0)
    grayB = cv2.GaussianBlur(grayB, (kernel_size, kernel_size), 0)
    
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    # print("SSIM: {}".format(score))
    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # loop over the contours
    result = imageA.copy()
    is_ok = True
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)
        is_ok = False
    
    datetime_dt = datetime.today()
    timestep = "{}_{}_{}_{}_{}_{}".format(datetime_dt.year, datetime_dt.month, datetime_dt.day, 
                                          datetime_dt.hour, datetime_dt.minute, datetime_dt.second)

    if(is_ok):
        cv2.putText(result, 'OK', (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 255, 0), 5, cv2.LINE_AA)
        os.makedirs(os.path.join(save_disk, ip, "ok", timestep))
    else:
        cv2.putText(result, 'NG', (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 5, (0, 0, 255), 5, cv2.LINE_AA)
        os.makedirs(os.path.join(save_disk, ip, "ng", timestep)) 
    
    cv2.imshow("leak_{}".format(ip), result)
    
    if(is_ok):
        cv2.imwrite(os.path.join(save_disk, ip, "ok", timestep,"origin.jpg"), imageA)
    else:
        cv2.imwrite(os.path.join(save_disk, ip, "ng", timestep,"origin.jpg"), imageA)
        cv2.imwrite(os.path.join(save_disk, ip, "ng", timestep,"result.jpg"), result)
    
    # cv2.imshow("output", dilation)
    # cv2.imshow("rect_image", rect_image)
    k = cv2.waitKey(1)
    if(k == -1):
        time.sleep(30)
    elif(k == ord('q')):
        break

cv2.destroyAllWindows()
ipcam.stop()    
