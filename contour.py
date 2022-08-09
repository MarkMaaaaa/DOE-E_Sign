
import numpy as np
import cv2 as cv

min_side = 15
max_side = 25
min_area = min_side**2
max_area = max_side**2
min_perimeter = 4*min_side
max_perimeter = 4*max_side


# Read image
image = cv.imread("data/images/image.jpg")


# ------------------ Preprocessing --------------------- #

# Denoise image
# Remove noises by Gaussian filter
mask = cv.GaussianBlur(image, (5,5), 0)

# Binary image
lower_bound = np.array([0,0,10])
upper_bound = np.array([255,255,195])
mask = cv.inRange(mask, lower_bound, upper_bound)

# Enhance the mask by using Morphological transfomation
# This is an operation based on the shape of an image
kernel = np.ones((3, 3), np.uint8)      # Kernel

mask = cv.erode(mask, kernel, iterations=6)     # Erosion
mask = cv.dilate(mask, kernel, iterations=3)    # Dilation
mask = np.invert(mask)                          # Inverse Binary

# ------------------ Contours --------------------- #

# Find all contours in the image based on the mask
contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Remove all contours that detect by mistake
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

# Sort contours

# TO-DO:
# This sort is not necessery, but we need to convert contours from tuple to list
# There should be a better way than sorted function
contours = sorted(contours, key=lambda x:cv.boundingRect(x)[1])         # Convert tuple to list

# Classify contours based on the row that they belong
row = 0
sorted_contours = [[], [], [], [], [], [], [], []]
cx0, cy0 = cv.minAreaRect(contours[0])[0]
for c in contours:
    cx, cy = cv.minAreaRect(c)[0]
    if abs(cy0-cy) > 5.0:
        cx0, cy0 = cx, cy
        row += 1
    sorted_contours[row].append(c)

# Sort contours in a row from left to right
i = 0
for row in sorted_contours:
    row = sorted(row, key=lambda x:cv.boundingRect(x)[0])
    for c in row:
        contours[i] = c 
        i += 1        

# Draw contours
cv.drawContours(image, contours, contourIdx=-1, color=(125, 125, 0), thickness=2)

# Label contours
for i, c in enumerate(contours):
    # Claculate the coordinates of the label
    M = cv.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    # Draw the label
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


# ------------------ Positioning --------------------- #

# Positiong
panel = np.zeros((8,32))
row, col = (0, 0)       # Panel's row and column indicator
cx0, cy0 = cv.minAreaRect(contours[0])[0]    # Left-top bit in the panel - always is on
panel[0][0] = 1
for i, c in enumerate(contours):
    if i >= len(contours)-1:
        break
    cx, cy = cv.minAreaRect(c)[0]                   # Coordination of current bit's center
    cx1, cy1 = cv.minAreaRect(contours[i+1])[0]     # Coordination of next bit's center

    if abs(cy - cy1) > 30:       # End of row
        row += 1
        col = round(abs(cx0 - cx1)/20)       # Distance between first bit of next row with the first 1bit  

    else:
        dist = round(abs(cx - cx1)/20)
        col = col+dist
    
    panel[row][col] = 1

print(panel)
    
    # if i >= len(contours)-1:
    #     break
 
# Show result
cv.imshow("preprocessed", image)
# cv.imwrite("filter_by_area.jpg", image)
cv.waitKey(0)