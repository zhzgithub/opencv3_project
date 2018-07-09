import cv2
import numpy as np
import time

camera = cv2.VideoCapture(0)	# 打开摄像头，并没有读取帧

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
kernel = np.ones((5,5),np.uint8)
background = None

time.sleep(1) #延时1秒

while (True):
  ret, background = camera.read()	# 这一步才是从摄像头中读取帧。每次while循环读取一帧作为背景帧
  background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)	
  background = cv2.GaussianBlur(background, (21, 21), 0) 
  # if background is None:
    # background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	
    # background = cv2.GaussianBlur(background, (21, 21), 0)     
    # # print(background[20][20])	
    # # print(background[80][80])	
    # # print(background[120][120])	
    # continue
  ret2, frame = camera.read()	#再读取一帧，以便和背景帧做差分，求出运动的目标
  
  cv2.imshow("background", background) # 为什么背景是全部黑色？摄像头打开了之后就进行了while循环，直接就读取了帧，
# 此时和摄像头刚打开时间很近，即捕捉到了全黑的帧，因为每次摄像头一打开的第一帧是全黑的？
# 并且从此以后都以这个全黑为背景，不再改变。如果不以全黑的为背景，可通过延时函数time.sleep(5)延时5秒试试看，此时捕捉的背景就是摄像头前方的。

# 照这么说，计算全黑帧与即时帧之间的差异进行目标跟踪，就是对视频的每一帧进行二值化吗？
# 因为背景全黑，差分，就是当前帧减去像素值全接近为零（比如0,1,2这样大小的值）的背景帧，再对这差分得到的帧进行二值化。。
  
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
  

  diff1 = cv2.absdiff(background, gray_frame)
  cv2.imshow("dif1:|background-gray_frame|", diff1)  #如果两帧之间没有动态，那么diff全黑，因为两帧完全一样，差分后为0，即全黑。
# 如果有动态，那么动态部分为亮色，即白色，因为两帧都是灰度图像，所以看似只有黑白，其实有很多灰度范围，只是因为相减后不动的部分
# 像素为0，所以动态的部分就显得很亮。
  diff2 = cv2.threshold(diff1, 50, 255, cv2.THRESH_BINARY)[1]	# 指定阈值法
  # diff2 = cv2.threshold(diff1, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]	# 大津法
  # diff2 = cv2.adaptiveThreshold(diff1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)	#自适应阈值
  # diff = cv2.dilate(diff, es, iterations = 2)
  image, cnts, hierarchy = cv2.findContours(diff2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  # image, cnts, hierarchy = cv2.findContours(diff2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  

  for c in cnts:
    if cv2.contourArea(c) < 1500:
      continue
    else:
      (x, y, w, h) = cv2.boundingRect(c)
      cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)	#画出矩形框
      cv2.rectangle(diff1, (x, y), (x + w, y + h), (255, 255, 0), 2)
  
  cv2.drawContours(gray_frame,cnts,-1,(255,0,0),1)		#画出轮廓
  
  cv2.imshow("gray_frame", gray_frame)
  cv2.imshow("frame", frame)
  cv2.imshow("dif2:", diff2)  
  

  if cv2.waitKey(1000 // 12) & 0xff == ord("q"):	# 当按下的键的的最后一个字节等于“q”的ascii码时，退出while循环
      break

cv2.destroyAllWindows()
camera.release()
