#import necessary libraries
import cv2
import numpy as np
import time
#initialize the video stream
cap = cv2.VideoCapture(0)

#make two arrays, one for the points, and another for the timings
points = []
timer = []
while True:
    #start the timing
    startime = time.time()

    #append the start time to the array named 'timer'
    timer.append(g)

    #you only want to use the start time, so delete any other elements in the array
    del timer[1:]
    _, frame = cap.read()

    #resize and blur the frame (improves performance)
    sized = cv2.resize(frame, (600, 600))
    frame = cv2.GaussianBlur(sized, (7, 7), 0)

    #convert the frame to HSV and mask it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hlow = 17
    slow = 150
    vlow = 24
    hhigh = 78
    shigh = 255
    vhigh = 255
    HSVLOW  = np.array([hlow, slow, vlow])
    HSVHIGH = np.array([hhigh, shigh, vhigh])
    mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(frame,frame, mask =mask)

    #create an edged frame of the thresholded frame
    edged = cv2.Canny(res, 50, 150)

    #find contours in the edged frame and append to the 'cnts' array
    cnts = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    # if contours are present
    if len(cnts)> 0:

        #find the largest contour according to their enclosed area
        c = max(cnts, key=cv2.contourArea)

        #get the center and radius values of the circle enclosing the contour
        (x, y), radius = cv2.minEnclosingCircle(c)
        centercircle = (int(x), int(y))
        radius = int(radius)
        cv2.circle(sized, centercircle, radius, (255, 30,255), 2) #this circle is the object
        cv2.circle(sized, centercircle, 5, (0, 0, 255), -1) #this circle is the moving red dot
        points.append(centercircle) #append this dot to the 'points' list
        if points is not None:
            for centers in points:
                cv2.circle(sized, centers, 5, (0, 0, 255), -1) #make a dot for each of the points

    #show all the frames and cleanup
    cv2.imshow('frame', sized)
    cv2.imshow('mask', res)
    k = cv2.waitKey(5) & 0xFF
    g = time.time()
    timer.append(g)

    #if 10 seconds have passed, erase all the points
    delta_t = timer[1] - timer[0]
    if delta_t >= 10:
        del timer[:]
        del points[:]
    if k == 27:
        break
