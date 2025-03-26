import cv2
import pygame
from PIL import Image 
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
pil_image = Image.open('qr2.png')
h = pil_image.size[0]
w = pil_image.size[1]
pil_image = pil_image.resize((w-10,h-10), Image.ANTIALIAS)
pil_image.save('qr_c.png')
img_dp = pygame.image.load("qr_c.png").convert()
dsp.blit(img_dp, (0, 0))
pygame.display.flip()
status = True
while (status):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False
pygame.quit()      
