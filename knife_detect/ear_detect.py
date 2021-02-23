import cv2
import pickle
import numpy as np

image = cv2.imread("test.png")
result = image.copy()
cv2.namedWindow("detect", cv2.WINDOW_NORMAL)
cv2.namedWindow("roi", cv2.WINDOW_NORMAL)
contours = pickle.load(open("contours.pickle", "rb"))

kernel_size = 9
sigma = 0
low_threshold = 30
high_threshold = 90
blur = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, low_threshold, high_threshold)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

mask = np.zeros_like(closing)
out = np.zeros_like(closing)
for cnt in contours:
    cv2.fillPoly(mask, pts=[cnt], color=(255, 255, 255))
out[mask == 255] = closing[mask == 255]
cnts, hierarchy = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in cnts:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)




mask = np.zeros_like(image)
roi = np.zeros_like(image)
for cnt in contours:
    cv2.fillPoly(mask, pts=[cnt], color=(255, 255, 255))
roi[mask == 255] = image[mask == 255]

cv2.imshow('detect', result)
cv2.imshow('roi', roi)
cv2.waitKey(0)