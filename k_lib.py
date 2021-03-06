import cv2
import numpy as np
from pprint import pprint
import logging
from datetime import datetime
import time
import math
import os
from functools import partial

# 85 ,70 ,90
THRESHOLD_OF_BINARY=90
# 10
CONTOUR_MINIMAL_AREA=10
# 420
CENTER_CIRCULE_RADIUS=205
# 0
DEBUG_IMSHOW = 0





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


def nothing(x):
    pass


def get_date():
	return str(int(round(time.time() * 1000)))[-4:]


def draw_cross(img,loc,color=BLUE,line_length	=10):
	(x,y) = loc
	cv2.line(img,(x,y-line_length),(x,y+line_length),color,1)
	cv2.line(img,(x-line_length,y),(x+line_length,y),color,1)


def get_region(img):
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
	cv2.imshow("region.png"+get_date(), region)	if DEBUG_IMSHOW	else 1

	return region

	

def get_contours(region):
	## Change to LAB space
	lab = cv2.cvtColor(region, cv2.COLOR_BGR2LAB)
	l,a,b = cv2.split(lab)
	imglab = np.hstack((l,a,b))
	cv2.imshow("region_lab.png"+get_date(), imglab) if DEBUG_IMSHOW	else 1	

	## normalized the a channel to all dynamic range
	na = cv2.normalize(a, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
	cv2.imshow("a_normalized.png"+get_date(), na)	if DEBUG_IMSHOW	else 1

	## Threshold to binary
	retval, threshed = cv2.threshold(na, thresh = THRESHOLD_OF_BINARY,  maxval=255, type=cv2.THRESH_BINARY)	

	## Do morphology
	kernel = cv2.getStructuringElement( cv2.MORPH_ELLIPSE , (3,3))
	opened = cv2.morphologyEx(threshed, cv2.MORPH_OPEN,kernel)
	res = np.hstack((threshed, opened))
	cv2.imshow("a_binary.png"+get_date(), res)	if DEBUG_IMSHOW	else 1

	## Find contours
	contours = cv2.findContours(opened, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)[-2]

	return contours


def get_contours_filtered(contours,region):
	## Draw Contours
	res = region.copy()
	cv2.drawContours(res, contours, -1, (255,0,0), 1)
	cv2.imshow("region_contours.png"+get_date(), res) if DEBUG_IMSHOW	else 1

	## Filter Contours
	contours_filtered = []
	i=0
	for idx, contour in enumerate(contours):
		bbox = cv2.boundingRect(contour)
		area = bbox[-1]*bbox[-2]
		if area < CONTOUR_MINIMAL_AREA:
			continue
		contours_filtered += [contour]
		i+=1

		rot_rect = cv2.minAreaRect(contour)
		(cx,cy), (w,h), rot_angle = rot_rect
		rbox = np.int0(cv2.boxPoints(rot_rect))
		cv2.drawContours(res, [rbox], 0, (0,255,0), 1)
		text="#{}: {:2.3f} > {} w{},h{},cx{},cy{}".format(idx, rot_angle,str(i),int(w),int(h),int(cx),int(cy))
		draw_cross(res,(int(cx),int(cy)))
		org=(int(cx)-10,int(cy)-10)
		#cv2.putText(res, text=text, org = org, fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale=0.7, color=(0,0,255), thickness = 1, lineType=cv2.LINE_AA)
		cv2.putText(res, text=text, org = org, fontFace = 1, fontScale=0.8, color=YELLOW, thickness = 1, lineType=16)

	
	cv2.imshow("result.png"+get_date(), res) if DEBUG_IMSHOW	else 1

	return contours_filtered


def get_center(contours_filtered,region):
	list_contours_length = [len(x) for x in contours_filtered]
	index_min_countur_length = np.argmin(list_contours_length)
	center_contour=contours_filtered[index_min_countur_length]

	rot_rect = cv2.minAreaRect(center_contour)
	(cx,cy), (w,h), rot_angle = rot_rect

	loc_center = (int(cx),int(cy))
	draw_cross(region,loc_center)
	#cv2.circle(region,loc , 20, BLACK , thickness=5, lineType=8, shift=0) 

	cv2.imshow("center.png"+get_date(), region) if DEBUG_IMSHOW	else 1

	logging.info(loc_center	)

	return loc_center

def get_center2(region):
	res = region.copy()
	gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,1000,param1=70,param2=50,minRadius=200,maxRadius=403)
	if 	circles is not None	:
		x,y,r=circles[0][0][0],circles[0][0][1],circles[0][0][2]
		cv2.circle(res,(int(x),int(y)) ,r, RED , thickness=1, lineType=8, shift=0) 
		draw_cross(res,(int(x),int(y)),YELLOW	,500)
		cv2.imshow("center"+get_date(), res) if DEBUG_IMSHOW	else 1
	else:
		logging.info('no detect')
	return	int(x),int(y)




	cv2.imshow("center", img)
	cv2.createTrackbar('dp', 'center' , 1, 10, nothing)
	cv2.createTrackbar('mindist', 'center' , 10, 500, nothing)
	cv2.createTrackbar('param1', 'center' , 80, 100, nothing)
	cv2.createTrackbar('param2', 'center' , 50, 100, nothing)
	cv2.createTrackbar('minRadius', 'center' , 200, 500, nothing)
	cv2.createTrackbar('maxRadius', 'center' , 1000, 2000, nothing)

	while(1):
		k = cv2.waitKey(1) & 0xFF
		if k == 27:
			exit()
			break

		# get current positions of four trackbars
		dp = cv2.getTrackbarPos('dp', 'center')
		mindist = cv2.getTrackbarPos('mindist', 'center')
		param1 = cv2.getTrackbarPos('param1', 'center')
		param2 = cv2.getTrackbarPos('param2', 'center')
		minRadius = cv2.getTrackbarPos('minRadius', 'center')
		maxRadius = cv2.getTrackbarPos('maxRadius', 'center')


		res = region.copy()
		gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
		#circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,1000,param1=70,param2=50,minRadius=200,maxRadius=403)
		circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,1000,param1=param1,param2=param2,minRadius=minRadius,maxRadius=maxRadius)

		if 	circles is not None	:
			x,y,r=circles[0][0][0],circles[0][0][1],circles[0][0][2]
			cv2.circle(res,(int(x),int(y)) ,r, RED , thickness=1, lineType=8, shift=0) 
			draw_cross	(res	,(int(x),int(y)),YELLOW	,500)
			cv2.imshow("center", res)
			logging.info('>>>>')
			logging.info(circles)
			logging.info(param1)
			logging.info(param2)
			logging.info(minRadius)
			logging.info(maxRadius)
			logging.info(r)
			logging.info('<<<')

		else:
			logging.info('no detect')

	return	int(x),int(y)



def get_img_cutted(region,loc_center):
	#img = region.copy()
	img = region 
	cv2.circle(img,loc_center ,int(CENTER_CIRCULE_RADIUS / 2), BLACK , thickness=CENTER_CIRCULE_RADIUS, lineType=8, shift=0) 
	cv2.imshow("cutted.png"+get_date(), img) if DEBUG_IMSHOW	else 1
	return img
  

def get_cutted_info(region,contours_cutted_filtered,loc_center,filename):
	info_list=[]
	res = region.copy()

	for idx, contour in enumerate(contours_cutted_filtered):
		cv2.drawContours(region, contour, -1, GREEN, 1)

		m=cv2.moments(contour) 
		cx = int(m['m10'] / m['m00'])
		cy = int(m['m01'] / m['m00'])

		# rot_rect = cv2.minAreaRect(contour)
		# (cx,cy), (w,h), rot_angle = rot_rect
		# rbox = np.int0(cv2.boxPoints(rot_rect))
		# cv2.drawContours(region, [rbox], 0, (0,255,0), 1)
		
		draw_cross(region,(int(cx),int(cy)))
		(ox,oy)=loc_center
		theta_degree=get_degree((cx,cy),loc_center)
		r=math.hypot(ox - cx, cy - oy)
		info_list+= [{
			"r": r,
			"theta": theta_degree,
		}]

		text="#{}: cx{},cy{},degree{},r{}".format(idx, int(cx),int(cy) , str(theta_degree),r)
		org=(int(cx)-10,int(cy)-10)
		#cv2.putText(region, text=text, org = org, fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale=0.7, color=(0,0,255), thickness = 1, lineType=cv2.LINE_AA)
		cv2.putText(region, text=text, org = org, fontFace = 1, fontScale=1, color=YELLOW, thickness = 1, lineType=16)

	# cv2.imshow(filename	+ " cutted.png"+get_date(), region)
	# cv2.waitKey(0)

	msg = get_alted(info_list)
	text_center="Center: ox{},oy{}".format(int(ox),int(oy))

	ox,oy=loc_center
	draw_cross(region,loc_center)	
	cv2.putText(region, text=filename, org = loc_center, fontFace = 1, fontScale=1, color=PINK, thickness = 1, lineType=16)
	cv2.putText(region, text=text_center, org = (ox,oy+20), fontFace = 1, fontScale=1, color=PINK, thickness = 1, lineType=16)
	cv2.putText(region, text="msg: "+msg, org = (ox,oy+40), fontFace = 1, fontScale=1, color=PINK, thickness = 1, lineType=16)
	#v2.imshow(filename	+ " cutted.png"+get_date(), region)



	return	info_list,msg


def get_alted(info):
	list_r = [ele['r'] for ele in  info ]
	index_min = np.argmin(list_r)
	if 	len(info) == 2:
		index_max = 1 - index_min
	elif len(info) == 1:
		index_max = index_min
	else:
		logging.info("ERROR! Check contours!")
		return

	degree_short = info[index_min]['theta']
	degree_long = info[index_max]['theta']
	
	alted_long = round(( degree_long * 1200 / 360) / 50) * 50
	alted_short = round( degree_short * 100 / 360) 

	return "short{},long{}".format(alted_short,alted_long)  

 

def get_degree(loc_x_y,loc_center):
	cx,cy=loc_x_y
	ox,oy=loc_center
	delta_y = cy - oy
	delta_x = cx - ox
	if delta_x > 0:
		if delta_y < 0:
			degree = math.degrees(math.atan(abs(delta_x/delta_y)))
		elif delta_y > 0:
			degree = math.degrees(math.atan(abs(  delta_y/delta_x ))) + 90
		else:
			degree	= 90
	elif delta_x < 0:
		if cy - oy > 0:
			degree = math.degrees(math.atan(abs(delta_x/delta_y))) + 180
		elif cy - oy < 0:
			degree = math.degrees(math.atan(abs(delta_y/delta_x))) + 270
		else	:
			degree	= 270
	else:
		degree	= 0

	# info = "cx{},cy{},ox{},oy{}".format(cx,cy,ox,oy)
	# logging.info(info)

	return degree

		