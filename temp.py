import cv2
import numpy as np
import coordinatestransformation as ct
import colourclassification as cc

framewidth = 640
frameheight = 400

# # cap = cv2.VideoCapture(0)
# if (cap.isOpened()== False): 
#   print("Error opening video  file")
# cap.set(3, framewidth)
# cap.set(4, frameheight)

img = cv2.imread('./Images/bluelego.jpg')
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (1280, 720))  
# cv2.imshow('img', imS)

def empty(a):
    pass
# cv2.namedWindow("HSV")
# cv2.resizeWindow("HSV", framewidth, frameheight)
# cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
# cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
# cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
# cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
# cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
# cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

def getContours(img, imgContours):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(imgContours, contours, -1, (150, 0, 150), 3)
    return contours

img = cv2.imread('./Images/legoref.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsvRange = np.array([[85, 162, 0], [179, 255, 255]])
mask = cv2.inRange(img_hsv, hsvRange[0], hsvRange[1])
hsv_masked = cv2.bitwise_and(img_hsv, img_hsv, mask = mask)

imgContours = hsv_masked.copy()
imgBlur = cv2.GaussianBlur(hsv_masked, (7,7), 1)
imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

threshold1 = 55
threshold2 = 131

imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
# kernel = np.ones((5,5))
imgDil = cv2.dilate(imgCanny, np.ones((5,5)), iterations = 1)

contours = getContours(imgDil, imgContours)

# cv2.imshow('contours', imgDil)
cv2.imwrite('./Images/contours.png', imgDil)
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

        # cv2.rectangle(img, pt1 = (cX - 40, cY-40), pt2 = (cX + 40, cY +40), color = (52, 235, 164), thickness = 5)
        # cv2.putText(img, colour, (cX, cY-110), cv2.FONT_HERSHEY_SIMPLEX, 1, (52, 235, 164), 2)
        # cv2.putText(img, str(cXmm), (cX, cY -80), cv2.FONT_HERSHEY_SIMPLEX, 1, (52, 235, 164), 2)
        # cv2.putText(img, str(cYmm), (cX, cY - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (52, 235, 164), 2)
        cv2.putText(imgContours, colour, (cX, cY - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

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