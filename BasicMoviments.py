# código destinado ao entendimento dos comandos básicos para o DJI Tello
# de modo geral, essa forma de enviar comandos gera um erro considerável na trajetória do drone
# teoricamente, nesse código, o drone deveria ir para frente e para trás voltando para o mesmo ponto inicial
# contudo, isso não acontece e existe um erro considerável

from djitellopy import tello # biblioteca para o DJI Tello
from time import sleep

me = tello.Tello() # criando objeto como sendo o drone
me.connect() # conectando o drone
print(me.get_battery()) # imprimindo a porcentagem de bateria do drone

me.takeoff() # decolagem do drone

me.send_rc_control(0, 50, 0, 0)
sleep(2) # vai para frente por 2 segundos
me.send_rc_control(0, -50, 0, 0)
sleep(2) # vai para trás por 2 segundos

me.land() # aterrissagem do drone

