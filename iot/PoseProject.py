from threading import active_count
import cv2
import mediapipe as mp
import time 
import bodymin as bm
import numpy as np
import random
import time
from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 1883
topic = "esp∕exercicio/led"
client_id = 'clientId-dZHZ88maBh2'
username = 'JULIA'
password = '35211932'
count = 0
dir = 0

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, msg):

    time.sleep(1)
    msg = f"{msgLed}"
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
         print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


client = connect_mqtt()
client.loop_start()
active = True
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
detector = bm.poseDetector()
while True:
    sucess, img = cap.read()
    img = detector.findPose(img, False)
    lmList = detector.getPosition(img, False)
    if len(lmList) != 0:   
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (220, 300), (0, 100))
        bar = np.interp(angle, (220, 300), (650, 100))
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0 :
                count += 0.5
                dir= 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1 :
                count += 0.5
                dir= 0
        if count == 1 and active:
            msgLed = 'ON'
            active = False
            publish(client, msgLed)
        if count == 10 and active == False:
            msgLed = 'OFF'
            publish(client, msgLed)
            active = True

        #draw bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN,
                       4, color, 4)
       
        #draw curl count
        #cv2.rectangle(img, (0, 450), (250, 720), (0, 255,0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN,
                       15, (255, 0, 0), 25)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)