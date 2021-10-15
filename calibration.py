import cv2
import numpy as np

# framewidth = 640
# frameheight = 400

framewidth = 720
frameheight = 480

# cap = cv2.VideoCapture(0)
# if (cap.isOpened()== False): 
#   print("Error opening video  file")
# cap.set(3, framewidth)
# cap.set(4, frameheight)

img = cv2.imread('./Images/legoref.jpg')
img = cv2.resize(img, (1920, 1080))
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

# while True:
# frameHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# h_min = cv2.getTrackbarPos("HUE Min", "HSV")
# h_max = cv2.getTrackbarPos("HUE Max", "HSV")
# s_min = cv2.getTrackbarPos("SAT Min", "HSV")
# s_max = cv2.getTrackbarPos("SAT Max", "HSV")
# v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
# v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

# lower = np.array([h_min, s_min, v_min])
# upper = np.array([h_max, s_max, v_max])

# mask = cv2.inRange(frameHSV, lower, upper)
# result = cv2.bitwise_and(frameHSV, frameHSV, mask = mask)
# cv2.imshow('Original', img)
# cv2.imshow('HSV Colour Space', frameHSV)
# if cv2.waitKey(30) & 0xFF == ord('q'):
#     cv2.destroyAllWindows()

# while True:
#     ret, frame = cap.read()
#     print(frame.shape)
#     if ret == True:
#         # frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#         cv2.imshow("image" , frame)

#         h_min = cv2.getTrackbarPos("HUE Min", "HSV")
#         h_max = cv2.getTrackbarPos("HUE Max", "HSV")
#         s_min = cv2.getTrackbarPos("SAT Min", "HSV")
#         s_max = cv2.getTrackbarPos("SAT Max", "HSV")
#         v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
#         v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

#         # lower = np.array([h_min, s_min, v_min])
#         # upper = np.array([h_max, s_max, v_max])

#         # mask = cv2.inRange(frameHSV, lower, upper)
#         # result = cv2.bitwise_and(frameHSV, frameHSV, mask = mask)


#         # cv2.imshow('Original', frame)
#         # cv2.imshow('HSV Colour Space', frameHSV)
#         # cv2.imshow("Mask", mask)
#         # cv2.imshow("Result", result)

#         # mask = cv2.cvtColor(mask ,cv2.COLOR_GRAY2BGR)
#         # hstack = np.hstack([frame, mask, result])
#         # cv2.imshow("Horizontal Stack", hstack)

#         if cv2.waitKey(30) & 0xFF == ord('q'):
#             break