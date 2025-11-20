#OBJECT DETECTION USING OPENCV



import cv2 # package of AI
import numpy as np


cap = cv2.VideoCapture(0)

#Lets load the frame
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Every colour
    low=np.array([0,42,0])
    high=np.array([179,255,255])
    

    #mask=cv2.inRange(hsv_frame, low_red, high_red)
    mask=cv2.inRange(hsv_frame, low, high)
    result=cv2.bitwise_and(frame, frame, mask=mask)
   
# Lets frame on the windows  
    cv2.imshow("Frame", frame)
    cv2.imshow("Result",result)
   
# weight key event which is 1 and which is 27 then break the loop that means we are going to stop the loop
    key = cv2.waitKey(1)
    if key == 27:
        break



