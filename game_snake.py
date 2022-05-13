# https://www.youtube.com/watch?v=w26Ze6lP02Y

import cvzone
import cv2
import numpy
from cvzone.HandTrackingModule import HandDetector
from snake import snake_class


url = 0
camera = cv2.VideoCapture(url)
camera.set(3,2080)
camera.set(4,720)

detector = HandDetector(detectionCon = 0.8, maxHands = 1)

food_path = 'D:\ANSON\DATN\code\snake\\banana.png'

game = snake_class(food_path)

while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame,1)

    if not ret:
        cv2.waitKey(10)
        
        camera.release()
        cv2.destroyAllWindows()
        break
    
    hands, frame = detector.findHands(frame, flipType=False)

    if hands:
        lmList = hands[0]['lmList']

        pointIndex = lmList[8][0:2]

        frame = game.update(frame, pointIndex)


    cv2.imshow('Snake',frame)

    k = cv2.waitKey(10) & 0xFF

    if k == ord('r'):
        game.game_over = False
        game.score = 0
    elif k == 27: 
        break

camera.release()
cv2.destroyAllWindows()