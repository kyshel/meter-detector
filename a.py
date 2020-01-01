exec(open("k_lib.py").read())

def get_final(filename):
	img_origin = cv2.imread(filename)

	img = img_origin.copy()
	region = get_region(img)
	contours = get_contours(region)
	contours_filtered = get_contours_filtered(contours,region)
	#loc_center = get_center(contours_filtered,region)
	loc_center=get_center2(region)

 
	# for contour in contours_filtered:
	# 	test=cv2.pointPolygonTest(contour,loc_center,True)
	# 	logging.info(test)

	region_cutted = get_img_cutted(region,loc_center)
	contours_cutted = get_contours(region_cutted)
	contours_cutted_filtered = get_contours_filtered(contours_cutted,region)
	cutted_info,msg=get_cutted_info(region,contours_cutted_filtered,loc_center,filename)
	return msg
 


def main():
	text_preset = "THRESHOLD_OF_BINARY:{},CONTOUR_MINIMAL_AREA:{},CENTER_CIRCULE_RADIUS:{},DEBUG_IMSHOW:{}".format(
		THRESHOLD_OF_BINARY,CONTOUR_MINIMAL_AREA,CENTER_CIRCULE_RADIUS,DEBUG_IMSHOW)
	logging.info(text_preset)

	dirname="t"
	sum_msg=""
	for filename in os.listdir(dirname):
		if filename.endswith(".jpg") :
			file_path=os.path.join(dirname, filename)
			msg=get_final(file_path)
			logging.info("{}: {}".format(filename,msg))
			sum_msg += filename + ',' +msg + '\n'


	with open('result.txt', 'w') as the_file:
    		the_file.write(sum_msg)


	cv2.waitKey(0) 
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()