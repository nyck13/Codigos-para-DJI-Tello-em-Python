# para entendimento desse scrip, é necessário acessar o KeyPressModule.py
# por meio desse script, é possível controlar o DJI Tello por meio do teclado

from djitellopy import tello
import KeyPressModule as kp

kp.init() # inicializa o KeyPressModule.py

me = tello.Tello()
me.connect()
print(me.get_battery())

def getKeyboardInput():
    lr, fb, up, yv = 0, 0, 0, 0 # define as velocidades iniciais em todas as direções como 0
    speed = 50 # define a velocidade que o drone assume como 50

    # a lógica para o controle do drone é explicada nas duas próximas linhas e o controle nas outras direções é similar
    if kp.getKey('LEFT'): lr = -speed # caso a tecla LEFT esteja pressionada, define a velocidade como 50 para esquerda
    elif kp.getKey('RIGHT'): lr = speed # caso a primeira condição não seja válida, verifica-se a segunda para definir a velocidade para direita

    if kp.getKey('UP'): fb = speed
    elif kp.getKey('DOWN'): fb = -speed

    if kp.getKey('w'): up = speed
    elif kp.getKey('s'): up = -speed

    if kp.getKey('a'): yv = -speed
    elif kp.getKey('d'): yv = speed

    if kp.getKey('q'): # se a tecla q for pressionada, o drone decola
        me.land()
    if kp.getKey('e'): # se a tecla e for pressionada, o drone aterrissa
        me.takeoff()

    # os comandos "q" e "e" podem apresentar bugs, uma vez que o drone só aterrissa se tiver decolado
    # além disso, só decola se não estiver já decolado

    return [lr, fb, up, yv] # a função getKeyboardInput retorna as velocidades translancionais e rotacionais

while True: # loop infinito para senmpre estar mandando comandos para o drone
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])