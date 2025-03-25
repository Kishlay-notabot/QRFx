import cv2
import tkinter as tk
from tkinter import PhotoImage
image = cv2.imread('qr.png', cv2.IMREAD_GRAYSCALE)
# image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
th, im_th_gray = cv2.threshold(image,170,255,cv2.THRESH_BINARY)
print(th)
cv2.imwrite('qr2.png', im_th_gray)
# otsu bad

# 170 b/w