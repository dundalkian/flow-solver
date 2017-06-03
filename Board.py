import time
import ScreenReader as scr
import numpy as np
import cv2
import itertools


def getBoard():
    startTime = time.time()

    listLength = 0
    i = 0
    while ((time.time() - startTime) < 2):
        # TODO - Make the bounding box apply automatically
        simpleImage = scr.getSimpleImage()

        lines = cv2.HoughLinesP(simpleImage, 4, np.pi/180, 400, minLineLength=400, maxLineGap=10)

        lineTemp = lines.tolist()
        lineList = []
        for line in lineTemp:
            line = line[0]
            lineList.append(line)

        for pair in itertools.combinations(lineList, 2):
            if (lineRefiner(pair[0], pair[1])) == False:
                continue
            else:
                lineList.remove(pair[0])
                lineList.remove(pair[1])
                lineList.append(lineRefiner(pair[0], pair[1]))

        i = i+1
        listLength = listLength + len(lineList)
        average = listLength/i

# ######################################################
# Just for show, it throws up the lines for you to see
        for line in lineList:
            cv2.line(simpleImage, (line[0], line[1]), (line[2], line[3]), [100, 255, 100], 4)
            cv2.circle(simpleImage, (line[0], line[1]), 2, (255, 255, 255), 3)
            cv2.circle(simpleImage, (line[2], line[3]), 2, (255, 255, 255), 3)

        cv2.imshow('Window', simpleImage)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
# ######################################################

    boardSize = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    return boardSize[int((average-12)/2)]


def lineRefiner(line1, line2):      # Where a line is a 4 element array of ints (x1 y1 x2 y2)
    e = 5   # Allowed error
    for i in range(4):
        if (line2[i] - line1[i]) < (e * -1) or (line2[i] - line1[i]) > e:
            return False
    newLine = []
    for i in range(4):
       newLine.append(int((line1[i] + line2[i])/2))
    return newLine

def createBoard():
    # TODO - Change output of getBoard() to a list, for rect. boards (WTF am I going to do with the hex set...?)
    size = getBoard()
    board = [[0 for x in range(size)] for y in range(size)]
    print(board)
    print(np.matrix(board))

createBoard()
