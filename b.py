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


 




img_origin = cv2.imread('2.jpg')



img = img_origin
height, width, channels = img.shape



for i in range(0,height-1):
	for j in range(0,width-1):
 
		cur_point = img[i][j]

		logging.info(cur_point)

 



		shift = 10
		r=235
		g=2
		b=0

		if  (r-shift <= cur_point[2] <= r+shift) and \
			(g-shift <= cur_point[1] <= g+shift) and \
			(b-shift <= cur_point[0] <= b+shift) :
				logging.info('1')
				logging.info(cur_point)



	# 	break
	# break







# pprint(img)


cv2.imshow('img',img)
cv2.waitKey(0) 
cv2.destroyAllWindows()