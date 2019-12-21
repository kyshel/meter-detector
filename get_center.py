#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import third package
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import cv2
import os
import time


# In[2]:


# !ls BONC\ cloudiip工业仪表表盘读数大赛


# In[3]:


data_path = "t"
example_img_path = "1.jpg"


# In[4]:


from pprint import pprint

def get_center(img_path):
    img = cv2.imread(example_img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # start_time  = time.time()
    circle1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=55, minRadius=200, maxRadius=400)
    # print("cost time, {}".format(time.time() - start_time))

    pprint(circle1)



    circles = circle1[0, :, :]
    # for i in circles[:]:
    #    print("res: circle coor x:{0:}, y:{1:}".format(i[0], i[1]))
    return circles[0][0], circles[0][1], circles[0][2]

x, y, r = get_center(example_img_path)
print("center x:{0:}, center y:{1:}, r: {2:}".format(x, y, r))
img = cv2.imread(example_img_path)

cv2.circle(img,(x,y) ,0, (255,0,0) , thickness=10, lineType=8, shift=0) 

cv2.imshow("img" , img)
cv2.waitKey(0) 
cv2.destroyAllWindows()

# In[5]:


# show center and circle
img = cv2.imread(example_img_path) 

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('img'), plt.xticks([]), plt.yticks([])

cv2.circle(img, (x, y), r, (255, 0, 0), 5)
cv2.circle(img, (x, y), 2, (255, 0, 0), 10)
 
plt.subplot(122), plt.imshow(img)
plt.title('circle'), plt.xticks([]), plt.yticks([])


# In[6]:


start_time = time.time()
for i in os.listdir(data_path):
    if i.endswith(".jpg"):
        img_path = os.path.join(data_path, i)
        x, y, z = get_center(img_path)
        print(x, y, z)
end_time = time.time()
print("total cost time:{0}".format(end_time - start_time))


# In[ ]:





# In[ ]:





# In[ ]:




