import os, time, json, random
from menus import *
from mapas import *
pos_de_mapa=0
indice=[mapa_spawn, mapa_cueva, mapa_sala, mapa_sala_jefe]
mapa_actual=indice[pos_de_mapa]
posicion=[5,4]
serpienteviva=True
def leer_inventario():
    with open ("inventario.json","r") as file:
        inventario=json.load(file)
    return inventario

inventario=leer_inventario()

def leer_estats():
    with open ("estadisticas.json","r") as file:
        estadisticas=json.load(file)
    return estadisticas

estadisticas=leer_estats()

def imprimir_mapa():
    for fila in mapa_actual:
        print("  ".join(fila))

def movimiento_spawn(posicion, mapa_actual, direccion, presentacion, cruz):
    x,y=posicion
    dx, dy=0,0
    if direccion=="a":
        dy=-1
    elif direccion=="d":
        dy=1
    elif direccion=="w":
        dx=-1
    elif direccion=="s":
        dx=1
    elif direccion=="e":
        usar_item()
        input("Presione cualquier tecla para continuar")
    else: print("Ingresa una opcion valida")
    nuevo_x=x+dx
    nuevo_y=y+dy

    if mapa_actual[nuevo_x][nuevo_y]=="▤":
        pass

    elif mapa_actual[nuevo_x][nuevo_y]==" ":
        mapa_actual[x][y]=" "
        mapa_actual[nuevo_x][nuevo_y]="♾"
        posicion[0],posicion[1]=nuevo_x, nuevo_y

    elif mapa_actual[nuevo_x][nuevo_y]=="✉︎":
        abrir_cofre()
        input("Ingresa cualquier tecla para continuar: ")
        mapa_actual[x][y]=" "
        mapa_actual[nuevo_x][nuevo_y]="♾"
        posicion[0],posicion[1]=nuevo_x, nuevo_y


    elif mapa_actual[nuevo_x][nuevo_y]=="☺︎":
        if not presentacion:
            if not cruz:
             presentacion=guia_inicio()
            else: 
             guia_final_no_presentado()
        else:
            if not cruz:
                guia_presentado()
            else: guia_final_presentado()

    elif mapa_actual[nuevo_x][nuevo_y]=="𓃠":
        perro()

    elif mapa_actual[nuevo_x][nuevo_y]=="𓆘":
        pelea_serpiente()
        if serpienteviva==False:
            mapa_actual[x][y]=" "
            mapa_actual[nuevo_x][nuevo_y]="♾"
            posicion[0],posicion[1]=nuevo_x, nuevo_y

    elif mapa_actual[nuevo_x][nuevo_y]=="◘":
        pos_de_mapa+=1


elementos_valores={"Espada de acero":15,
               "Escudo del heroe":10,
               "Pocion de salud":10,
               "Comida":5,
               "Espada galactica":50,
               "Escudo inmortal":50,
               "Comida podrida":-5}

elementos_descripciones={"Espada de acero":"Añade 15 puntos de daño",
               "Escudo del heroe":"Te protege de 10 puntos de daño",
               "Pocion de salud":"Cura 10 puntos de salud",
               "Comida":"Cura 5 puntos de salud",
               "Espada galactica":"Añade 50 puntos de salud",
               "Escudo inmortal":"Te protege de 50 puntos de daño",
               "Comida podrida":"Podria ser peor"}

elementos_probabilidades={"Espada de acero":.2,
               "Escudo del heroe":.15,
               "Pocion de salud":.2,
               "Comida":.2,
               "Espada galactica":.05,
               "Escudo inmortal":.05,
               "Comida podrida":.15}

def abrir_cofre():
    print("Abriendo cofre...")
    time.sleep(1)
    objetos=list(elementos_valores.keys())
    probabilidades=list(elementos_probabilidades.values())
    objeto = random.choices(objetos, weights=probabilidades, k=1)[0]
    descripcion=elementos_descripciones[objeto]

    print("Obtuviste: ")
    print(f"{objeto}")
    print(f"{descripcion}")
    if objeto in ["Comida","Comida podrida","Pocion de salud"]:
        if objeto in inventario:
            inventario[objeto]+=1
        else: inventario[objeto]=1
        with open ("inventario.json","w") as file:
            json.dump(inventario, file, indent=4)
    else:
        if objeto in ["Espada de acero","Espada galactica"]:
            estadisticas["Ataque"]+=elementos_valores[objeto]
        else: estadisticas["Defensa"]+=elementos_valores[objeto]
        with open ("estadisticas.json","w") as file:
            json.dump(estadisticas, file, indent=4)
        
def usar_item():
            print("========Inventario========")
            for item, cantidad in inventario.items():
                        print(f"{item}->{cantidad}")
            print("==========================")
            while True:
                    objeto_elegido=input("Ingrese el nombre del objeto elegido(Escriba salir para salir): ")
                    if objeto_elegido in inventario.keys():
                        if inventario[objeto_elegido]<=0:
                            print ("No tienes del objeto elegido")
                        else:
                            estadisticas["Salud"]+=elementos_valores[objeto_elegido]
                            print (f"Se añadieron {elementos_valores[objeto_elegido]} de salud")
                            inventario[objeto_elegido]-=1
                            with open("estadisticas.json","w") as file:
                                json.dump(estadisticas, file, indent=4)
                            with open("inventario.json","w") as file:
                                json.dump(inventario, file, indent=4)
                            break
                    elif objeto_elegido in ["Salir","salir"]:
                        break
                    else: print("Ingrese un item existente")

def huida(minh, maxh, pro):
    huidae=False
    huida=random.randint(minh,maxh)
    if huida<pro:
        print("Huiste")
        input("Presiona cualquier tecla para continuar")
        huidae=True
    else: print("No pudiste huir")

    return huidae


def pelea_serpiente():
    print("Una serpiente te rodea")
    print("Comienza el combate")
    time.sleep(2)
    serpientevida=20
    global serpienteviva
    while True:
        op=combate_opciones()
        if op=="1":
            print(f"Atacas provocando {estadisticas['Ataque']} de daño")
            serpientevida-=estadisticas["Ataque"]
            if serpientevida<=0:
                print("Has ganado el combate")
                serpienteviva=False
                input("Presiona cualquier tecla para continuar")
                break
        elif op=="2":
            usar_item()
        elif op=="3":
            huidae=huida(1,10,5)
            if huidae==True:
                break
        if serpientevida>0:
            print("La serpiente se prepara para atacar")
            daño=random.randint(3,7)
            print(f"La serpiente de hace {daño} de daño")
            estadisticas["Salud"]-=daño
            with open("estadisticas.json","w") as file:
                json.dump(estadisticas, file, indent=4)
            if estadisticas["Salud"]<=0:
                print("Moriste")
                final_malo_muerto=True
                break    


