from FF_libreria import Flipflop, Xor, Cable, Entrada, Salida
from Red_local import Red_local
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import socket
import usocket

#Pantalla
WIDTH=128
HEIGHT=64
i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT,i2c)
#-------------------------------------

#Grafica
def graficar(entrada, salida):
    oled.fill(0)
    oled.text("Encriptado:",0,0)
    oled.text(entrada,0,8)
    oled.text("Original:",0,32)
    oled.text(salida,0,40)
    oled.show()
#-------------------------------------
    
R = Red_local()
R.Crear_red()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    aux = str(request,"utf-8")
    inicio = aux
    conn.sendall(str("exito"))
    conn.close()

    print(inicio)
    entrada = Entrada(inicio)

    C1 = Cable([])
    C2 = Cable([])
    C3 = Cable([])
    C4 = Cable([])

    X1 = Xor([C2,C4])
    X2 = Xor([X1,C1])

    D1 = Flipflop(C1,1)
    D2 = Flipflop(C2,0)
    D3 = Flipflop(C3,1)

    ff = [D1,D2,D3]

    C1.entradas = [entrada]
    C2.entradas = [D1]
    C3.entradas = [D2]
    C4.entradas = [D3]

    salida = Salida(X2)


    while True:
        salida.leer_valor()
        for f in ff:
            f.buffer()
        for f in ff:
            f.actualizar()
        if not entrada.siguiente():
            break

    fin = salida.get()

    print(fin)
    print("")
    graficar(inicio, fin)
    