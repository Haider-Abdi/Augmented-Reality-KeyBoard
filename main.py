import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.5)
keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        [" ", "+", "-", "*", "!", "(", ")", "@", "&", "#"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""
keyboard = Controller()
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        #cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
         #                 20, rt=0)
        cv2.rectangle(img, button.pos, (x + w-30, y + h-30), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 5, y + 25),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    return img
# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
#                       (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0.5
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#     return out


class Button():
    def __init__(self, pos, text, size=[65, 65]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([60 * j+10, 60 * i+10], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5-30, y + h + 5-30), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20-15, y + 65-40),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                ## when clicked
                if l < 30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w-30, y + h-30), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20-15, y + 65-40),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    finalText += button.text
                    sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
