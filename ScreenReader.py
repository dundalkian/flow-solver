import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui

#numpy, pillow, opencv


# Make a mask to help get rid of lines

# Add logic to get rid of duplicate lines (maybe find dups then average them into one line?)


def simplifyImage(oldImage):
    simpleImg = cv2.cvtColor(oldImage, cv2.COLOR_BGR2GRAY)
    simpleImg = cv2.Canny(simpleImg, threshold1 = 150, threshold2 = 300)
    return simpleImg

def board(bwImg):
    lines = cv2.HoughLinesP(bwImg, 4, np.pi/180, 400, minLineLength=400, maxLineGap=10)
    #print(lines)
    for line in lines:
        line = line[0]
        print(line)
        cv2.line(bwImg, (line[0], line[1]), (line[2], line[3]), [100, 255, 100], 4)
        cv2.circle(bwImg, (line[0], line[1]), 2, (255, 255, 255), 3)
        cv2.circle(bwImg, (line[2], line[3]), 2, (255, 255, 255), 3)
    print("end of loop")
    return bwImg

def findCircles(bwImg):
    circles = cv2.HoughCircles(bwImg, cv2.HOUGH_GRADIENT, 1, 30, param1=300, param2=40, minRadius=31, maxRadius=75) #25 min 60 max good for 6x6 boards/ 31 min 80 mqx for 5x5.
    #print(circles)
    circles = np.uint16(np.around(circles))  #rounds to an int,
    print(circles)
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(bwImg, (i[0], i[1]), i[2], (100, 255, 100), 2)
        # draw the center of the circle
        cv2.circle(bwImg, (i[0], i[1]), 2, (100, 100, 255), 3)
    return bwImg

markTime = time.time()
while(True):
    screen = np.array(ImageGrab.grab(bbox=(0, 30, 510, 900)))
    newScreen = simplifyImage(screen)
    finalScreen = board(newScreen)
    cv2.imshow('Window', finalScreen)
    #print(list(pyautogui.locateAllOnScreen('A.png')))
    #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    print(time.time() - markTime)
    markTime = time.time()
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break