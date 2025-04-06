import json, time, os
from funciones_jugador import *
from menus import *
from mapas import *
bienvenida()
mostrar_reglas()
limpiar()
indice=[mapa_spawn, mapa_cueva, mapa_sala, mapa_sala_jefe]
final_malo_muerto=False
final_bueno=False
clase=clases()
limpiar()
while True:
    posmap=leer_posmapa()
    pos_de_mapa=posmap[0]
    mapa_actual=indice[pos_de_mapa]
    imprimir_mapa(mapa_actual)
    if estadisticas["Salud"]<=0:
        limpiar()
        print("============MORISTE===============")
        print("El demonio ha destruido el pueblo")
        print("      Intentalo de nuevo")
        print("==================================")
        time.sleep(5)
        limpiar()
        break
    elif final_bueno==True:
        print("=============================")
        print("          VICTORIA           ")
        print("=============================")
        print(" Salvaste el pueblo, dios te")
        print("     concedio su favor")
        time.sleep(5)
        limpiar()
        break
    direccion=input("W/A/S/D/E: ").lower()
    if pos_de_mapa==0:
        posicion=movimiento_spawn(posicion, mapa_actual, direccion)
    elif pos_de_mapa==1:
        posicion=movimiento_cueva(posicion, mapa_actual, direccion)
    elif pos_de_mapa==2:
        posicion=movimiento_sala(posicion, mapa_actual, direccion)
    elif pos_de_mapa==3:
        final_bueno=movimiento_sala_jefe(posicion, mapa_actual, direccion)
    limpiar()










