import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
import PIL
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from geometry_utility import create_rectangle_array, point_intersects

    # Leaving gracefully
class Screen():
    def __init__(self, screen_number=0, screen_size_x=1280, screen_size_y=720):
        self.cap = cv2.VideoCapture(screen_number)
        self.cap.set(3, screen_size_x)
        self.cap.set(4, screen_size_y)
        self.header_index = 0
        self.overlayList = self.setup_header_list()
        self.detector = htm.HandDetector(min_detection_confidence=0.50)
        self.switch_delay = 0
        self.BPM = 100

    def setup_header_list(self, folder_path="header"):
        myList = os.listdir(folder_path)
        overlayList = []

        for imPath in myList:
            image = cv2.imread(f'{folder_path}/{imPath}')
            overlayList.append(image)

        return overlayList

    def draw_controls(self, img):

        cv2.rectangle(img, (1000, 400), (1225, 425), (0, 255, 0), 3)
        cv2.rectangle(img, (1000, 400), (int(self.BPM + 1000), 425), (255, 255, 255), cv2.FILLED)

        cv2.rectangle(img, (1000, 475), (1200, 500), (0, 255, 0), 3)
        cv2.rectangle(img, (1000, 550), (1200, 575), (0, 255, 0), 3)
        cv2.rectangle(img, (1000, 625), (1200, 650), (0, 255, 0), 3)

        return img

    def draw(self, img, lmList):

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
                if y1 < 89:
                    if 0 < x1 < 90:
                        if self.header_index == 0 and self.switch_delay > 10:
                            self.header_index = 1
                            self.switch_delay = 0
                        elif self.switch_delay > 10:
                            self.header_index = 0
                            self.switch_delay = 0

            # Drawing mode
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                print("Drawing Mode")

            point = Point(x1, y1)
            rectangle = create_rectangle_array((1000, 400), (1220, 425))
            if point_intersects(point, rectangle):
                self.BPM = int(x1-1000)



        return img

    def show(self):

        while True:

            # Import the image
            success, img = self.cap.read()
            img = cv2.flip(img, 1)

            # Find hand landmarks
            img = self.detector.findHands(img=img, draw=False)
            for handNumber in range(0, self.detector.handCount()):
                lmList = self.detector.find_position(img, handNumber=handNumber, draw=True)
                img = self.draw(img, lmList)

            header = self.overlayList[self.header_index]
            if self.header_index == 1:
                self.draw_controls(img)

            img[0:header.shape[0], 0:header.shape[1]] = header

            cv2.imshow("Image", img)

            cv2.waitKey(1)
            self.switch_delay += 1
            if self.switch_delay > 500:
                self.switch_delay = 0

if __name__ == "__main__":
    screen = Screen()
    screen.show()