import os, time, json, random
from menus import *
from mapas import *
indice=[mapa_spawn, mapa_cueva, mapa_sala, mapa_sala_jefe]
posicion=[5,4]
serpienteviva=True
presentacion=False

def leer_inventario():
    with open ("inventario.json","r") as file:
        inventario=json.load(file)
    return inventario

inventario=leer_inventario()

def leer_posmapa():
    with open("posicionjugador.json","r") as file:
        posmap=json.load(file)
    return posmap
def escribir_posmapa():
    with open("posicionjugador.json","w") as file:
        json.dump(posmap, file)

posmap=leer_posmapa()
pos_de_mapa=posmap[0]

mapa_actual=indice[pos_de_mapa]
def leer_estats():
    with open ("estadisticas.json","r") as file:
        estadisticas=json.load(file)
    return estadisticas

estadisticas=leer_estats()

def imprimir_mapa(mapa_actual):
        for fila in mapa_actual:
            print("  ".join(fila))
 
def movimiento_spawn(posicion, mapa_actual, direccion):
    global presentacion
    global pos_de_mapa
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
             if presentacion==True:
                 print("Que dios te acompañe")
                 input("Presione cualquier tecla para continuar")
             else: 
                guia_inicio()
                presentacion=True

    elif mapa_actual[nuevo_x][nuevo_y]=="𓃠":
        perro()

    elif mapa_actual[nuevo_x][nuevo_y]=="𓆘":
        serpienteviva=pelea_serpiente()
        if serpienteviva==False:
            mapa_actual[x][y]=" "
            mapa_actual[nuevo_x][nuevo_y]="♾"
            posicion[0],posicion[1]=nuevo_x, nuevo_y

    elif mapa_actual[nuevo_x][nuevo_y]=="◘":
        posmap[0]+=1
        escribir_posmapa()
        posicion[0],posicion[1]=5,1
    return posicion

elementos_valores={"Espada de acero":15,
               "Escudo del heroe":5,
               "Pocion de salud":20,
               "Comida":10,
               "Espada galactica":50,
               "Escudo inmortal":50,
               "Comida podrida":-5}

elementos_descripciones={"Espada de acero":"Añade 15 puntos de daño",
               "Escudo del heroe":"Te protege de 5 puntos de daño",
               "Pocion de salud":"Cura 20 puntos de salud",
               "Comida":"Cura 10 puntos de salud",
               "Espada galactica":"Añade 50 puntos de daño",
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
            print(f"VIDA:{estadisticas['Salud']}")
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
    else: 
        print("No pudiste huir")
        time.sleep(1)

    return huidae

def pelea_serpiente():
    print("Una serpiente te rodea")
    print("Comienza el combate")
    time.sleep(2)
    limpiar()
    serpientevida=30
    global serpienteviva
    serpienteviva=True
    turno=1
    global clase
    while True:
            imprimir_mapa(mapa_spawn)
            print(f"=====Turno {turno}=====")
            print(f"Jugador:{estadisticas['Salud']}   Enemigo: {serpientevida}")
            op=combate_opciones()
            if op=="1":
                print(f"Atacas provocando {estadisticas['Ataque']} de daño")
                serpientevida-=estadisticas["Ataque"]
                if serpientevida<=0:
                    print("Has ganado el combate")
                    serpienteviva=False
                    print("El medallòn absorbe 10 puntos de salud")
                    if clase=="2":
                        estadisticas["Ataque"]+=2
                        print("Absorbiste 2 de daño")
                    estadisticas["Salud"]+=10
                    with open("estadisticas.json","w") as file:
                        json.dump(estadisticas, file, indent=4)
                    input("Presiona cualquier tecla para continuar")
                    limpiar()
                    return serpienteviva
                    break
            elif op=="2":
                usar_item()
            elif op=="3":
                huidae=huida(1,10,5)
                if huidae==True:
                    limpiar()
                    break
            if serpientevida>0:
                print("La serpiente se prepara para atacar")
                time.sleep(1)
                daño=random.randint(10,15)
                print(f"La serpiente de hace {daño} de daño")
                time.sleep(1)
                if daño<estadisticas["Defensa"]:
                    print("Bloqueaste todo el daño")
                else:
                    daño-=estadisticas["Defensa"]
                    estadisticas["Salud"]-=daño
                    print(f"Recibes {daño} de daño")
                with open("estadisticas.json","w") as file:
                    json.dump(estadisticas, file, indent=4)
                if estadisticas["Salud"]<=0:
                    print("Moriste")
                    time.sleep(3)
                    break
            turno+=1
            time.sleep(1)
            limpiar()    

def movimiento_cueva(posicion, mapa_actual, direccion):
    global pos_de_mapa
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


    elif mapa_actual[nuevo_x][nuevo_y]=="☹":
            esqueletovivo=pelea_muñeco()
            if esqueletovivo==False:
                mapa_actual[x][y]=" "
                mapa_actual[nuevo_x][nuevo_y]="♾"
                posicion[0],posicion[1]=nuevo_x, nuevo_y

    elif mapa_actual[nuevo_x][nuevo_y]=="◘":
        posmap[0]+=1
        escribir_posmapa()
        posicion[0],posicion[1]=5,1
    return posicion

def pelea_muñeco():
    print("Una esqueleto te ataca")
    print("Comienza el combate")
    time.sleep(2)
    limpiar()
    esqueletovida=30
    global esqueletovivo
    turno=1
    while True:
            imprimir_mapa(mapa_cueva)
            print(f"=====Turno {turno}=====")
            print(f"Jugador:{estadisticas['Salud']}   Enemigo: {esqueletovida}")
            op=combate_opciones()
            if op=="1":
                print(f"Atacas provocando {estadisticas['Ataque']} de daño")
                esqueletovida-=estadisticas["Ataque"]
                if esqueletovida<=0:
                    print("Has ganado el combate")
                    print("El medallòn absorbe 15 puntos de salud")
                    if clase=="2":
                        estadisticas["Ataque"]+=3
                        print("Absorbiste 3 de daño")
                    estadisticas["Salud"]+=15
                    with open("estadisticas.json","w") as file:
                        json.dump(estadisticas, file, indent=4)
                    esqueletovivo=False
                    input("Presiona cualquier tecla para continuar")
                    return esqueletovivo
                    break
            elif op=="2":
                usar_item()
            elif op=="3":
                huidae=huida(1,20,7)
                if huidae==True:
                    break
            if esqueletovida>0:
                print("El esqueleto se prepara para atacar")
                time.sleep(1)
                daño=random.randint(10,20)
                print(f"El esqueleto te hace {daño} de daño")
                time.sleep(1)
                if daño<estadisticas["Defensa"]:
                    print("Bloqueaste todo el daño")
                else:
                    daño-=estadisticas["Defensa"]
                    estadisticas["Salud"]-=daño
                    print(f"Recibes {daño} de daño")
                with open("estadisticas.json","w") as file:
                    json.dump(estadisticas, file, indent=4)
                if estadisticas["Salud"]<=0:
                    print("Moriste")
                    time.sleep(3)
                    final_malo_muerto=True
                    break    
            turno+=1
            time.sleep(1)
            limpiar()
        
def movimiento_sala(posicion, mapa_actual, direccion):
    global pos_de_mapa
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


    elif mapa_actual[nuevo_x][nuevo_y]=="☹":
            esqueletovivo=pelea_sala()
            if esqueletovivo==False:
                mapa_actual[x][y]=" "
                mapa_actual[nuevo_x][nuevo_y]="♾"
                posicion[0],posicion[1]=nuevo_x, nuevo_y

    elif mapa_actual[nuevo_x][nuevo_y]=="☠︎":
            esqueletovivo=pelea_miniboss()
            if esqueletovivo==False:
                mapa_actual[x][y]=" "
                mapa_actual[nuevo_x][nuevo_y]="♾"
                posicion[0],posicion[1]=nuevo_x, nuevo_y

    elif mapa_actual[nuevo_x][nuevo_y]=="◘":
        posmap[0]+=1
        escribir_posmapa()
        posicion[0],posicion[1]=1,4
    return posicion
     
def pelea_sala():
    print("Una esqueleto te ataca")
    print("Comienza el combate")
    time.sleep(2)
    limpiar()
    esqueletovida=40
    global esqueletovivo
    turno=1
    while True:
            imprimir_mapa(mapa_sala)
            print(f"=====Turno {turno}=====")
            print(f"Jugador:{estadisticas['Salud']}   Enemigo: {esqueletovida}")
            op=combate_opciones()
            if op=="1":
                print(f"Atacas provocando {estadisticas['Ataque']} de daño")
                esqueletovida-=estadisticas["Ataque"]
                if esqueletovida<=0:
                    print("Has ganado el combate")
                    if clase=="2":
                        estadisticas["Ataque"]+=5
                        print("Absorbiste 5 de daño")
                    print("El medallòn absorbe 15 puntos de salud")
                    estadisticas["Salud"]+=15
                    with open("estadisticas.json","w") as file:
                        json.dump(estadisticas, file, indent=4)
                    esqueletovivo=False
                    input("Presiona cualquier tecla para continuar")
                    return esqueletovivo
                    break
            elif op=="2":
                usar_item()
            elif op=="3":
                huidae=huida(1,20,7)
                if huidae==True:
                    break
            if esqueletovida>0:
                print("El esqueleto se prepara para atacar")
                time.sleep(1)
                daño=random.randint(10,30)
                print(f"El esqueleto te hace {daño} de daño")
                time.sleep(1)
                if daño<estadisticas["Defensa"]:
                    print("Bloqueaste todo el daño")
                else:
                    daño-=estadisticas["Defensa"]
                    estadisticas["Salud"]-=daño
                    print(f"Recibes {daño} de daño")
                with open("estadisticas.json","w") as file:
                    json.dump(estadisticas, file, indent=4)
                if estadisticas["Salud"]<=0:
                    print("Moriste")
                    final_malo_muerto=True
                    break    
            turno+=1
            time.sleep(1)
            limpiar()

def pelea_miniboss():
    print("Una esqueleto gigante te ataca")
    print("Comienza el combate")
    time.sleep(2)
    limpiar()
    esqueletovida=60
    global esqueletovivo
    turno=1
    while True:
            imprimir_mapa(mapa_sala)
            print(f"=====Turno {turno}=====")
            print(f"Jugador:{estadisticas['Salud']}   Enemigo: {esqueletovida}")
            op=combate_opciones()
            if op=="1":
                print(f"Atacas provocando {estadisticas['Ataque']} de daño")
                esqueletovida-=estadisticas["Ataque"]
                if esqueletovida<=0:
                    print("Has ganado el combate")
                    print("El medallòn absorbe 50 puntos de salud")
                    if clase=="2":
                        estadisticas["Ataque"]+=15
                        print("Absorbiste 15 de daño")
                    estadisticas["Salud"]+=50
                    esqueletovivo=False
                    with open("estadisticas.json","w") as file:
                        json.dump(estadisticas, file, indent=4)
                    input("Presiona cualquier tecla para continuar")
                    return esqueletovivo
                    break
            elif op=="2":
                usar_item()
            elif op=="3":
                huidae=huida(1,20,14)
                if huidae==True:
                    break
            if esqueletovida>0:
                print("El esqueleto gigante se prepara para atacar")
                time.sleep(1)
                daño=random.randint(20,40)
                print(f"El esqueleto gigante te hace {daño} de daño")
                time.sleep(1)
                if daño<estadisticas["Defensa"]:
                    print("Bloqueaste todo el daño")
                else:
                    daño-=estadisticas["Defensa"]
                    estadisticas["Salud"]-=daño
                    print(f"Recibes {daño} de daño")
                with open("estadisticas.json","w") as file:
                    json.dump(estadisticas, file, indent=4)
                if estadisticas["Salud"]<=0:
                    print("Moriste")
                    final_malo_muerto=True
                    break    
            turno+=1
            time.sleep(1)
            limpiar()

def pelea_boss():
    print("El demonio te ataca")
    print("Comienza el combate")
    time.sleep(2)
    limpiar()
    esqueletovida=100
    demoniovivo=True
    turno=1
    while True:
            imprimir_mapa(mapa_sala_jefe)
            print(f"=====Turno {turno}=====")
            print(f"Jugador:{estadisticas['Salud']}   Enemigo: {esqueletovida}")
            op=combate_opciones()
            if op=="1":
                print(f"Atacas provocando {estadisticas['Ataque']} de daño")
                esqueletovida-=estadisticas["Ataque"]
                if esqueletovida<=0:
                    print("Has ganado el combate")
                    print("El medallòn se libera, abriendo la puerta hacia la cruz")
                    demoniovivo=False
                    input("Presiona cualquier tecla para continuar")
                    return demoniovivo
                    break
            elif op=="2":
                usar_item()
            elif op=="3":
                huidae=huida(1,20,3)
                if huidae==True:
                    break
            if esqueletovida>0:
                print("El demonio se prepara para atacar")
                time.sleep(1)
                daño=random.randint(30,60)
                print(f"El demonio te hace {daño} de daño")
                time.sleep(1)
                if daño<estadisticas["Defensa"]:
                    print("Bloqueaste todo el daño")
                else:
                    daño-=estadisticas["Defensa"]
                    estadisticas["Salud"]-=daño
                    print(f"Recibes {daño} de daño")
                with open("estadisticas.json","w") as file:
                    json.dump(estadisticas, file, indent=4)
                if estadisticas["Salud"]<=0:
                    print("Moriste")
                    break    
            turno+=1
            time.sleep(1)
            limpiar()
        
def movimiento_sala_jefe(posicion, mapa_actual, direccion):
    global pos_de_mapa
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

    elif mapa_actual[nuevo_x][nuevo_y]=="⛧":
            demoniovivo=pelea_boss()
            if demoniovivo==False:
                mapa_actual[x][y]=" "
                mapa_actual[nuevo_x][nuevo_y]="♾"
                posicion[0],posicion[1]=nuevo_x, nuevo_y
                mapa_sala_jefe[8][4]=" "

    elif mapa_actual[nuevo_x][nuevo_y]=="✟":
        final_bueno=True
        return final_bueno
    
 
def reinicio():           
    escribir_posmapa()
    with open("inventario.json","w") as file:
        json.dump(inventario, file, indent=4)
    with open("estadisticas.json","w") as file:
        json.dump(estadisticas, file, indent=4)
   

def clases():
    while True:
        global clase
        clase=clases_menu()
        match clase:
            case "1":
                estadisticas["Salud"]=100
                estadisticas["Ataque"]=15
                estadisticas["Defensa"]=5
                posmap[0]=0
                inventario={"Comida": 2,
                "Pocion de salud": 2}
                reinicio()
                print("Clase elegida correctamente")
                time.sleep(2)
                return clase
                break
            case "2":
                estadisticas["Salud"]=130
                estadisticas["Ataque"]=7
                estadisticas["Defensa"]=5
                posmap[0]=0
                inventario={"Comida": 2,
                "Pocion de salud": 5}
                reinicio()
                print("Clase elegida correctamente")
                time.sleep(2)
                return clase
                break
            case "3":
                estadisticas["Salud"]=85
                estadisticas["Ataque"]=12
                estadisticas["Defensa"]=15
                posmap[0]=0
                inventario={"Comida": 5,
                "Pocion de salud": 2}
                reinicio()
                print("Clase elegida correctamente")
                time.sleep(2)
                return clase
                break
            case "4":
                estadisticas["Salud"]=110
                estadisticas["Ataque"]=5
                estadisticas["Defensa"]=20
                posmap[0]=0
                inventario={"Comida": 3,
                "Pocion de salud": 3}
                reinicio()
                print("Clase elegida correctamente")
                time.sleep(2)
                return clase
                break
            case _: 
                print("Ingrese una clase correcta")
                time.sleep(1)
        limpiar()


