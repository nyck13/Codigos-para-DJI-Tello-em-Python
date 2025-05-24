# esse projeto é basicamente a concatenação dos códigos KeyboardControl.py e ImageCapture.py
# o projeto basicamente busca fazer o controle do drone pelo teclado e capturar fotos em tempo real

from djitellopy import tello
import KeyPressModule as kp
import time
import cv2

kp.init()

me = tello.Tello()
me.connect()
print(me.get_battery())
global img
me.streamon() # ativa a transmissão de imagens

def getKeyboardInput():
    lr, fb, up, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey('LEFT'): lr = -speed
    elif kp.getKey('RIGHT'): lr = speed

    if kp.getKey('UP'): fb = speed
    elif kp.getKey('DOWN'): fb = -speed

    if kp.getKey('w'): up = speed
    elif kp.getKey('s'): up = -speed

    if kp.getKey('a'): yv = -75
    elif kp.getKey('d'): yv = 75

    if kp.getKey('q'):
        me.land()
    if kp.getKey('e'):
        me.takeoff()

    # função para fazer a captura das imagens e enviar para uma pasta no computador
    if kp.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3) # delay necessário para que o drone não registre várias fotos

    return [lr, fb, up, yv]

while True:
    values = getKeyboardInput()

    img = me.get_frame_read().frame # captura o frame
    img = cv2.resize(img, (360, 240)) # altera o tamanho da imagem para melhorar o processamento
    cv2.imshow('Image', img) # cria a janela de visualização
    cv2.waitKey(1)

    me.send_rc_control(values[0], values[1], values[2], values[3])