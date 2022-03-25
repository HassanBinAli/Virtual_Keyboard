import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone

from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

Detector = HandDetector(detectionCon=0.8, maxHands=2)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", ""],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        [" "]]
finalText = ""

keyboard = Controller()


def draw_all(image, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        if button.text != "" and button.text != " ":
            cv2.rectangle(image, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
            cv2.putText(image, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                        (255, 255, 255), 4)
        elif button.text != " ":
            cv2.rectangle(image, button.pos, (x + 2*w + 20, y + h), (255, 0, 255), cv2.FILLED)
            cv2.putText(image, "backspace", (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 255, 255), 2)
        else:
            cv2.rectangle(image, button.pos, (x + 5 * w + 20, y + h), (255, 0, 255), cv2.FILLED)
            cv2.putText(image, "space", (x + 100, y + 45), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 255, 255), 2)
    return image


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    hands, img = Detector.findHands(img)
    # hands = Detector.findHands(img, draw=False) # gives the number of hands detected without drawing it
    # lmList, bboxInfo = Detector.find

    img = draw_all(img, buttonList)

    if hands:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            hand = hands[0]
            lm_list = hand["lmList"]   # hand is a dictionary that contains lmlist
            if button.text != "" and button.text != " ":
                if x < lm_list[8][0] < x+w and y < lm_list[8][1] < y+h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                                (255, 255, 255), 4)
                    l, _ = Detector.findDistance(lm_list[8], lm_list[12])

                    if l < 45:
                        #keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                                    (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.2)

            elif button.text != " ":
                if x < lm_list[8][0] < x + 2*w +20 and y < lm_list[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + 2*w + 20, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, "backspace", (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 2)
                    l, _ = Detector.findDistance(lm_list[8], lm_list[12])

                    if l < 45:
                        #keyboard.press("\b")
                        cv2.rectangle(img, button.pos, (x + 2*w +20, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, "backspace", (x + 10, y + 45), cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 255, 255), 2)

                        finalText = finalText[0:-1]
                        sleep(0.2)
            else:
                if x < lm_list[8][0] < x + 5 * w + 20 and y < lm_list[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + 5 * w + 20, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, "space", (x + 100, y + 45), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 2)
                    l, _ = Detector.findDistance(lm_list[8], lm_list[12])

                    if l < 45:
                        #keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + 5 * w + 20, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, "space", (x + 100, y + 45), cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 255, 255), 2)

                        finalText += button.text
                        sleep(0.2)

    cv2.rectangle(img, (50, 450), (1000, 550), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 525), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("", img)
    cv2.waitKey(1)
