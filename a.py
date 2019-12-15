import cv2
import numpy as np
from pprint import pprint
import logging

logging.basicConfig(
	level=logging.INFO,
	# format='%(asctime)s %(name)-1s %(levelname)-3s %(message)s',
	#format='%(levelname)-3s %(message)s',
	format='%(levelname)-3s [%(filename)s:%(lineno)d] %(message)s',
	datefmt='%y-%m-%d %H:%M:%S',
	handlers=[
	# logging.FileHandler(FILENAME_LOGGING),
	logging.StreamHandler()
	]
)


WHITE = [255,255,255]
BLACK = [0,0,0]
RED =[0,0,255]
GREEN =[0,255,0]
BLUE =[255,0,0]
YELLOW =[0,243,255]
PINK =[189,0,255]
PURPLE =[255,0,205]

 




img_origin = cv2.imread('1.jpg')
img2 = img_origin.copy()
img = img_origin.copy()
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

height, width, channels = img.shape



red_points_loc = []

for i in range(0,height-1):
	for j in range(0,width-1):
 
		cur_point = img[i][j]

 
		shift = 10
		r=235
		g=2
		b=0

		if  (r-shift <= cur_point[2] <= r+shift) and \
			(g-shift <= cur_point[1] <= g+shift) and \
			(b-shift <= cur_point[0] <= b+shift) :
				# logging.info('1')
				# logging.info(cur_point)
				# logging.info((i,j))

				red_points_loc += [[i,j]]



	# 	break
	# break



logging.info(red_points_loc)

rec_x_points = [x for x,y in red_points_loc]
rec_y_points = [y for x,y in red_points_loc]

rec_LU=(min(rec_y_points),min(rec_x_points))
rec_RD=(max(rec_y_points),max(rec_x_points))





cv2.rectangle(img, rec_RD, rec_LU, (255,0,0), 5)



# for i,j in red_points_loc:
# 	img[i,j] = [255,0,0]



# pprint(img)

# cv2.circle(img, rec_LU, 5, BLACK , thickness=5, lineType=8, shift=0) 




 
img = img_origin.copy()
## Threshold in grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
retval, threshed = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY )

## Find wathc region by counting the projector
h,w = img.shape[:2]
x = np.sum(threshed, axis=0)
y = np.sum(threshed, axis=1)
yy = np.nonzero(y>(w/5*255))[0]
xx = np.nonzero(x > (h/5*255))[0]
region = img[yy[0]:yy[-1], xx[0]:xx[-1]]
cv2.imshow("region.png", region)

## Change to LAB space
lab = cv2.cvtColor(region, cv2.COLOR_BGR2LAB)
l,a,b = cv2.split(lab)
imglab = np.hstack((l,a,b))
cv2.imshow("region_lab.png", imglab)

## normalized the a channel to all dynamic range
na = cv2.normalize(a, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
cv2.imshow("region_a_normalized.png", na)

## Threshold to binary
retval, threshed = cv2.threshold(na, thresh = 180,  maxval=255, type=cv2.THRESH_BINARY)

## Do morphology
kernel = cv2.getStructuringElement( cv2.MORPH_ELLIPSE , (3,3))
opened = cv2.morphologyEx(threshed, cv2.MORPH_OPEN,kernel)
res = np.hstack((threshed, opened))
cv2.imshow("region_a_binary.png", res)

## Find contours
contours = cv2.findContours(opened, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)[-2]

logging.info(contours	)

list_contours_length = [len(x) for x in contours]

index_min_countur_length = np.argmin(list_contours_length)

logging.info(index_min_countur_length	)
 


## Draw Contours
res = region.copy()
cv2.drawContours(res, contours, -1, (255,0,0), 1)
cv2.imshow("region_contours.png", res)

## Filter Contours
for idx, contour in enumerate(contours):
    bbox = cv2.boundingRect(contour)
    area = bbox[-1]*bbox[-2]
    if area < 100:
        continue
    rot_rect = cv2.minAreaRect(contour)
    (cx,cy), (w,h), rot_angle = rot_rect
    rbox = np.int0(cv2.boxPoints(rot_rect))
    cv2.drawContours(res, [rbox], 0, (0,255,0), 1)
    text="#{}: {:2.3f}".format(idx, rot_angle)
    org=(int(cx)-10,int(cy)-10)
    #cv2.putText(res, text=text, org = org, fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale=0.7, color=(0,0,255), thickness = 1, lineType=cv2.LINE_AA)
    cv2.putText(res, text=text, org = org, fontFace = 1, fontScale=0.8, color=(0,0,255), thickness = 1, lineType=16)

cv2.imshow("region_result.png", res)












#cv2.imshow('img',img)
cv2.waitKey(0) 
cv2.destroyAllWindows()