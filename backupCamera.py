import ScreenReader as scr
import cv2

while True:
    lineList = scr.findLines()
    circleList = scr.findCircles()
    simpleImage = scr.getGreyImage()


    for line in lineList:
        cv2.line(simpleImage, (line[0], line[1]), (line[2], line[3]), [100, 255, 100], 4)
        cv2.circle(simpleImage, (line[0], line[1]), 2, (255, 255, 255), 3)
        cv2.circle(simpleImage, (line[2], line[3]), 2, (255, 255, 255), 3)

    for i in circleList[0, :]:
        # draw the outer circle
        cv2.circle(simpleImage, (i[0], i[1]), i[2], (100, 255, 100), 2)
        # draw the center of the circle
        cv2.circle(simpleImage, (i[0], i[1]), 2, (100, 100, 255), 3)
    cv2.imshow('Window', simpleImage)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
