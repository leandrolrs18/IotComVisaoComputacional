import cv2 
import mediapipe as mp
import time
import math

class poseDetector ():
    def __init__(self, mode = False, upBody = False, smooth = True, 
                detectionCon = 0.5, trackCon = 0.5):
        #inicialmente ao chamar essa classe, essas variaveis é criada pro usuario. Por exemplo, ao chamar a handDetector
        # mp.solutions.hands já criado
        # n posso ultilizar o parametro direto, primeiro é criado variaveis self.x com o parametro que pode ser usadas dentro da função
        # como se estivesse fazendo uma cópia, 
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpPose= mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody,
                                       self.smooth, self.detectionCon, self.trackCon)                    #objeto/classe que detecta mãos
        self.mpDraw = mp.solutions.drawing_utils                                            #objeto/classe que desenha a classe self.hands  

    def findPose (self, img, draw=True):
        imgRGB = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)                                      #convertendo para RGB
        self.results = self.pose.process (imgRGB)                                               # nessa acredito que pega a posição?

        if self.results.pose_landmarks:                                                    # para cada mão achada
            #for handLms in results.multi_hand_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,                                #desenha na img original as conexões dos pontos achados
                                            self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition (self, img, draw=True):

        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate (self.results.pose_landmarks.landmark):                                      #para cada mão achada pegar o id e lm dessa posição
                h, w, c = img.shape                                                         
                cx, cy = int (lm.x*w), int(lm.y*h)                                          # o valor do lm é em 0.8 etc, precisa da conversão
                self.lmList.append([id, cx, cy])                                    
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)                # desenha um circulo 
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        #get landmarks
        x1, y1 =self.lmList[p1][1:]
        x2, y2 =self.lmList[p2][1:]
        x3, y3 =self.lmList[p3][1:]

        #Calculate the Angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2(y1-y2, x1-x2))
        
        if angle < 0:
            angle += 360
        #print(angle)

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), 2)
            #cv2.putText(img, str(int(angle)), (x2-50, y2+50), cv2.FONT_HERSHEY_PLAIN,
             #           2, (0, 0, 255), 2)
        return angle