from machine import Pin
from utime import sleep_ms
import network
import gc
try:
    import usocket as socket
except:
    import socket

"""
Librería estandar para manejo de red local wifi
Creada como protocol estandar en el salón de proyectos digitales avanzados
para evitar los problemas de comunicación experimentados hasta la fecha

Permite crear una zona wifi con el raspberry pico w o ingresar a una red ya creadas
También mantiene registro de las redes conocidas

Creado por Andrés Goncalves.
Fecha: 24/1/2024.
"""

NOMBRE_DE_LA_RED_LOCAL = 'Pico-W-Andres'
CLAVE_DE_LA_RED_LOCAL = '123456789'

gc.collect()

def leer(tope):
    entrada = 0
    primera_vuelta=True
    while ((not isinstance(entrada, int)) or (not (entrada > 0 and entrada <= tope))):
        if not primera_vuelta:
            print("Ingrese una opción válida")
        try:
            entrada = int(input())
        except Exception:
            print("Ingrese una opción válida")
        primera_vuelta = False
    return entrada

def guardar_redes(lista):
    try:
        archivo = open("RedesWifi.txt", "w")
        
        for linea in lista:
            try:
                archivo.write(str(linea[0]) + " " + str(linea[1]) + '\n')
            except:
                print("Error al escribir")

        archivo.close()
    except:
        print("No se pudo sobrescribir el archivo")
    
class Red_local:
    
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        self.led.off()
    
    def Inicio(self):
        
        print("")
        print("¿Que desea hacer?")
        print("1- Crear red")
        print("2- Unirse a una red?")
        
        opcion = leer(2)

        if opcion == 1:
            R.Crear_red()
        else:
            R.Unirse_red()

    def Crear_red(self):
    
        """
        Crea una red con los parametro establecidos en las contantes:
        NOMBRE_DE_LA_RED_LOCAL
        CLAVE_DE_LA_RED_LOCAL
        
        En las líneas 22 y 23 respectivamente
        """
        
        nombre = NOMBRE_DE_LA_RED_LOCAL
        clave = CLAVE_DE_LA_RED_LOCAL

        self.red = network.WLAN(network.AP_IF)
        #Hard reset
        self.red.disconnect()
        self.red.deinit()
        self.red = network.WLAN(network.AP_IF)
        #--------------------------------------

        self.red.config(essid=nombre, password=clave)
        self.red.active(True)

        while self.red.active() == False:
          pass

        print("")
        print(self.red.ifconfig())
        print(self.red.config('ssid'))
        print("")

        self.led.on()

    def Unirse_red(self):
    
        """
        Escanea las redes wifi disponibles y permite escoger la red de preferencia
        Adicionalmente almacena las redes con sus claves correspondientes para futuras conexiones
        """

        self.red = network.WLAN(network.STA_IF)
        #Hard reset
        self.red.disconnect()
        self.red.deinit()
        self.red = network.WLAN(network.STA_IF)
        #--------------------------------------
        self.red.active(True)
        
        redes_disponibles_aux = self.red.scan()
        redes_disponibles = []
        cont = 1
        
        print("")
        print("Escoja la red a la que desea unirse:")
        
        for i in redes_disponibles_aux:
            aux = str(i[0],"utf-8")
            if not aux == "":
                print(str(cont)+"- "+aux)
                redes_disponibles.append(aux)
                cont+= 1
        
        entrada = leer(len(redes_disponibles))
        print("")
        
        nombre = redes_disponibles[entrada-1]
        clave = ""
        
        lista_redes_guardadas = []
        
        try:
            archivo = open("RedesWifi.txt", "r")
            aux = archivo.read()
            archivo.close()
            
            lista_redes_guardadas = []
            for linea in aux.split("\n"):
                if linea == "":
                    continue
                lista_redes_guardadas.append(linea.split(" "))
                
            for n in lista_redes_guardadas:
                if n[0] == nombre:
                    clave = n[1]
        except:
            print("",end="")
                
        while self.red.isconnected() == False:
            
            if clave == "":
                print("Ingrese contraseña")
                clave = input()
                print("")

            self.red.connect(nombre, clave)
            
            cont = 0
            while self.red.isconnected() == False:
                print('Conectando', end="")
                sleep_ms(100)
                cont += 1
                for i in range(3):
                    print('.',end="")
                    sleep_ms(100)
                    cont += 1
                print("")
                if cont >= 150:
                    clave = ""
                    print("La clave guardada no parece ser correcta")
                    break

        print('Conexión exitosa')
        print(self.red.ifconfig())
        
        actualizado = False
        
        for i in range(len(lista_redes_guardadas)):
            if lista_redes_guardadas[i][0] == nombre:
                lista_redes_guardadas[i][1] = clave
                actualizado = True
                
        if not actualizado:
            lista_redes_guardadas.append([nombre,clave])
        
        guardar_redes(lista_redes_guardadas)
                
        self.led.on()