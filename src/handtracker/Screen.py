import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
import PIL


    # Leaving gracefully
class Screen():
    def __init__(self, screen_number=0, screen_size_x=1280, screen_size_y=720):
        self.cap = cv2.VideoCapture(screen_number)
        self.cap.set(3, screen_size_x)
        self.cap.set(4, screen_size_y)

        self.detector = htm.HandDetector(min_detection_confidence=0.50)

    def setup_header(self, img, image_index=0, folder_path="header"):
        myList = os.listdir(folder_path)
        overlayList = []

        for imPath in myList:
            image = cv2.imread(f'{folder_path}/{imPath}')
            overlayList.append(image)

        header = overlayList[image_index]
        img[0:header.shape[0], 0:header.shape[1]] = header

        return img

    def draw(self, img, lmList):

        cv2.rectangle(img, (1000, 400), (1200, 425), (0, 255, 0), 3)
        cv2.rectangle(img, (1000, 475), (1200, 500), (0, 255, 0), 3)
        cv2.rectangle(img, (1000, 550), (1200, 575), (0, 255, 0), 3)
        cv2.rectangle(img, (1000, 625), (1200, 650), (0, 255, 0), 3)

        if len(lmList) != 0:

            # Tip of index and middle finger
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            fingers = self.detector.finger_is_open(lmList=lmList)
            # print(fingers)

            # Selection mode, if two fingers are up
            if fingers[1] and fingers[2]:
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 0, 255), cv2.FILLED)
                print("Selection Mode")
                # checking for the click
                if y1 < 106:
                    if 310 < x1 < 401:
                        # header = overlayList[3]
                        self.setup_header(img, 3)
                    elif 465 < x1 < 560:
                        # header = overlayList[0]
                        self.setup_header(img, 0)
                    elif 620 < x1 < 712:
                        # header = overlayList[2]
                        self.setup_header(img, 2)
                    elif 857 < x1 < 933:
                        # header = overlayList[1]
                        self.setup_header(img, 1)
            # Drawing mode
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                print("Drawing Mode")

            # Setting the header image


        return img

    def show(self):


        while True:

            # Import the image
            success, img = self.cap.read()
            img = cv2.flip(img, 1)

            img = self.setup_header(img, 0)
            # Find hand landmarks
            img = self.detector.findHands(img=img, draw=False)
            for handNumber in range(0, self.detector.handCount()):
                lmList = self.detector.find_position(img, handNumber=handNumber, draw=False)
                img = self.draw(img, lmList)

            cv2.imshow("Image", img)

            cv2.waitKey(1)

if __name__ == "__main__":
    screen = Screen()
    screen.show()