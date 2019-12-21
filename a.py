exec(open("k_lib.py").read())

def get_final(filename):
	img_origin = cv2.imread(filename)

	img = img_origin.copy()
	region = get_region(img)
	contours = get_contours(region)
	contours_filtered = get_contours_filtered(contours,region)
	loc_center = get_center(contours_filtered,region)

	#loc_center2=get_center2(region)


 
	cv2.createTrackbar('param1', 'center' , 0, 100, partial(on_trackbar, img=region ))
	on_trackbar(10,region)

	return	

	# logging.info(loc_center) 
	 
	region_cutted = get_img_cutted(region,loc_center)
	contours_cutted = get_contours(region_cutted)
	contours_cutted_filtered = get_contours_filtered(contours_cutted,region)
	cutted_info,msg=get_cutted_info(region,contours_cutted_filtered,loc_center)

	return msg
 

def on_trackbar(param1,img):
	res = img.copy()
	gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	circle1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,1000,param1=param1,param2=50,minRadius=220,maxRadius=2000)

	x,y,r=circle1[0][0][0],circle1[0][0][1],circle1[0][0][2]
	#cv2.circle(region,(int(x),int(y)) ,0, BLACK , thickness=r, lineType=8, shift=0) 
	draw_cross	(res	,(int(x),int(y)),YELLOW	,500)
	cv2.imshow("center", res)
	pprint	((x,y,r)) 



def main():
	dirname="t"
	for filename in os.listdir(dirname):
		if filename.endswith(".jpg") :
			file_path=os.path.join(dirname, filename)
			msg=get_final(file_path)
			logging.info("{}: {}".format(filename,msg))









	cv2.waitKey(0) 
	cv2.destroyAllWindows()

if __name__ == "__main__":
    main()