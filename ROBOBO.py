# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'robobo.py'))

from Robobo import Robobo
from utils.LED import LED
from utils.Color import Color
from utils.IR import IR
from utils.Emotions import Emotions
from utils.Sounds import Sounds

robobo = Robobo('10.113.36.183')
robobo.connect()

senal=None
brazo=None
valido=None
robobo.setActiveBlobs(False,True,False,True)

def brazo_baxter_callback():

    final= robobo.readQR().id
    print (final)
    print(senal)
    
    if final == senal and brazo =='derecho':
        robobo.stopMotors()
        robobo.sayText('Los objetos de color verde debo dejarlos en el brazo derecho del Baxter')
        robobo.movePanTo(90,30)
        robobo.moveWheelsByTime(-5,-5,3)
        robobo.moveWheelsByTime(-8,8,2) 
        robobo.moveWheels(5,5)

    elif final == senal and brazo =='izquierdo':
        robobo.stopMotors()
        robobo.sayText('Los objetos de color azul o morado debo dejarlos en el brazo izquierdo del Baxter')
        robobo.movePanTo(90,30)
        robobo.moveWheelsByTime(-5,-5,23)
        robobo.moveWheelsByTime(-8,8,2.25) 
        robobo.moveWheels(5,5)

    elif final == 'izquierda':
        robobo.moveWheelsByTime(8,-8,1.8)
        robobo.moveWheelsByTime(5,5,11)
        robobo.moveWheelsByTime(-8,8,2.25)
        robobo.movePanTo(0,30)
        robobo.moveTiltTo(80,15)
        robobo.sayText('Esperando una nueva asignacion de tarea')
        robobo.whenANewQRCodeIsDetected(qrcallback)
        
def blob_nule():
    robobo.wait(1)
    #funcion vacia

def salida():
    print('Entre en salida')
    robobo.moveWheelsByTime(-4,4,4.5) #regularlo
    robobo.movePanTo(-95,30)
    robobo.moveWheels(5,5)
    robobo.whenANewColorBlobIsDetected(blob_nule) 
    robobo.whenANewQRCodeIsDetected(brazo_baxter_callback)

def infrarojo():

    while robobo.readIRSensor(IR.FrontC) < 125: 
        robobo.wait(0.01)

    robobo.stopMotors() 
    robobo.sayText('Objeto enganchado') 
    robobo.moveTiltTo(90, 15) 
    salida()

def blobcallback():
    
    color=senal
    robobo.stopMotors()
    robobo.sayText('Debo buscar la bola de color {}'.format(color))
    print(color)
    
    
    if  robobo.readColorBlob(color).posx > 80:
        robobo.sayText('La bola esta a la izquierda')
        robobo.moveWheelsByTime(5,-5,0.75)
        robobo.moveWheels(5,5)
        infrarojo()
    
    elif robobo.readColorBlob(color).posx <80 and robobo.readColorBlob(color).posx >30: 
        robobo.sayText('La bola esta en el centro')
        robobo.moveWheels(5,5)
        infrarojo()
       
           
    elif robobo.readColorBlob(color).posx < 30:
        robobo.sayText('La bola esta a la derecha')
        robobo.moveWheelsByTime(-5,5,0.75)
        robobo.moveWheels(5,5)
        infrarojo()

def trafico_callback():
    print("entre en trafico")
    trafico= robobo.readQR().id
    print (trafico)
    if trafico == 'peligrosa izquierda':
        robobo.moveWheelsByTime(10,10,1)
        robobo.moveWheelsByTime(8,-8,2.15) 
        robobo.moveWheels(15,15)
    elif trafico== 'peligrosa derecha':
        robobo.wait(1)
        robobo.moveWheelsByTime(10,10,2) 
        robobo.moveWheelsByTime(-8,8,2.25) 
        robobo.moveWheels(15,15)

    elif trafico == 'ceda':
        robobo.stopMotors()

    elif trafico == 'parar': 
        robobo.stopMotors() 
        robobo.moveWheelsByTime(8,-8,1.75) #gira el angulo justo para quedarse mirando las bolas
        robobo.moveWheelsByTime(8,8,2)     #Avanza 2 segundos en esa direccion
        robobo.sayText('Entrando en modo busqueda del objeto de color') 
        robobo.moveTiltTo(95,15)  
        robobo.moveWheels(4,4)  
        robobo.whenANewColorBlobIsDetected(blobcallback)
        
def busqueda():
    robobo.moveWheels(10,10)
    robobo.whenANewQRCodeIsDetected(trafico_callback)

def colocacion():
    robobo.moveWheelsByTime(8,-8,2.2)
    # girar 45 grados
    
def qrcallback():
    
    global senal
    senal= robobo.readQR().id.strip()
    global brazo
    print (senal)
    robobo.sayText('Asignacion de tarea recibida.Tarea asignada {}'.format(senal))
    if senal == 'green':
        brazo='derecho'
        colocacion()
        busqueda()

    elif senal == 'custom':
        brazo='izquierdo'
        colocacion()
        busqueda()
    
    elif senal == 'blue':
        brazo='izquierdo'
        colocacion()
        busqueda()
    
    elif senal == 'apagate':
        robobo.sayText('Trabajo terminado. Hasta la proxima vez')
        global valido 
        valido = False

robobo.moveTiltTo(80, 15)  

robobo.whenANewQRCodeIsDetected(qrcallback)

valido=True

while valido==True :
    robobo.wait(1)

robobo.stopMotors()
