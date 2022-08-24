#!/usr/bin/env python

import cv2 as cv
import numpy as np

def homography(source, corners=[[8, 14], [763, 17], [24, 379], [742, 392]]):

    # Read source image.
    im_src = cv.imread(source)

    scale_percent = 60 # percent of original size
    width = int(im_src.shape[1] * scale_percent / 100)
    height = int(im_src.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    im_src = cv.resize(im_src, dim, interpolation = cv.INTER_AREA)

    # Four corners of the book in source image
    # pts_src = np.array([[8, 14], [763, 17], [24, 379], [742, 392]])
    pts_src = np.array(corners)

    # Read destination image.
    im_dst = cv.resize(im_src, (640, 320),
               interpolation = cv.INTER_NEAREST)

    # Four corners of the book in destination image.
    pts_dst = np.array([[0, 0],[640, 0],[0, 320],[640, 320]])

    # Calculate Homography
    h, status = cv.findHomography(pts_src, pts_dst)

    # Warp source image to destination based on homography
    im_out = cv.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))

    # Display images
    cv.imshow("Source Image", im_src)
    cv.imshow("Warped Source Image", im_out)
    cv.imwrite("data/images/pers.jpg", im_out)

    cv.waitKey(0)

# lu, ru, lb, rb = (8,14), (763,17), (24,379), (742,394)
# [8, 14], [763, 17], [24, 379], [742, 394]