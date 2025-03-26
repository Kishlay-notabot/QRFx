import cv2
import pygame
image = cv2.imread('qr.png', cv2.IMREAD_GRAYSCALE)
# image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
th, im_th_gray = cv2.threshold(image,170,255,cv2.THRESH_BINARY)
print(th)
cv2.imwrite('qr2.png', im_th_gray)
# otsu bad 170 b/w
pygame.init()
x = 1000
y = 700
dsp = pygame.display.set_mode((x, y))
pygame.display.set_caption('QRFx')
img_dp = pygame.image.load("qr2.png").convert()
dsp.blit(img_dp, (0, 0))
pygame.display.flip()
status = True
while (status):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False
pygame.quit()      
