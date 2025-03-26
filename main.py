import cv2
import pygame
image = cv2.imread('qr.png', cv2.IMREAD_GRAYSCALE)
# image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
th, im_th_gray = cv2.threshold(image,170,255,cv2.THRESH_BINARY)
print(th)
# contours, hierarchy = cv2.findContours(im_th_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# im_color = cv2.cvtColor(im_th_gray, cv2.COLOR_GRAY2BGR)
# cv2.drawContours(im_color, contours, -1, (0, 0, 255), 1)
edges = cv2.Canny(image=im_th_gray, threshold1=100, threshold2=200)
cv2.imwrite('qr2.png', edges)

# otsu bad 170 b/w
pygame.init()
x = 500
y = 500
dsp = pygame.display.set_mode((x, y))
pygame.display.set_caption('QRFx')
img_dp = pygame.image.load("qr2.png").convert()
picture = pygame.transform.scale(img_dp, (x,y))
dsp.blit(picture, (0, 0))
pygame.display.flip()
status = True
while (status):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False
pygame.quit()      
