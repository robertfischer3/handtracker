import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

folderPath = "header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandDetector(min_detection_confidence=0.50)
while True:

    # Import the image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hand landmarks
    img = detector.findHands(img=img, draw=False )

    for handNumber in range(0, detector.handCount()):
        lmList = detector.find_position(img, handNumber=handNumber, draw=False)
        if len(lmList) != 0:

            # Tip of index and middle finger
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            fingers = detector.finger_is_open(lmList=lmList)
            # print(fingers)

    # Selection mode, if two fingers are up
            if fingers[1] and fingers[2]:
                cv2.rectangle(img, (x1, y1-25), (x2, y2+25), (255, 0, 255), cv2.FILLED)
                print("Selection Mode")
    # Drawing mode
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                print("Drawing Mode")
    # Setting the header image
    img[0:107, 0:1012]=header

    cv2.imshow("Image", img)

    cv2.waitKey(1)
    # Leaving gracefully
