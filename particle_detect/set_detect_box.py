import cv2
import pickle
import numpy as np

def draw_circle(event, x, y, flags, param):
    global contour
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(temp_image, (x, y), 5, (0, 0, 255), -1)
        contour.append(np.array((x, y)))


cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', draw_circle)

image = cv2.imread("stage.jpg")
temp_image = image.copy()


contours = []
contour = []
while True:
    cv2.imshow('image', temp_image)
    k = cv2.waitKey(1)
    if(k == -1):
        pass
    elif(k == ord("c") or k == ord("C")):
        contours.append(np.array(contour.copy()))
        contour = []
        temp_image = image.copy()
        for cnt in contours:
            cv2.line(temp_image, tuple(cnt[0]), tuple(cnt[1]), (0, 0, 255), 5)
            cv2.line(temp_image, tuple(cnt[1]), tuple(cnt[2]), (0, 0, 255), 5)
            cv2.line(temp_image, tuple(cnt[2]), tuple(cnt[3]), (0, 0, 255), 5)
            cv2.line(temp_image, tuple(cnt[3]), tuple(cnt[0]), (0, 0, 255), 5)
    elif(k == ord("q") or k == ord("Q")):
        if(len(contour) == 4):
            contours.append(np.array(contour.copy()))
        break
cv2.destroyAllWindows()
pickle.dump(np.array(contours), open("contours.pickle", "wb"))
