import numpy as np
from PIL import ImageGrab
import cv2
import time
import itertools

#numpy, pillow, opencv


# TODO - Make the mask automatically applied
def maskedArea(img):
    area = np.array([[5, 180], [495, 180], [495, 730], [5, 730]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [area], 255)
    masked = cv2.bitwise_and(img, mask)
    return masked



def getSimpleImage():
    Img = np.array(ImageGrab.grab(bbox=(0, 30, 510, 900)))
    simpleImg = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)
    simpleImg = cv2.Canny(simpleImg, threshold1 = 150, threshold2 = 300)
    simpleImg = maskedArea(simpleImg)
    return simpleImg



# TODO - Find Circle optimizations for all boards. Also, find relative size of circles on rect. boards.
def findCircles(bwImg):
    circles = cv2.HoughCircles(bwImg, cv2.HOUGH_GRADIENT, 1, 30, param1=300, param2=40, minRadius=31, maxRadius=75) #25 min 60 max good for 6x6 boards/ 31 min 80 mqx for 5x5.
    #print(circles)
    circles = np.uint16(np.around(circles))  # rounds to an int,
    print(circles)
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(bwImg, (i[0], i[1]), i[2], (100, 255, 100), 2)
        # draw the center of the circle
        cv2.circle(bwImg, (i[0], i[1]), 2, (100, 100, 255), 3)
    return bwImg


#
# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)
# size = getBoard()
# print('Board is ' + str(size) + 'x' + str(size))






# markTime = time.time()
# while(True):
#     screen = np.array(ImageGrab.grab(bbox=(0, 30, 510, 900)))
#     newScreen = simplifyImage(screen)
#     finalScreen = board(newScreen)
#     cv2.imshow('Window', finalScreen)
#
#     print(time.time() - markTime)
#     markTime = time.time()
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break
