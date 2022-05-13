from random import random
import cv2
import numpy as np
import math
import random
import cvzone

class snake_class():
    def __init__(self, path_food):
        self.points = []    # all points of the snake
        self.lengths = []   # distance between each point
        self.current_length = 0     # current length of the snake
        self.allow_length = 150     # total allowed length
        self.previous_head = 0,0    # previous head point

        self.food_path = cv2.imread(path_food, cv2.IMREAD_UNCHANGED)
        self.heigh, self.width,_ = self.food_path.shape
        self.food_point = 0,0
        self.random_food()

        self.score = 0
        self.game_over = False
        

    def random_food(self):
        self.food_point = random.randint(100,1000), random.randint(100,600)

    def update(self, img_main, current_head):

        if self.game_over:
            cvzone.putTextRect(img_main, 'Game Over', [300,300], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(img_main, f'Your score: {self.score}', [300,450], scale=7, thickness=5, offset=20)
    
        else:
            px, py = self.previous_head

            cx, cy = current_head

            self.points.append([cx,cy])

            distance = math.hypot(cx-px, cy-py)

            self.lengths.append(distance)

            self.current_length += distance

            self.previous_head = cx,cy

            # reduce length
            if self.current_length > self.allow_length:
                for i, length in enumerate(self.lengths):
                    self.current_length -= length
                    self.lengths.pop(i)
                    self.points.pop(i)

                    if self.current_length <= self.allow_length:
                        break

            # check eat
            rx, ry = self.food_point

            if rx - self.width//2 < cx < rx + self.width//2 and\
                ry - self.heigh//2 < cy < ry + self.heigh//2:
                # print('ate')
                self.random_food()
                self.allow_length += 50
                self.score += 1
                print(self.score)

            # draw snake
            if self.points:
                for i,point in enumerate(self.points):
                    if i != 0:
                        cv2.line(img_main, self.points[i-1], self.points[i], (0,255,0), 20)

                cv2.circle(img_main, self.points[-1], radius=20, color=(255,255,0), thickness=cv2.FILLED)

            # draw food
            img_main = cvzone.overlayPNG(img_main, self.food_path, (rx-self.width//2,ry-self.heigh//2))

            cvzone.putTextRect(img_main, f'Your score: {self.score}', [50,50], scale=3, thickness=3, offset=10)

            # check hit
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img_main, [pts], False, (255,0,255), 3)
            min_dis = cv2.pointPolygonTest(pts, (cx,cy), True)

            if -1 <= min_dis <= 1:
                print('Hit')
                self.game_over = True

                self.points = []    # all points of the snake
                self.lengths = []   # distance between each point
                self.current_length = 0     # current length of the snake
                self.allow_length = 150     # total allowed length
                self.previous_head = 0,0    # previous head point
                # self.score = 0

        return img_main

