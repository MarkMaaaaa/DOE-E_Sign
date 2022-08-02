import numpy as np
import cv2 as cv


# Read image
image= cv.imread("data/images/panel.jpg")

# Denoise image
blur = cv.GaussianBlur(image, (5,5), 0)

# Gray scale
grayImage = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

# Binary image
lower_bound = np.array([0,0,10])
upper_bound = np.array([255,255,195])
binary = cv.inRange(blur, lower_bound, upper_bound)
cv.imshow('binary', binary)

# Kernel
kernel = np.ones((3, 3), np.uint8)

# Erosion and dialation
mask = cv.erode(binary, kernel, iterations=6)
mask = cv.dilate(mask, kernel, iterations=3)
cv.imshow('mask', mask)

# Inverse Binary
mask = np.invert(mask)
cv.imshow('invers mask', mask)

# Find contours
contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# contours = sorted(contours, key=lambda x:cv.boundingRect(x)[0])

cv.drawContours(image, contours, contourIdx=-1, color=(255, 0, 0), thickness=3)
print(len(contours))

# Show result
cv.imshow("preprocessed", image)
# cv.imwrite("output.jpg", image)
cv.waitKey(0)