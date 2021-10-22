import cv2
import numpy as np

framewidth = 1920
frameheight = 1080

cap = cv2.VideoCapture(0)
if (cap.isOpened()== False): 
    print("Error opening video  file")
cap.set(3, framewidth)
cap.set(4, frameheight)

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", framewidth, frameheight)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)


# h_min = 0
# h_max = 115
# s_min = 42
# s_max = 255
# v_min = 130
# v_max = 255
while True:
    ret, frame = cap.read()
    if ret == True:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("HUE Min", "HSV")
        h_max = cv2.getTrackbarPos("HUE Max", "HSV")
        s_min = cv2.getTrackbarPos("SAT Min", "HSV")
        s_max = cv2.getTrackbarPos("SAT Max", "HSV")
        v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
        v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(frameHSV, lower, upper)
        result = cv2.bitwise_and(frameHSV, frameHSV, mask = mask)


        cv2.imshow('Original', frame)
        # cv2.imshow('HSV Colour Space', frameHSV)
        # cv2.imshow("Mask", mask)
        cv2.imshow("Result", result)
        out = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

        mask = cv2.cvtColor(mask ,cv2.COLOR_GRAY2BGR)
        cv2.imshow('masked', out)
        # hstack = np.hstack([frame, mask, result])
        # cv2.imshow("Horizontal Stack", hstack)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()