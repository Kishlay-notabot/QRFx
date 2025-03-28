import cv2
# import pygame
import sys
import numpy as np
image = cv2.imread('qr.png', cv2.IMREAD_GRAYSCALE)
threshold1 = int(sys.argv[1]) if len(sys.argv) > 1 else 50
threshold2 = int(sys.argv[2]) if len(sys.argv) > 2 else 100
#  ----------------------
#  first to binary
th, im_th_gray = cv2.threshold(image,170,255,cv2.THRESH_BINARY)
#  ----------------------
# then add kernel for closing to binary image

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
#  ----------------------
# Apply morphological closing
for _ in range (5):
    blt = cv2.bilateralFilter(im_th_gray,20,100,100)

resized = ResizeWithAspectRatio(blt, width=400)
#  ----------------------
# resize and show image 
cv2.imshow('closing on binary',resized)
cv2.waitKey(500)

# image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# print(th)
# contours, hierarchy = cv2.findContours(im_th_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# im_color = cv2.cvtColor(im_th_gray, cv2.COLOR_GRAY2BGR)
# cv2.drawContours(im_color, contours, -1, (0, 0, 255), 1)


#  ----------------------
# do edge detection and save file 
edges = cv2.Canny(image=blt, threshold1=threshold1, threshold2=threshold2)

cv2.imwrite('qr2.png', edges)
cv2.imshow('edges',resized)
cv2.waitKey(4000)
cv2.destroyAllWindows()
# https://answers.opencv.org/question/53548/gap-filling-contours-lines/
# https://stackoverflow.com/questions/26586123/filling-gaps-in-shape-edges
# https://www.reddit.com/r/learnpython/comments/h16htq/how_to_change_all_colors_in_the_image_to_white/

