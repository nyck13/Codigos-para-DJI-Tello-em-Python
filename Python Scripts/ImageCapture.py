# código utilizado para capturar a imagem ao vivo gerado pela camêra do DJI Tello

from djitellopy import tello
import cv2

me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon() # ativa a visualização em tempo real

while True:
    img = me.get_frame_read().frame # captura o frame
    img = cv2.resize(img, (360, 240)) # altera o tamanho da imagem para melhorar o processamento
    cv2.imshow('Image', img) # cria a janela de visualização
    cv2.waitKey(1)