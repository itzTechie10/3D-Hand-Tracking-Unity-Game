import math
import socket

import cv2
from cvzone.HandTrackingModule import HandDetector

# parameters
width, height = 1280, 720

#webcam

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)


#Hand Detector

detector = HandDetector(maxHands=2, detectionCon=0.8)

# communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    #get frame from webcam
    success, img = cap.read()
    #hands
    hands, img = detector.findHands(img)

    data = []
    data1 = []
    data2 = []
    flag = False


    # landmark values - (x,y,z) * 21
    if hands:
        # get the first hand  detected
        hand = hands[0]

        # get the landmark list
        lmList = hand["lmList"]

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            #print(lmList2)

            for lm in lmList2:
                data1.extend([lm[0], height - lm[1], lm[2]])
            #print("data1: ",data1)


        #print(lmList)

        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])

        data2 = data + data1
        data2.append(len(hands))

        print(data2)

        #print("data: ",data)
        sock.sendto(str.encode(str(data2)), serverAddressPort)

    if(len(hands) == 0):
        sock.sendto(str.encode(str(0)), serverAddressPort)


    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)