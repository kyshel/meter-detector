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

ACCU=0


def draw_cross(img,loc):
	(x,y) = loc
	cv2.line(img,(x,y-10),(x,y+10),(255,0,0),1)
	cv2.line(img,(x-10,y),(x+10,y),(255,0,0),1)


def get_region(img):
	global ACCU
	ACCU+=1
	str_accu=str(ACCU)

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
	cv2.imshow("region.png"+str_accu, region)	

	return region

	

def get_contours(region):
	global ACCU
	str_accu=str(ACCU)

	## Change to LAB space
	lab = cv2.cvtColor(region, cv2.COLOR_BGR2LAB)
	l,a,b = cv2.split(lab)
	imglab = np.hstack((l,a,b))
	cv2.imshow("region_lab.png"+str_accu, imglab)	

	## normalized the a channel to all dynamic range
	na = cv2.normalize(a, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
	cv2.imshow("region_a_normalized.png"+str_accu, na)	

	## Threshold to binary
	retval, threshed = cv2.threshold(na, thresh = 180,  maxval=255, type=cv2.THRESH_BINARY)	

	## Do morphology
	kernel = cv2.getStructuringElement( cv2.MORPH_ELLIPSE , (3,3))
	opened = cv2.morphologyEx(threshed, cv2.MORPH_OPEN,kernel)
	res = np.hstack((threshed, opened))
	cv2.imshow("region_a_binary.png"+str_accu, res)	

	## Find contours
	contours = cv2.findContours(opened, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)[-2]

	return contours


def get_contours_filtered(contours,region):
	global ACCU
	str_accu=str(ACCU)

	## Draw Contours
	res = region.copy()
	cv2.drawContours(res, contours, -1, (255,0,0), 1)
	cv2.imshow("region_contours.png"+str_accu, res)

	## Filter Contours
	contours_filtered = []
	i=0
	for idx, contour in enumerate(contours):
		bbox = cv2.boundingRect(contour)
		area = bbox[-1]*bbox[-2]
		if area < 100:
			continue
		contours_filtered += [contour]
		i+=1
		rot_rect = cv2.minAreaRect(contour)
		(cx,cy), (w,h), rot_angle = rot_rect
		rbox = np.int0(cv2.boxPoints(rot_rect))
		cv2.drawContours(res, [rbox], 0, (0,255,0), 1)
		text="#{}: {:2.3f} > {}".format(idx, rot_angle,str(i))
		org=(int(cx)-10,int(cy)-10)
		#cv2.putText(res, text=text, org = org, fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale=0.7, color=(0,0,255), thickness = 1, lineType=cv2.LINE_AA)
		cv2.putText(res, text=text, org = org, fontFace = 1, fontScale=0.8, color=YELLOW, thickness = 1, lineType=16)

		cv2.imshow("region_result.png"+str_accu, res)

	return contours_filtered


def get_center(contours_filtered,region):
	global ACCU
	str_accu=str(ACCU)

	list_contours_length = [len(x) for x in contours_filtered]
	index_min_countur_length = np.argmin(list_contours_length)
	center_contour=contours_filtered[index_min_countur_length]

	rot_rect = cv2.minAreaRect(center_contour)
	(cx,cy), (w,h), rot_angle = rot_rect

	loc_center = (int(cx),int(cy))
	draw_cross(region,loc_center)
	#cv2.circle(region,loc , 20, BLACK , thickness=5, lineType=8, shift=0) 

	cv2.imshow("region_center.png"+str_accu, region)

	return loc_center
