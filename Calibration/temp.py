from types import resolve_bases
import cv2
import numpy as np
import coordinatestransformation as ct
import colourclassification as cc
# hsvRange = np.array([[0, 97, 96], [111, 255, 209]])
# hsvRange = np.array([[0, 91, 62], [107, 255, 255]])
hsvRange = np.array([[0, 93, 120], [128, 255, 255]])


framewidth = 1920
frameheight = 1080

cap = cv2.VideoCapture(0)

cap.set(3, framewidth)
cap.set(4, frameheight)

# fgbg = cv2.createBackgroundSubtractorMOG2(history = 1000000)

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(imgContours, contours, -1, (150, 0, 150), 3)
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    return sorted_contours

ref = cv2.imread('./Images/staticref.jpg')

while True:
    if cap.isOpened():
        status, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        diff = cv2.absdiff(img, ref)
        th, dst = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        con, hie = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(dst, con, -1,(255,255,255),3)
        res = cv2.bitwise_and(img, img, mask = dst)
        cv2.imshow('dest', res)

        hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, hsvRange[0], hsvRange[1])
        out = cv2.bitwise_and(img, img, mask = mask)

        imgContours = out.copy()
        imgBlur = cv2.GaussianBlur(out, (7,7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

        threshold1 = 97
        threshold2 = 255

        imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
        imgDil = cv2.dilate(imgCanny, np.ones((5,5)), iterations = 1)
        contours = getContours(imgDil)
        # if not contours:
        #     lego.deactivate()
        # for contour in contours:
        mask1 = np.zeros(img.shape[:2], np.uint8)
        for c in contours:
            if cv2.contourArea(c) > 200:
                cv2.drawContours(mask1, c, -1, 255, -1)
                M = cv2.moments(c)
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                # cv2.imshow('hsv', hsv)
                # cv2.imshow('res', mask1)
                pixel = img[cY, cX, :]
                # print(cX, cY)
                colour = cc.get_colour_gnb(pixel)

                cv2.rectangle(img, pt1 = (cX - 40, cY-40), pt2 = (cX + 40, cY +40), color = (52, 235, 164), thickness = 1)
                cv2.putText(img, colour, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
                
                cYmm = round(ct.y_mm(cY))
                cXmm = round(ct.x_mm(cX))

        cv2.imshow('img', cv2.resize(img, (1280, 720), interpolation = cv2.INTER_LINEAR))
        cv2.imshow('hsv', out)
                # print('hsv mean is {hsv}'.format(hsv = hsvmean))
                        # lego.update(colour, (cXmm,cYmm))
                        # print('lego is at' + str(lego.get_xy()))
                        # time.sleep(0.01)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
# # cap = cv2.VideoCapture(0)
# if (cap.isOpened()== False): 
#   print("Error opening video  file")
# cap.set(3, framewidth)
# cap.set(4, frameheight)

# img = cv2.imread('./Images/legoref.jpg')
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img = cv2.resize(img, (1280, 720))  
# cv2.imshow('img', imS)

# def empty(a):
#     pass
# # cv2.namedWindow("HSV")
# # cv2.resizeWindow("HSV", framewidth, frameheight)
# # cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
# # cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
# # cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
# # cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
# # cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
# # cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

# def getContours(img, imgContours):
#     contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     # cv2.drawContours(imgContours, contours, -1, (150, 0, 150), 3)
#     return contours

# # img = cv2.imread('./Images/legoref.jpg')
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# hsvRange = np.array([[85, 162, 0], [179, 255, 255]])
# mask = cv2.inRange(img_hsv, hsvRange[0], hsvRange[1])
# hsv_masked = cv2.bitwise_and(img_hsv, img_hsv, mask = mask)

# imgContours = hsv_masked.copy()
# imgBlur = cv2.GaussianBlur(hsv_masked, (7,7), 1)
# imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

# threshold1 = 55
# threshold2 = 131

# imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
# # kernel = np.ones((5,5))
# imgDil = cv2.dilate(imgCanny, np.ones((5,5)), iterations = 1)

# contours = getContours(imgDil, imgContours)

# # cv2.imshow('contours', imgDil)
# # cv2.imwrite('./Images/contours.png', imgDil)
# for c in contours:
#     # if 1200  < cv2.contourArea(c) < 1500:
#     if cv2.contourArea(c) > 200:
#         # print(cv2.contourArea(c))
#         M = cv2.moments(c)
#         cX = int((M["m10"] / M["m00"]))
#         cY = int((M["m01"] / M["m00"]))

#         # print(cX, cY)
#         pixel = img[cY, cX, :]

#         cYmm = round(ct.y_mm(cY))
#         cXmm = round(ct.x_mm(cX))
#         # cYcm = cY * cm2pixel
#         # cXcm = cX * cm2pixel
#         # position = np.array([cXcm, cYcm, 0, 1])[np.newaxis].T
#         # coordsBaseFrame = transformation @ position
#         # x = math.floor(coordsBaseFrame[0] * 10) 
#         # y = math.floor(coordsBaseFrame[1] * 10)
#         # print(pixel)
#         cv2.circle(img, center = (cX, cY), radius = 2, color = (0,0,0), lineType = 10)
#         colour = cc.get_colour(pixel)

#         # lego.update(colour, coordsBaseFrame)
#         # pick_lego()

#         # cv2.rectangle(img, pt1 = (cX - 40, cY-40), pt2 = (cX + 40, cY +40), color = (52, 235, 164), thickness = 5)
#         # cv2.putText(img, colour, (cX, cY-110), cv2.FONT_HERSHEY_SIMPLEX, 1, (52, 235, 164), 2)
#         # cv2.putText(img, str(cXmm), (cX, cY -80), cv2.FONT_HERSHEY_SIMPLEX, 1, (52, 235, 164), 2)
#         # cv2.putText(img, str(cYmm), (cX, cY - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (52, 235, 164), 2)
#         cv2.putText(imgContours, colour, (cX, cY - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# cv2.imshow('img', img)
# cv2.imwrite('./Images/detect_center.png', imgDil)

# cv2.imshow('res', imgContours)
# while True:

#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     h_min = cv2.getTrackbarPos("HUE Min", "HSV")
#     h_max = cv2.getTrackbarPos("HUE Max", "HSV")
#     s_min = cv2.getTrackbarPos("SAT Min", "HSV")
#     s_max = cv2.getTrackbarPos("SAT Max", "HSV")
#     v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
#     v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

#     lower = np.array([h_min, s_min, v_min])
#     upper = np.array([h_max, s_max, v_max])

#     mask = cv2.inRange(hsv, lower, upper)
#     result = cv2.bitwise_and(hsv, hsv, mask = mask)
#     cv2.imshow('result', result)
#     if cv2.waitKey(30) & 0xFF == ord('q'):
#         break

# while True:
#     ret, frame = cap.read()
#     if ret == True:
#         frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#         h_min = cv2.getTrackbarPos("HUE Min", "HSV")
#         h_max = cv2.getTrackbarPos("HUE Max", "HSV")
#         s_min = cv2.getTrackbarPos("SAT Min", "HSV")
#         s_max = cv2.getTrackbarPos("SAT Max", "HSV")
#         v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
#         v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

#         lower = np.array([h_min, s_min, v_min])
#         upper = np.array([h_max, s_max, v_max])

#         mask = cv2.inRange(frameHSV, lower, upper)
#         result = cv2.bitwise_and(frameHSV, frameHSV, mask = mask)


#         # cv2.imshow('Original', frame)
#         # cv2.imshow('HSV Colour Space', frameHSV)
#         # cv2.imshow("Mask", mask)
#         # cv2.imshow("Result", result)

#         mask = cv2.cvtColor(mask ,cv2.COLOR_GRAY2BGR)
#         hstack = np.hstack([frame, mask, result])
#         cv2.imshow("Horizontal Stack", hstack)

#         if cv2.waitKey(30) & 0xFF == ord('q'):
#             break
#     else:
#         break
cv2.waitKey(0)
cv2.destroyAllWindows()