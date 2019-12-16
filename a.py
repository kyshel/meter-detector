exec(open("k_lib.py").read())

img_origin = cv2.imread('1.jpg')

img = img_origin.copy()
region = get_region(img)
contours = get_contours(region)
contours_filtered = get_contours_filtered(contours,region)
loc_center = get_center(contours_filtered,region)

logging.info(loc_center) 
 













#cv2.imshow('img',img)
cv2.waitKey(0) 
cv2.destroyAllWindows()