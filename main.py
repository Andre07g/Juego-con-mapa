import json, time, os
from funciones_jugador import *
from menus import *
from mapas import *
presentacion = False
cruz = False
final_malo = False
final_bueno = False
bienvenida()
mostrar_reglas()
limpiar()
while True:
    imprimir_mapa()
    direccion=input("Teclea: ")
    movimiento_spawn(posicion, mapa_actual, direccion, presentacion, cruz)
    limpiar()


