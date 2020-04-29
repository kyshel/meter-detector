# meter-detector
这是图灵联邦举办的一项比赛，根据所提供如下的1001张图片，实现2件事：  
1、定位表盘的圆心位置；  
2、定位圆心和指针的位置；  
![image](https://user-images.githubusercontent.com/11898075/80555225-3c08d180-8a02-11ea-8c45-8ac4cb13a920.png)
比赛链接：https://www.turingtopia.com/competitionnew/detail/53aa39e8d46048d8a4de2c6d21adafb1/sketch


# 最终排名得分
https://www.turingtopia.com/competitionnew/detail/53aa39e8d46048d8a4de2c6d21adafb1/ranking
![image](https://user-images.githubusercontent.com/11898075/80555125-f1875500-8a01-11ea-9865-625a732dd68e.png)

# 解题思路
1.	Get_region截取目标区域
 
![image](https://user-images.githubusercontent.com/11898075/80555064-b9801200-8a01-11ea-80e0-d456e4aae259.png)

2.	Get_contours获取红色区域轮廓
 
![image](https://user-images.githubusercontent.com/11898075/80555068-bbe26c00-8a01-11ea-8cf3-0f48d11813f2.png)

3.	Contours_filtered 利用面积大小过滤红色区域轮廓
 
![image](https://user-images.githubusercontent.com/11898075/80555076-bedd5c80-8a01-11ea-92b9-b1b86bc6c82d.png)

4.	Get_center2 获取圆心坐标
 
![image](https://user-images.githubusercontent.com/11898075/80555079-c1d84d00-8a01-11ea-9b9f-57073e5278dd.png)

5.	Get_img_cutted 画黑色的圆覆盖掉指针根部，只露出尖端
 
![image](https://user-images.githubusercontent.com/11898075/80555082-c4d33d80-8a01-11ea-94cb-7cd3d0b00c71.png)

6.	get_cutted_info获取尖端轮廓并定位质心
 
 
![image](https://user-images.githubusercontent.com/11898075/80555086-c7359780-8a01-11ea-9a87-9378021b4f46.png)
![image](https://user-images.githubusercontent.com/11898075/80555092-cac91e80-8a01-11ea-9b07-0a97017c57f8.png)



7.	结果请见result.txt

