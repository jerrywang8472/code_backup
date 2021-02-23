import cv2
import pickle
import numpy as np
contours = pickle.load(open("contours.pickle", "rb"))
cv2.namedWindow("image", cv2.WINDOW_NORMAL)

image = cv2.imread("test.png")
mask = np.zeros_like(image)
out = np.zeros_like(image)
for cnt in contours:
    cv2.fillPoly(mask, pts=[cnt], color=(255, 255, 255))

out[mask == 255] = image[mask == 255]

cv2.imshow("image", out)
cv2.waitKey(0)