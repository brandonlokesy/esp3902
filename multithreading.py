import sys
import threading
import time

import cv2
import numpy as np

import colourclassification as cc
import coordinatestransformation as ct
from arduino import Arduino
from legobrick import Lego
from pydexarm import Dexarm

hsvRange = np.array([[0, 91, 62], [107, 255, 255]])
def getContours(img):
    def get_contour_precedence(contour, cols):
        tolerance_factor = 10
        origin = cv2.boundingRect(contour)
        return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contours, key = lambda x:get_contour_precedence(x, img.shape[1]))
    # sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])
    return sorted_contours

def rotrics_track():
    if lego.active == False:
        print("Nothing to track")
        pass
    else:
        x,y = lego.get_xy()
        dexarm.move_to((x,y, 0), feedrate = 100000)
        pass


def pick():
    while True:
        if lego.active == False:
            arduino.operate()
            print("Nothing to track")
        else:
            arduino.stop()
            x,y = lego.get_xy()
            print('tracking')
            print("Rotrics moving to {x}, {y}".format(x=x,y=y))
            dexarm.move_to((x,y, 30), feedrate = 100000)

            time.sleep(1)
            dexarm.delay_ms(100)
            xpos, ypos = lego.get_xy()
            xrobot, yrobot = dexarm.get_current_position()[:2]
            if (xpos - error < xrobot < xpos + error) and (ypos - error < yrobot < ypos + error):
                x,y = lego.get_xy()
                dexarm.move_to((x,y,-32), feedrate = 100000)
                dexarm.soft_gripper_pick()
                dexarm.move_to((x,y,50), feedrate = 100000)
                place, railpos = cc.colourBucket(lego.get_colour())
                print('place is', str(place))
                xplace, yplace, z = place
                print('x is {x}, y is {y}'.format(x = xplace, y = yplace))
                dexarm.move_rail(extrude = railpos, feedrate = 100000)
                dexarm.move_to((xplace, yplace, 50), feedrate = 100000)
                dexarm.soft_gripper_place()
                dexarm.move_to((0, 200, 30), feedrate = 100000)
                lego.deactivate()

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
                diff = cv2.absdiff(self.img, ref)
                th, dst = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
                dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
                con, hie = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(dst, con, -1,(255,255,255),3)
                res = cv2.bitwise_and(self.img, self.img, mask = dst)
                hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

                mask = cv2.inRange(hsv, hsvRange[0], hsvRange[1])
                out = cv2.bitwise_and(hsv, hsv, mask = mask)

                imgContours = out.copy()
                imgBlur = cv2.GaussianBlur(out, (7,7), 1)
                imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

                threshold1 = 97
                threshold2 = 255

                imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
                imgDil = cv2.dilate(imgCanny, np.ones((5,5)), iterations = 1)
                contours = getContours(imgDil)

                mask = np.zeros(self.img.shape, np.uint8)
                if not contours:
                    lego.deactivate()
                elif contours and cv2.contourArea(contours[0]) > 200:
                    cv2.drawContours(mask, contours[0], -1, 255, -1)

                    M = cv2.moments(contours[0])
                    cX = int((M["m10"] / M["m00"]))
                    cY = int((M["m01"] / M["m00"]))

                    pixel = self.img[cY, cX, :]
                    cYmm = round(ct.y_mm(cY))
                    cXmm = round(ct.x_mm(cX))
                    colour = cc.get_colour(pixel)

                    lego.update(colour, (cXmm,cYmm))
                    print('lego is at' + str(lego.get_xy()))
                    # time.sleep(0.01)
        
    def show_frame(self):
        cv2.imshow('frame', self.img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

if __name__ == '__main__':
    ref = cv2.imread('./Images/staticref.jpg')
    lego = Lego()
    dexarm = Dexarm('COM4')
    error = 15
    pixeltol = 30
    arduino = Arduino('COM6')
    dexarm.go_home()
    lego.active = False

    dexarm.soft_gripper_place()

    vid = VideoStreamWidget()

    time.sleep(1)
    while True:
        try:
            vid.show_frame()
            pick()
        except(KeyboardInterrupt, SystemExit):
            print("Received keyboard interrupt\n")
            dexarm.go_home()
            dexarm.soft_gripper_nature()
            cv2.destroyAllWindows()
            sys.exit()
