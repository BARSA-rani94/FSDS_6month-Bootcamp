#OBJECT DETECTION USING OPENCV



import cv2 # package of AI
import numpy as np


cap = cv2.VideoCapture(0)

#Lets load the frame
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #blue color
    low_blue=np.array([94,80,2])
    high_blue=np.array([126,255,255])   
    

    #mask=cv2.inRange(hsv_frame, low_red, high_red)
    blue_mask=cv2.inRange(hsv_frame, low_blue, high_blue)
    blue=cv2.bitwise_and(frame, frame, mask=blue_mask)
   
# Lets frame on the windows  
    cv2.imshow("Frame", frame)
    cv2.imshow("Blue Color Detection", blue)
   
# weight key event which is 1 and which is 27 then break the loop that means we are going to stop the loop
    key = cv2.waitKey(1)
    if key == 27:
        break

