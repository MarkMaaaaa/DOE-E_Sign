import cv2 as cv
import numpy as np


def color_detection(source, panel_dimension=(24, 4)):
    source = str(source)
    image = cv.imread(source)
    # cv.imshow("source", image)

    # Denoise image
    # Remove noises by Gaussian filter
    # mask = cv.GaussianBlur(image, (5,5), 0)
    # cv.imshow("blur", image)

    # Convert to HSV format and color threshold
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # Binary image
    lower_bound = np.array([0,0,0])
    upper_bound = np.array([180,125,255])
    mask = cv.inRange(hsv, lower_bound, upper_bound)

    # Enhance the mask by using Morphological transfomation
    # This is an operation based on the shape of an image
    kernel = np.ones((3, 3), np.uint8)      # Kernel
    mask = cv.dilate(mask, kernel, iterations=3)    # Dilation
    mask = cv.erode(mask, kernel, iterations=5)     # Erosion
    mask = cv.dilate(mask, kernel, iterations=15)    # Dilation
    
    number_of_vertical_line = int(image.shape[1]/panel_dimension[0])
    vertical_line = []
    for i in range(panel_dimension[0]+1):
        x_of_line = i * number_of_vertical_line
        vertical_line.append(x_of_line)

    number_of_horizontal_line = int(image.shape[0]/panel_dimension[1])
    horizontal_line = []
    for i in range(panel_dimension[1]+1):
        y_of_line = i * number_of_horizontal_line
        horizontal_line.append(y_of_line)
    
    panel = [[0 for i in range(panel_dimension[0])] for j in range(panel_dimension[1])]
    for i in range(panel_dimension[1]):
        for j in range(panel_dimension[0]):
            x0, x1 = vertical_line[j], vertical_line[j+1]
            y0, y1 = horizontal_line[i], horizontal_line[i+1]
            
            roi = mask[y0:y1, x0:x1]

            number_of_white_pix = np.sum(roi == 255)
            number_of_black_pix = np.sum(roi == 0)
            if number_of_white_pix > number_of_black_pix:
                panel[i][j] = 1

    for row in panel:
        print(*row, sep=' ', end='\n')

    return panel
    