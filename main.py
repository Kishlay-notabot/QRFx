import cv2
import sys
import numpy as np
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


image = cv2.imread('source.png', cv2.IMREAD_GRAYSCALE) # read in grayscale
binarization_threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 170
threshold1 = int(sys.argv[1]) if len(sys.argv) > 2 else 50
threshold2 = int(sys.argv[2]) if len(sys.argv) > 3 else 100
blt = image.copy()
for _ in range (5):
    blt = cv2.GaussianBlur(blt,(5,5),0) # gaussian blur

resized = ResizeWithAspectRatio(blt, width=400)
cv2.imshow('gaussian on grayscale',resized)
cv2.waitKey(500)
th, fn = cv2.threshold(blt,binarization_threshold,255,cv2.THRESH_BINARY) # binarization of 5x gaussian blur
cv2.imwrite('binarized.png', fn) # write binarized
binarez = ResizeWithAspectRatio(fn, width=400)
cv2.imshow('binarized', binarez)
edges = cv2.Canny(image=fn, threshold1=threshold1, threshold2=threshold2) # canny edge detection 
ed_res = ResizeWithAspectRatio(edges, width=400)
cv2.imwrite('result.png', edges) # write canny edged
cv2.imshow('edges',ed_res)

original_image = cv2.imread('source.png')
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

qr_contour = None
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    
    if area > 1000:
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            
            if 0.8 < aspect_ratio < 1.2:
                qr_contour = contour
                break

if qr_contour is not None:
    cv2.drawContours(original_image, [qr_contour], -1, (0, 0, 255), 3)

resized_contour = ResizeWithAspectRatio(original_image, width=800)
cv2.imshow('QR Code Contour', resized_contour)
cv2.waitKey(3000)
cv2.destroyAllWindows()
# https://answers.opencv.org/question/53548/gap-filling-contours-lines/
# https://stackoverflow.com/questions/26586123/filling-gaps-in-shape-edges
# https://www.reddit.com/r/learnpython/comments/h16htq/how_to_change_all_colors_in_the_image_to_white/
# image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# print(th)
# contours, hierarchy = cv2.findContours(im_th_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# im_color = cv2.cvtColor(im_th_gray, cv2.COLOR_GRAY2BGR)
# cv2.drawContours(im_color, contours, -1, (0, 0, 255), 1)
# th, im_th_gray = cv2.threshold(image,170,255,cv2.THRESH_BINARY)

