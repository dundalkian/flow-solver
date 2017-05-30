import numpy as np
from PIL import ImageGrab
import cv2
import time
import itertools

import pyautogui as gui

#numpy, pillow, opencv


# Make a mask to help get rid of lines

# Add logic to get rid of duplicate lines (maybe find dups then average them into one line?)

def playArea(img):
    area = np.array([[5, 180], [495, 180], [495, 730], [5, 730]])
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [area], 255)
    masked = cv2.bitwise_and(img, mask)
    return masked



def simplifyImage(oldImage):
    simpleImg = cv2.cvtColor(oldImage, cv2.COLOR_BGR2GRAY)
    simpleImg = cv2.Canny(simpleImg, threshold1 = 150, threshold2 = 300)
    simpleImg = playArea(simpleImg)
    return simpleImg

def getBoard():
    startTime = time.time()

    listLength = 0
    i = 0
    while ((time.time() - startTime) < 3):
        screen = np.array(ImageGrab.grab(bbox=(0, 30, 510, 900)))
        bwImg = simplifyImage(screen)

        lines = cv2.HoughLinesP(bwImg, 4, np.pi/180, 400, minLineLength=400, maxLineGap=10)

        lineTemp = lines.tolist()
        lineList = []
        for line in lineTemp:
            line = line[0]
            lineList.append(line)
        #print(lineList)
        #print("list")

        for pair in itertools.combinations(lineList, 2):
            if (lineRefiner(pair[0], pair[1])) == False:
                continue
            else:
                #print(pair)
                #print("pair")
                lineList.remove(pair[0])
                lineList.remove(pair[1])
                lineList.append(lineRefiner(pair[0], pair[1]))
        #print(lineList)

        i = i+1
        listLength = listLength + len(lineList)
        average = listLength/i
        for line in lineList:
            #print(line)
            cv2.line(bwImg, (line[0], line[1]), (line[2], line[3]), [100, 255, 100], 4)
            cv2.circle(bwImg, (line[0], line[1]), 2, (255, 255, 255), 3)
            cv2.circle(bwImg, (line[2], line[3]), 2, (255, 255, 255), 3)
        #print("end of loop")

        cv2.imshow('Window', bwImg)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    #print(average)
    #average = int(average)
    #print(average)
    boardSize = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    #print('done')
    return boardSize[int((average-12)/2)]



# Takes two lines and if they are too similar, it averages their points together and returns a single line
# to represent the line that has been counted twice.
def lineRefiner(line1, line2):      # Where a line is a 4 element array of ints (x1 y1 x2 y2)
    #line1 = line1[0]
    #line2 = line2[0]
    #print(line1)
    e = 5 # Allowed error
    for i in range(4):
        if (line2[i] - line1[i]) < (e * -1) or (line2[i] - line1[i]) > e:
            #print(False)
            return False
    newLine = []
    for i in range(4):
       newLine.append(int((line1[i] + line2[i])/2))
    #print(newLine)
    #print("newline")
    return newLine




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

for i in list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)
size = getBoard()
print('Board is ' + str(size) + 'x' + str(size))
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
