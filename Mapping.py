# esse projeto permite controlar o drone por meio do teclado, enquanto possui uma versão virtual em paralelo
# a versão virtual teórica permite rastrear a posição do drone em um mapa

from djitellopy import tello
import KeyPressModule as kp
import numpy as np
from time import sleep
import cv2
import math

###################### PARÂMETROS ######################

fSpeed = 117/10 # Velocidade frontal em cm/s (15cm/s)
aSpeed = 360/10 # Velocidade angular em graus/s (50graus/s)
interval = 0.25

dInterval = fSpeed*interval # distância instantânea percorrida pelo drone
aInterval = aSpeed*interval # ângulo instantâneo percorrido pelo drone

########################################################

x, y = 500, 500 # posição incial do drone virtual
a = 0
yaw = 0

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

points = [(0,0), (0,0)] # inicializa a referência para o drone

def getKeyboardInput():
    lr, fb, up, yv = 0, 0, 0, 0
    speed = 15 # velocidade do drone
    aSpeed = 50 # velocidade angular do drone
    global yaw, x, y, a
    d = 0

    # de forma geral, quando se pressiona a tecla, é enviado um comando para o drone físico e o drone virtual
    # o drone físico não executa exatamente o mesmo comando que o virtual, uma vez que existe um erro considerável
    # o drone virtual altera os valores dos seus paramêtros toda vez que uma tecla é pressionada

    if kp.getKey('LEFT'):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey('RIGHT'):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey('UP'):
        fb = speed
        d = dInterval
        a = 270
    elif kp.getKey('DOWN'):
        fb = -speed
        d = dInterval
        a = -270

    if kp.getKey('w'):
        up = speed
    elif kp.getKey('s'):
        up = -speed

    if kp.getKey('a'):
        yv = -aSpeed
        yaw -= aInterval

    elif kp.getKey('d'):
        yv = aSpeed
        yaw += aInterval

    if kp.getKey('q'):
        me.land()
    if kp.getKey('e'):
        me.takeoff()

    sleep(interval)
    a += yaw # define o novo ângulo do drone
    x += int(d*math.cos(math.radians(a))) # define a posição em x do drone por meio da multiplicação da distância percorrida pelo cosseno do ângulo
    y += int(d*math.sin(math.radians(a))) # define a posição em y do drone por meio da multiplicação da distância percorrida pelo seno do ângulo

    return [lr, fb, up, yv, x, y] # retorna os atributos do drone e sua posição atual

# função para mapear a trajetória do drone
def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0,0,225), cv2.FILLED)
    cv2.circle(img, points[-1], 5, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0]-500)/100}, {(points[-1][1]-500)/100})m',
                (points[-1][0]+10, points[-1][1]+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

while True:
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    if (points[-1][0] != values[4] or points[-1][1] != values[5]):
        points.append((values[4], values[5]))
    drawPoints(img, points)
    cv2.imshow('Output', img)
    cv2.waitKey(1)