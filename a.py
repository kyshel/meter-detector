exec(open("k_lib.py").read())

def get_final(filename):
	img_origin = cv2.imread(filename)

	img = img_origin.copy()
	region = get_region(img)
	contours = get_contours(region)
	contours_filtered = get_contours_filtered(contours,region)
	loc_center = get_center(contours_filtered,region)

	# logging.info(loc_center) 
	 
	region_cutted = get_img_cutted(region,loc_center)
	contours_cutted = get_contours(region_cutted)
	contours_cutted_filtered = get_contours_filtered(contours_cutted,region)
	cutted_info,msg=get_cutted_info(region,contours_cutted_filtered,loc_center)

	return msg
 


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