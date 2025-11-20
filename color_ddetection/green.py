#OBJECT DETECTION USING OPENCV


import cv2 # package of AI
import numpy as np

#Lets capture the camera. 0 for webcam. if you want other webcam then we can change to index to 1, 2
cap = cv2.VideoCapture(0)

#Lets load the frame
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #green color
    low_green=np.array([40,70,70])  
    high_green=np.array([80,255,255])

    #mask=cv2.inRange(hsv_frame, low_green, high_green)
    green_mask=cv2.inRange(hsv_frame, low_green, high_green)
    green   =cv2.bitwise_and(frame, frame, mask=green_mask)

   
   
# Lets frame on the windows  
    cv2.imshow("Frame", frame)
    cv2.imshow("Green Color Detection", green)
   

    key = cv2.waitKey(1)
    if key == 27:
        break

