# módulo criado para capturar a tecla apertada no teclado e enviar para o drone

import pygame

# criação da janela do pygame, os comandos só funcionam quando essa janela está ativa
def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))

# função para captura da tecla pressionada
def getKey(keyName):
    ans = False
    for event in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()

    return ans

def main():
    print(getKey('LEFT'))

if __name__ == '__main__':
    init()
    while True:
        main()

