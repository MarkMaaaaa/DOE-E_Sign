import re
import numpy as np
import cv2 as cv

min_side = 15
max_side = 25
min_area = min_side**2
max_area = max_side**2
min_perimeter = 4*min_side
max_perimeter = 4*max_side


# Read image
image = cv.imread("data/images/panel.jpg")
# image = cv.imread('data/images/panel_circ.jpg')

# Denoise image
blur = cv.GaussianBlur(image, (5,5), 0)

# Gray scale
grayImage = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

# Binary image
lower_bound = np.array([0,0,10])
upper_bound = np.array([255,255,195])
binary = cv.inRange(blur, lower_bound, upper_bound)
# cv.imshow('binary', binary)

# Kernel
kernel = np.ones((3, 3), np.uint8)

# Erosion and dialation
mask = cv.erode(binary, kernel, iterations=6)
mask = cv.dilate(mask, kernel, iterations=3)
# cv.imshow('mask', mask)

# Inverse Binary
mask = np.invert(mask)
# cv.imshow('invers mask', mask)

# Find contours
contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=lambda x:cv.boundingRect(x)[0] + cv.boundingRect(x)[1] * image.shape[1])
# print(contours)

# Filter contours 
for i, c in enumerate(contours):
     # Filter by Counter Area
    areaContour=cv.contourArea(c)   # Calculate area of contour
    if areaContour < min_area or areaContour > max_area:
        contours.pop(i)
        continue

    # Filter by Counter Perimeter
    perimeter = cv.arcLength(c, True)
    if perimeter < min_perimeter or perimeter > max_perimeter:
        contours.pop(i)
        continue

    # Filter by Contour Shape
    approx = cv.approxPolyDP(c, 0.03*perimeter, True)
    if not len(approx) == 4:
        contours.pop(i)
        continue

# Draw contours
cv.drawContours(image, contours, contourIdx=-1, color=(125, 125, 0), thickness=2)

# Label contours
for i, c in enumerate(contours):
    rect = cv.minAreaRect(c)
    print(i+1, rect)
    M = cv.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv.putText(image, text=str(i+1), org=(cx,cy),
            fontFace= cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0,0,255),
            thickness=2, lineType=cv.LINE_AA)

# # Minimum and Maximum size of side
# size = []
# for i, c in enumerate(contours):
#     rect = cv.minAreaRect(c)[1]
#     size.append(rect)
# min_size = min(size)
# max_size = max(size)
# print(min_size, max_size)

panel = np.zeros((8,32))

# # Positiong
# first_bit = cv.minAreaRect(contours[0])[0]
# # print(first_bit)
# for i, c in enumerate(contours):
#     if i >= len(contours)-1:
#         break
#     centroid_curr = cv.minAreaRect(c)[0]
#     centroid_next = cv.minAreaRect(contours[i+1])[0]
#     print(centroid_curr)
#     # print(centroid_next)
#     if abs(centroid_curr[0] - first_bit[0]) > 10:
#         print("___________________________________________________________")
#         first_bit = centroid_curr
#         continue
 
# Show result
cv.imshow("preprocessed", image)
# cv.imwrite("filter_by_area.jpg", image)
cv.waitKey(0)