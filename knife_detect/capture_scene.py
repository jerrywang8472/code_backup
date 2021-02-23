import cv2

vc = cv2.VideoCapture("163124-av-1.avi")
vido_width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
vido_height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
vc.set(cv2.CAP_PROP_POS_MSEC, 3000)
rval, frame = vc.read()
if(rval):
    cv2.imwrite("test.jpg", frame)