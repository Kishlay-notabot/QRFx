import cv2
import pygame
image = cv2.imread('qr.png', cv2.IMREAD_GRAYSCALE)
# image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
th, im_th_gray = cv2.threshold(image,170,255,cv2.THRESH_BINARY)
print(th)
cv2.imwrite('qr2.png', im_th_gray)
# otsu bad 170 b/w
pygame.init()
x = 500
y = 500
dsp = pygame.display.set_mode((x, y))
pygame.display.set_caption('QRFx')
img_dp = pygame.image.load("qr2.png").convert()
picture = pygame.transform.scale(img_dp, (x,y))
im2, contours, hierarchy = cv2.findContours(im_th_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
dsp.blit(picture, (0, 0))
pygame.display.flip()
status = True
while (status):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False
pygame.quit()      
