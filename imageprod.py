import cv2 
import matplotlib.pyplot as plt
import numpy as np
import colourclassification as cc

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(imgContours, contours, -1, (150, 0, 150), 3)
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    return sorted_contours

hsvRange = np.array([[0, 91, 62], [107, 255, 255]])
img = cv2.imread('./Images/Test Data/test1.jpg')
img = cv2.resize(img, (1920, 1080))  
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, hsvRange[0], hsvRange[1])
out = cv2.bitwise_and(hsv, hsv, mask = mask)
res = cv2.cvtColor(out, cv2.COLOR_HSV2BGR)

imgContours = out.copy()
imgBlur = cv2.GaussianBlur(out, (7,7), 1)
imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)


threshold1 = 97
threshold2 = 255

imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
# kernel = np.ones((5,5))
imgDil = cv2.dilate(imgCanny, np.ones((5,5)), iterations = 1)

contours = getContours(imgDil)
for c in contours:
        # if 1200  < cv2.contourArea(c) < 1500:
        if cv2.contourArea(c) > 200:
            # print(cv2.contourArea(c))
            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))

            # print(cX, cY)
            pixel = img[cY, cX, :]

            # cYmm = round(ct.y_mm(cY))
            # cXmm = round(ct.x_mm(cX))
            # cYcm = cY * cm2pixel
            # cXcm = cX * cm2pixel
            # position = np.array([cXcm, cYcm, 0, 1])[np.newaxis].T
            # coordsBaseFrame = transformation @ position
            # x = math.floor(coordsBaseFrame[0] * 10) 
            # y = math.floor(coordsBaseFrame[1] * 10)
            # print(pixel)
            cv2.circle(img, center = (cX, cY), radius = 2, color = (0,0,0), lineType = 10)
            colour = cc.get_colour_knn(pixel)

            # lego.update(colour, coordsBaseFrame)
            # pick_lego()

            cv2.rectangle(img, pt1 = (cX - 40, cY-40), pt2 = (cX + 40, cY +40), color = (52, 235, 164), thickness = 1)
            cv2.putText(img, colour, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            # cv2.putText(img, str(cXmm), (cX, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            # cv2.putText(img, str(cYmm), (cX, cY + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 235, 164), 2)
            cv2.putText(imgContours, colour, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            # print(img.shape, (cX, cY))
            # imgStack = stackImages(0.8, ([img, imgBlur, imgGray]))
            # imgStack = np.hstack([[img], [imgBlur], [imgCanny]])
            cv2.imshow("image", img)
            cv2.imshow("blurred", imgContours)
            cv2.imshow("gray", imgDil)
# cv2.imshow('res', res)
# cv2.imwrite('./Images/labeltest.png', img)

cv2.waitKey(0)
cv2.destroyAllWindows()