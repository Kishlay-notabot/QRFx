import cv2
# import pygame
import sys
import numpy as np
image = cv2.imread('qr.png', cv2.IMREAD_GRAYSCALE)
threshold1 = int(sys.argv[1]) if len(sys.argv) > 1 else 50
threshold2 = int(sys.argv[2]) if len(sys.argv) > 2 else 100
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
kernel = np.ones((15, 15), np.uint8)
# image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
th, im_th_gray = cv2.threshold(image,170,255,cv2.THRESH_BINARY)
closed_img = cv2.morphologyEx(im_th_gray, cv2.MORPH_CLOSE, kernel)
# print(th)
# contours, hierarchy = cv2.findContours(im_th_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# im_color = cv2.cvtColor(im_th_gray, cv2.COLOR_GRAY2BGR)
# cv2.drawContours(im_color, contours, -1, (0, 0, 255), 1)
edges = cv2.Canny(image=closed_img, threshold1=threshold1, threshold2=threshold2)
resz = ResizeWithAspectRatio(edges, width=400)
cv2.imshow('blurred', resz)
cv2.waitKey(1000)
cv2.destroyAllWindows()
cv2.imwrite('qr2.png', edges)
# tried gaussian blur. FILLING is the only option. maybe
# bilateral filter didnt work
# white fill, floodfill.
# otsu bad 170 b/w
# https://answers.opencv.org/question/53548/gap-filling-contours-lines/
# https://stackoverflow.com/questions/26586123/filling-gaps-in-shape-edges
# https://www.reddit.com/r/learnpython/comments/h16htq/how_to_change_all_colors_in_the_image_to_white/

