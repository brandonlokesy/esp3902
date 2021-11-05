import cv2
import numpy as np

framewidth = 640
frameheight = 480

cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)
hsvRange = np.array([[0, 91, 62], [107, 255, 255]])

def empty(a):
    #comment
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", framewidth, frameheight)
cv2.createTrackbar("Threshold1", "Parameters", 97, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 255, 255, empty)

def getContours(img, imgContours):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContours, contours, -1, (255, 0, 255), 7)


while True:
    ret, img = cap.read()
    # img = cv2.imread('./Images/Test Data/test1.jpg')
    imgContours = img.copy()

    frameHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(frameHSV, hsvRange[0], hsvRange[1])
    result = cv2.bitwise_and(frameHSV, frameHSV, mask = mask)

    imgBlur = cv2.GaussianBlur(result, (3,3), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((3,3))
    imgDil = cv2.dilate(imgCanny, kernel, iterations = 1)
    # imgDil = imgCanny


    getContours(imgDil, imgContours)
    # imgStack = stackImages(0.8, ([img, imgBlur, imgGray]))
    # imgStack = np.hstack([[img], [imgBlur], [imgCanny]])

    cv2.imshow("image", img)
    cv2.imshow("blurred", imgContours)
    # cv2.imshow()
    cv2.imshow("gray", imgDil)
    # cv2.imshow("Result", imgStack)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break


'''
From experimenting, I suggest
Threshold1 = 55
Threshold2 = 131'''