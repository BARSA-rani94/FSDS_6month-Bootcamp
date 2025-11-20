#OBJECT DETECTION USING OPENCV



import cv2 # package of AI
import numpy as np


cap = cv2.VideoCapture(0)

#Lets load the frame
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #red color
    low_red = np.array([161, 155, 84]) # lowest hue would be - 161,155,84( how do i found this i tested before and found this)
    high_red = np.array([179, 255, 255])

    #mask for red color
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)


   
   
# Lets frame on the windows  
    cv2.imshow("Frame", frame)
   
    cv2.imshow('Red', red)
    key = cv2.waitKey(1)
    if key == 27:
        break












