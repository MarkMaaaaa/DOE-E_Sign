#!/usr/bin/env python

import cv2
import numpy as np

if __name__ == '__main__' :

    # Read source image.
    im_src = cv2.imread('panel.jpg')
    # Four corners of the book in source image
    pts_src = np.array([[8, 14], [763, 17], [24, 379], [742, 392]])

    # Read destination image.
    im_dst = cv2.resize(im_src, (640, 320),
               interpolation = cv2.INTER_NEAREST)

    # Four corners of the book in destination image.
    pts_dst = np.array([[0, 0],[640, 0],[0, 320],[640, 320]])

    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)

    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))

    # Display images
    cv2.imshow("Source Image", im_src)
    cv2.imshow("Destination Image", im_dst)
    cv2.imshow("Warped Source Image", im_out)
    cv2.imwrite("image.jpg", im_out)

    cv2.waitKey(0)

# lu, ru, lb, rb = (8,14), (763,17), (24,379), (742,394)
# [8, 14], [763, 17], [24, 379], [742, 394]