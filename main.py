import cv2
import numpy as np
import imutils
import colourclassification as cc
from legobrick import Lego
from pydexarm import Dexarm
import time
import math
import coordinatestransformation as ct

framewidth = 1920
frameheight = 1080


# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)

cap.set(3, framewidth)
cap.set(4, frameheight)

# cm2pixel = 1/(14.7)
cm2pixel = 30.6/480

blueHSV = np.array([[94, 80, 112], [120, 255, 255]])
redHSV = np.array([[0, 125, 165],[13, 255, 255]] )
greenHSV = np.array([[40, 93, 130], [179, 255, 255]])  
hsvRange = np.array([[0, 182, 112], [114, 255, 145]])

# rotation = np.array([[-1, 0, 0],
#                     [0 ,1, 0],
#                     [0, 0, -1],
#                     [0, 0, 0]])
# displacement = np.array([17.7, 13.5, 0, 1])[np.newaxis].T
# transformation = np.hstack((rotation, displacement))

# colourLocations = {}

lego = Lego()
dexarm = Dexarm("COM4")

dexarm.go_home()
dexarm.sliding_rail_init()
dexarm.move_rail(0)

def getContours(img, imgContours):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(imgContours, contours, -1, (150, 0, 150), 3)
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    return (sorted_contours[0],)
    #test comment


def pick_lego(lego):
    if lego.active == False:
        print("nothing to pick")
        pass
    else:
        print("Picking up Lego")
        x,y = lego.get_xy()
        colour = lego.get_colour()
        dexarm.fast_move_to((x,y, 20), feedrate = 10000)
        dexarm.fast_move_to((x,y, -32), feedrate = 10000)
        if dexarm.get_current_position()[:2] == (cXmm, cYmm):
            dexarm.soft_gripper_pick()
            dexarm.fast_move_to((x,y,30), feedrate = 10000)
            dexarm.move_rail(extrude = 400, feedrate = 5000)
            # dexarm.move_to(cc.colourBucket(colour))
            dexarm.fast_move_to((200, 100, 0), feedrate = 5000)
            dexarm.soft_gripper_place()
            dexarm.move_rail(extrude = 0, feedrate = 5000)
            # dexarm.go_home()
            dexarm.fast_move_to((0, 200, 30), feedrate = 10000)
            # dexarm.soft_gripper_nature()
            lego.deactivate()
            pass

def rotrics_track(lego):
    if lego.active == False:
        print("Nothing to track")
        pass
    else:
        # print("Tracking Lego")
        x,y = lego.get_xy()
        print(x,y)
        dexarm.move_to((x,y, -10))
        # time.sleep(10)
        pass


while True:
    ret, img = cap.read()
    # print(img.shape)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    # blueMask = cv2.inRange(hsv, blueHSV[0], blueHSV[1])
    # redMask = cv2.inRange(hsv, redHSV[0], redHSV[1])
    # greenMask = cv2.inRange(hsv, greenHSV[0], greenHSV[1])

    # mask = blueMask & redMask & greenMask
    # mask = cv2.bitwise_or(blueMask, redMask)
    # mask = cv2.bitwise_or(mask, greenMask)

    mask = cv2.inRange(hsv, hsvRange[0], hsvRange[1])

    out = cv2.bitwise_and(img, img, mask = mask)
    cv2.imshow("image", out)

    imgContours = out.copy()
    imgBlur = cv2.GaussianBlur(out, (7,7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = 55
    threshold2 = 131
    
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    # kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny, np.ones((5,5)), iterations = 1)

    contours = getContours(imgDil, imgContours)
    # cv2.imshow("colour mask", imgDil)

    # cv2.imshow('img', img)
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)[1:]
    for c in contours:
        # if 1200  < cv2.contourArea(c) < 1500:
        if cv2.contourArea(c) > 200:
            # print(cv2.contourArea(c))
            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))

            # print(cX, cY)
            pixel = img[cY, cX, :]

            cYmm = round(ct.y_mm(cY))
            cXmm = round(ct.x_mm(cX))
            # cYcm = cY * cm2pixel
            # cXcm = cX * cm2pixel
            # position = np.array([cXcm, cYcm, 0, 1])[np.newaxis].T
            # coordsBaseFrame = transformation @ position
            # x = math.floor(coordsBaseFrame[0] * 10) 
            # y = math.floor(coordsBaseFrame[1] * 10)
            # print(pixel)
            cv2.circle(img, center = (cX, cY), radius = 2, color = (0,0,0), lineType = 10)
            colour = cc.get_colour(pixel)

            # lego.update(colour, coordsBaseFrame)
            # pick_lego()

            cv2.rectangle(img, pt1 = (cX - 40, cY-40), pt2 = (cX + 40, cY +40), color = (52, 235, 164), thickness = 1)
            cv2.putText(img, colour, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            cv2.putText(img, str(cXmm), (cX, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            cv2.putText(img, str(cYmm), (cX, cY + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            cv2.putText(imgContours, colour, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            # print(img.shape, (cX, cY))
            # imgStack = stackImages(0.8, ([img, imgBlur, imgGray]))
            # imgStack = np.hstack([[img], [imgBlur], [imgCanny]])
            cv2.imshow("image", img)
            cv2.imshow("blurred", imgContours)
            cv2.imshow("gray", imgDil)

            lego.update(colour, (cXmm,cYmm))
            pick_lego(lego)
            # rotrics_track(lego)
            # dexarm.move_to((x,y, 50))
            # dexarm.move_to(())

            # cv2.imshow("Result", imgStack)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
    if cv2.waitKey(30) & 0xFF == ord('q'):
            break

#333 324
'''
From experimenting, I suggest
Threshold1 = 55
Threshold2 = 131'''