import cv2
# import pygame
import sys
import numpy as np
image = cv2.imread('qr2.jpeg', cv2.IMREAD_GRAYSCALE)
threshold1 = int(sys.argv[1]) if len(sys.argv) > 1 else 80
threshold2 = int(sys.argv[2]) if len(sys.argv) > 2 else 200
# image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# th, im_th_gray = cv2.threshold(image,170,255,cv2.THRESH_BINARY)
# print(th)
# contours, hierarchy = cv2.findContours(im_th_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# im_color = cv2.cvtColor(im_th_gray, cv2.COLOR_GRAY2BGR)
# cv2.drawContours(im_color, contours, -1, (0, 0, 255), 1)
edges = cv2.Canny(image=image, threshold1=threshold1, threshold2=threshold2)
# blur = cv2.blur(edges,(5,5))
cv2.imwrite('qr2.png', edges)
# try gaussian blur blurred_img = cv2.GaussianBlur(img, (5,5), 0)
# bilateral filter is maybe what i exactly want. also read about filling contour gaps
# otsu bad 170 b/w
# https://answers.opencv.org/question/53548/gap-filling-contours-lines/
# https://stackoverflow.com/questions/26586123/filling-gaps-in-shape-edges


