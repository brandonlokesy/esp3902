import cv2
import numpy as np
import imutils
import colourclassification as cc
from legobrick import Lego
from pydexarm import Dexarm
import time
import math
import coordinatestransformation as ct
import sys
import threading

hsvRange = np.array([[0, 182, 112], [114, 255, 145]])

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(imgContours, contours, -1, (150, 0, 150), 3)
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    return sorted_contours

def captureCamera(num):
    # cap = cv2.VideoCapture(num)
    # cap.set(3, 1920)
    # cap.set(4, 1080)
    # cm2pixel = 30.6/480
    print('captureCamera')
    while True:
        print('entering camera loop')
        ret, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, hsvRange[0], hsvRange[1])
        out = cv2.bitwise_and(img, img, mask = mask)
        cv2.imshow('hsv masked', out)

        imgContours = out.copy()
        imgBlur = cv2.GaussianBlur(out, (7,7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

        threshold1 = 55
        threshold2 = 131

        imgCanny = cv2.Canny(imgGray, threshold1, threshold2)

        imgDil = cv2.dilate(imgCanny, np.ones((5,5)), iterations = 1)

        contour = getContours(imgDil)

        if cv2.contourArea(contour[0]) > 200:
            print('contour detected')
            M = cv2.moments(contour[0])
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))

            pixel = img[cY, cX, :]

            cYmm = round(ct.y_mm(cY))
            cXmm = round(ct.x_mm(cX))
            cv2.circle(img, center = (cX, cY), radius = 2, color = (0,0,0), lineType = 10)
            colour = cc.get_colour(pixel)
            cv2.rectangle(img, pt1 = (cX - 40, cY-40), pt2 = (cX + 40, cY +40), color = (52, 235, 164), thickness = 1)
            cv2.putText(img, colour, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            cv2.putText(img, str(cXmm), (cX, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            cv2.putText(img, str(cYmm), (cX, cY + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            cv2.putText(imgContours, colour, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow("image", img)
            cv2.imshow("blurred", imgContours)
            cv2.imshow("gray", imgDil)

            lego.update(colour, (cXmm,cYmm))

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break


def rotrics_track(lego):
    if lego.active == False:
        print("Nothing to track")
        pass
    else:
        x,y = lego.get_xy()
        # print("Rotrics moving to {x}, {y}".format(x=x,y=y))
        dexarm.move_to((x,y, -10))

# def pick_lego(lego):
#     if lego.active == False:
#         print('Nothing to pick')
#         pass
#     else:
#         print("Picking up Lego")
#         x,y = lego.get_xy()
#         colour = lego.get_colour()
#         dexarm.fast_move_to((x,y, 20), feedrate = 10000)
#         dexarm.fast_move_to((x,y, -32), feedrate = 10000)
#         if dexarm.get_current_position()[:2] == lego.get_xy():
#             dexarm.soft_gripper_pick()
#             dexarm.fast_move_to((x,y,30), feedrate = 10000)
#             dexarm.move_rail(extrude = 400, feedrate = 5000)
#             # dexarm.move_to(cc.colourBucket(colour))
#             dexarm.fast_move_to((200, 100, 0), feedrate = 5000)
#             dexarm.soft_gripper_place()
#             dexarm.move_rail(extrude = 0, feedrate = 5000)
#             # dexarm.go_home()
#             dexarm.fast_move_to((0, 200, 30), feedrate = 10000)
#             # dexarm.soft_gripper_nature()
#             lego.deactivate()
#             pass        

def pick():
    while True:
        rotrics_track(lego)
        if dexarm.get_current_position()[:2] == lego.get_xy():
            x,y = lego.get_xy()
            dexarm.fast_move_to((x,y,-34), feedrate = 10000)
            dexarm.soft_gripper_pick()
            dexarm.fast_move_to((x,y,0), feedrate = 10000)
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

class VideoStreamWidget(object):
    def __init__(self, src = 0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(3, 1920)
        self.capture.set(4, 1080)
        self.thread = threading.Thread(target = self.update, args = ())
        self.thread.daemon = True
        self.thread.start()
    
    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.img) = self.capture.read()

                hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

                mask = cv2.inRange(hsv, hsvRange[0], hsvRange[1])
                out = cv2.bitwise_and(self.img, self.img, mask = mask)

                imgContours = out.copy()
                imgBlur = cv2.GaussianBlur(out, (7,7), 1)
                imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

                threshold1 = 55
                threshold2 = 131

                imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
                imgDil = cv2.dilate(imgCanny, np.ones((5,5)), iterations = 1)
                contours = getContours(imgDil)
                for contour in contours:
                    if cv2.contourArea(contour) > 200:
                        print('contour detected')
                        M = cv2.moments(contour)
                        cX = int((M["m10"] / M["m00"]))
                        cY = int((M["m01"] / M["m00"]))

                        pixel = self.img[cY, cX, :]
                        print(cX, cY)
                        cYmm = round(ct.y_mm(cY))
                        cXmm = round(ct.x_mm(cX))
                        colour = cc.get_colour(pixel)

                        lego.update(colour, (cXmm,cYmm))
                        print(lego.get_xy())
                        time.sleep(0.01)
        
    def show_frame(self):
        cv2.imshow('frame', self.img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

if __name__ == '__main__':
    lego = Lego()
    dexarm = Dexarm('COM4')
    dexarm.go_home()
    dexarm.sliding_rail_init()
    dexarm.move_rail(0)
    # num = 0
    # cap = cv2.VideoCapture(num)
    # cap.set(3, 1920)
    # cap.set(4, 1080)
    # cm2pixel = 30.6/480
    vid = VideoStreamWidget()
    time.sleep(1)
    while True:
        # ret, img = cap.read()
        # if cap.isOpened():
        #     cv2.imshow('img', img)
        # if cv2.waitKey(30) & 0xFF == ord('q'):
        #     break
        try:
            vid.show_frame()
            # t0 = threading.Thread(target = captureCamera, args = (0,))
            # t1 = threading.Thread(target = pick)
            # t1.daemon = True
            # # t0.start()
            # t1.start()
            pick()
        except(KeyboardInterrupt, SystemExit):
            print("Received keyboard interrupt\n")
            dexarm.go_home()
            dexarm.move_rail(0)
            dexarm.soft_gripper_nature()
            cv2.destroyAllWindows()
            sys.exit()

    