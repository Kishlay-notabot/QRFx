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
# cv2.waitKey(0)
th, fn = cv2.threshold(blt,binarization_threshold,255,cv2.THRESH_BINARY) # binarization of 5x gaussian blur
cv2.imwrite('binarized.png', fn) # write binarized
binarez = ResizeWithAspectRatio(fn, width=400)
cv2.imshow('binarized', binarez)
edges = cv2.Canny(image=fn, threshold1=threshold1, threshold2=threshold2) # canny edge detection 
ed_res = ResizeWithAspectRatio(edges, width=400)
cv2.imwrite('result.png', edges) # write canny edged
cv2.imshow('edges',ed_res)
kernel = np.ones((3,3), np.uint8)
dilated_edges = cv2.dilate(edges, kernel, iterations=1)
closed_edges = cv2.morphologyEx(dilated_edges, cv2.MORPH_CLOSE, kernel, iterations=2)
cv2.imshow('dilated and closed', ResizeWithAspectRatio(closed_edges, width=400))
contours, hierarchy = cv2.findContours(closed_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

qr_decoder = cv2.QRCodeDetector()
data, points, _ = qr_decoder.detectAndDecode(fn)
image_bgr = cv2.cvtColor(fn, cv2.COLOR_GRAY2BGR)
if points is not None:
    points = points[0].astype(int)
    for i in range(len(points)):
        pt1 = tuple(points[i])
        pt2 = tuple(points[(i + 1) % len(points)])
        cv2.line(image_bgr, pt1, pt2, (0, 255, 0), 2)

qr_resized = ResizeWithAspectRatio(image_bgr, width=400)
cv2.imshow('cvqrcode detection', qr_resized)
result_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

def angle_between_vectors(v1, v2):
    dot = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_angle = dot / (norm_v1 * norm_v2)
    angle_rad = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    angle_deg = np.degrees(angle_rad)
    return angle_deg

right_angled_contours = []

for contour in contours:
    if len(contour) < 4:
        continue
    
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    if len(approx) >= 4 and cv2.contourArea(approx) > 100:
        angles = []
        for i in range(len(approx)):
            prev_pt = approx[i-1][0]
            curr_pt = approx[i][0]
            next_pt = approx[(i+1) % len(approx)][0]
            
            v1 = prev_pt - curr_pt
            v2 = next_pt - curr_pt
            
            angle = angle_between_vectors(v1, v2)
            angles.append(angle)
        
        right_angles_count = sum(1 for angle in angles if 87 <= angle <= 100)
        
        if right_angles_count >= 2:
            right_angled_contours.append(approx)
            cv2.drawContours(result_image, [approx], -1, (0, 255, 0), 2)

right_angled_contours = sorted(right_angled_contours, key=cv2.contourArea, reverse=True)[:20]

potential_finder_patterns = []
for contour in right_angled_contours:
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h
    if 0.8 <= aspect_ratio <= 1.2:
        potential_finder_patterns.append(contour)

if len(potential_finder_patterns) >= 3:
    finder_patterns = potential_finder_patterns[:3]
    
    all_corners = np.vstack([contour for contour in finder_patterns])
    x, y, w, h = cv2.boundingRect(all_corners)
    
    tl = [x, y]
    tr = [x + w, y]
    bl = [x, y + h]
    br = [x + w, y + h]
    
    corners = np.array([tl, tr, bl, br], np.int32)
    corners = corners.reshape((-1, 1, 2))
    
    cv2.polylines(result_image, [corners], True, (0, 0, 255), 2)
    
    for point in corners:
        x, y = point[0]
        cv2.circle(result_image, (x, y), 5, (255, 0, 0), -1)
        
        line_length = 20
        if x == tl[0] and y == tl[1]:  # Top-left
            cv2.line(result_image, (x, y), (x + line_length, y), (255, 0, 0), 2)
            cv2.line(result_image, (x, y), (x, y + line_length), (255, 0, 0), 2)
        elif x == tr[0] and y == tr[1]:  # Top-right
            cv2.line(result_image, (x, y), (x - line_length, y), (255, 0, 0), 2)
            cv2.line(result_image, (x, y), (x, y + line_length), (255, 0, 0), 2)
        elif x == bl[0] and y == bl[1]:  # Bottom-left
            cv2.line(result_image, (x, y), (x + line_length, y), (255, 0, 0), 2)
            cv2.line(result_image, (x, y), (x, y - line_length), (255, 0, 0), 2)
        elif x == br[0] and y == br[1]:  # Bottom-right
            cv2.line(result_image, (x, y), (x - line_length, y), (255, 0, 0), 2)
            cv2.line(result_image, (x, y), (x, y - line_length), (255, 0, 0), 2)

result_image_resized = ResizeWithAspectRatio(result_image, width=400)
cv2.imshow('QR Code Detection', result_image_resized)
cv2.imwrite('qr_detection.png', result_image)
cv2.waitKey(4000)
cv2.destroyAllWindows()


