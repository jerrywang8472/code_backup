# import the necessary packages
from skimage.metrics import structural_similarity
import cv2
import pickle
import numpy as np

contours = pickle.load(open("contours.pickle", "rb"))

cv2.namedWindow("A", cv2.WINDOW_NORMAL)
cv2.namedWindow("B", cv2.WINDOW_NORMAL)
cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
# load the two input images
imageA = cv2.imread("stage_0.jpg")
maskA = np.zeros_like(imageA)
outA = np.zeros_like(imageA)
for cnt in contours:
    cv2.fillPoly(maskA, pts=[cnt], color=(255, 255, 255))

outA[maskA == 255] = imageA[maskA == 255]


imageB = cv2.imread("stage_2.jpg")
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
print("SSIM: {}".format(score))
# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# loop over the contours
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)


# show the output images
cv2.imshow("A", imageA)
cv2.imshow("B", imageB)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)