# import the necessary packages
import cv2
import pickle
import numpy as np

top_y = 1650
buttom_y = 1983
contours = pickle.load(open("contours.pickle", "rb"))

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("Particle", cv2.WINDOW_NORMAL)

frame_period = 1
kernel_size = 11
sigma = 0
cap = cv2.VideoCapture('hue165.avi')
while(True):
    ret, frame = cap.read()

    blur = cv2.GaussianBlur(frame, (kernel_size, kernel_size), sigma)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    thresh = cv2.adaptiveThreshold(v, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    # ret, thresh = cv2.threshold(v, 150, 255, cv2.THRESH_BINARY)
    mask = np.zeros_like(thresh)
    out = np.zeros_like(thresh)
    for cnt in contours:
        cv2.fillPoly(mask, pts=[cnt], color=(255, 255, 255))
    out[mask == 255] = thresh[mask == 255]
    cnts, hierarchy = cv2.findContours(out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow('Frame', frame[top_y:buttom_y, :, :])
    cv2.imshow("Particle", out[top_y:buttom_y, :])
    if cv2.waitKey(frame_period) & 0xFF == ord('q'):
        break