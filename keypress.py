import cv2
import numpy as np
from djitellopy import tello
#import time

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()
me.takeoff()
#me.send_rc_control(0,0,25,0)
#time.sleep(2)
w, h = 360,240
pmargemdeerro = 0
maximodere = [5000, 6000]
pid = [0.4, 0.4, 0]
#imagem = tela de captura... VIDEO
#listadecara = onde ira centralizar a face
#listadearea = tela total


def findFace(imagem):
    faceCascade = cv2.CascadeClassifier("K:\TRELLO\haarcascade_frontalface_alt.xml")
    imgGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.1, 8)

    listadecara = []
    listadearea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(imagem , (x ,y), (x + w, y + h), (0,0,255), 2)
        centralx = x + w//2
        centraly = y + w//2
        area = w * h
        cv2.circle(imagem,(centralx,centraly),5,(0,255,0),cv2.FILLED)
        listadecara.append([centralx,centraly])
        listadearea.append(area)
    if len(listadearea) !=0:
        i = listadearea.index(max(listadearea))
        return imagem, [listadecara[i],listadearea[i]]
    else:
        return imagem [[0 , 0], 0]

def RastreamentoDeFace(info, w, pid, pmargemdeerro):
    area = info [1]
    x,y = info [0]
    dere = 0

    margemdeerro = x - w//2
    velocidade = pid[0] * margemdeerro + pid [1] * (margemdeerro - pmargemdeerro)
    velocidade = int(np.clip(velocidade,-100,100))


    if area > maximodere[0] and area < maximodere [1]:
        dere = 0
    if area > maximodere[2]:
        dere= -20
    elif area < maximodere[0] and area !=0 :
        dere = 20

    if x == 0:
        velocidade = 0
        margemdeerro = 0

    me.send_rc_control(0, dere, 0, velocidade)
    return margemdeerro


#captura = cv2.VideoCapture(1)
while True:
    imagem = me.get_frame_read().frame
    #_, imagem = captura.read()
    imagem = cv2.resize(imagem, (w,h))
    imagem, info = findFace(imagem)
    pmargemdeerro = RastreamentoDeFace(info, w, pid, pmargemdeerro)
    #print("central", [0] , "AREA" , info[1])
    cv2.imshow("TELINHA", imagem)
    if cv2.waitkey(1) & 0xFF == ord('q'):
        me.land()
        break
