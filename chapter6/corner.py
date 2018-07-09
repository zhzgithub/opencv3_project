import cv2
import numpy as np
# import sys
# # img = cv2.imread(sys.argv[1])
# # img = cv2.imread('../images/' + 'sys.argv[1]')
# # img = cv2.imread('../images/chess_board.png' )
img = cv2.imread('..\\images\\chess_board.png' )
print(img.shape)

# img = cv2.imread('E:\\opencv3-python\\pycv-master\\chapter6\\chess_board.png' )
# img = cv2.imread('E:/opencv3-python/pycv-master/chapter6/chess_board.png' )
# img = cv2.imread('./chess_board.png' )
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 5, 23, 0.04)
img[dst>0.01 * dst.max()] = [0, 0, 255] 
while (True):
  cv2.imshow('corners', img)
  if (cv2.waitKey() & 0xff) == ord("q"): 
   break
cv2.destroyAllWindows()
