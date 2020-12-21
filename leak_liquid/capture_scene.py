import cv2

vc = cv2.VideoCapture("Ch13-20201216-095302.mp4")
vido_width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
vido_height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
vc.set(cv2.CAP_PROP_POS_MSEC,69000)
rval, frame = vc.read()
if(rval):
    cv2.imwrite("stage_0.jpg", frame)