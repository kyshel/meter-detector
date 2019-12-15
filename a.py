import cv2
import numpy as np
from pprint import pprint

img_origin = cv2.imread('1.jpg')



img = img_origin
height, width, channels = img.shape



for i in range(0,height-1):
	for j in range(0,width-1):
		print(i,j)
		cur_point = img[i][j]

		print(cur_point)



		shift = 10
		r=235
		g=2
		b=0

		break
	break







# pprint(img)


cv2.imshow('img',img)
cv2.waitKey(0) 
cv2.destroyAllWindows()