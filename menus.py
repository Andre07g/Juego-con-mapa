import os, time, json
def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')


def bienvenida():
    print("="*40)
    print(" "*15,"CROSS CAVE")
    print("="*40)

def mostrar_reglas():
    reglas=""""
    ================REGLAS================
    1. El jugador esta representado
       por "♾"
    2. Para moverte debes usar WASD 
       dentro de la consola, solo puedes
       ingresar una letra a la vez seguida
       de la tecla Enter
    3. Presiona E para abrir el inventario
    ======================================
    """
    print(reglas)
    input("Presiona cualquier tecla para iniciar: ")

def guia_inicio():
    global presentacion, final_malo
    print("Hombre: Viajero, me presento, soy Lucius, el jefe de este pueblo")
    time.sleep(1)
    print("Hombre: Nuestro pueblo ha sido maldito, un demonio robò nuestra cruz y huyò a la cueva")
    time.sleep(1)
    print("Ayudanos a recuperarla, y te recompensaremos")
    while True: 
        print("1.Para ayudarlos")
        print("2.Para seguir tu camino")
        salvarlos=input("Ingresa tu eleccion: ")
        if salvarlos=="1": 
            print("Hombre: Gracias, viajero")
            time.sleep(1)
            print("Puede que esto te ayude")
            time.sleep(1)
            print("Obtuviste 1 de comida")
            time.sleep(1)
            input("Presione cualquier tecla para continuar")
            presentacion=True
            break
        elif salvarlos=="2":
            print("Hombre: Dios se apiade de nosotros")
            input("Presiona cualquier tecla para continuar")
            final_malo=True
            break
    return presentacion
def guia_presentado():
    print("Lucius: Que dios te guie, viajero...")
    input("Presiona cualquier tecla para continuar")

def guia_final_presentado():
    print("Lucius: Gracias viajero, eres nuestro heroe, mi pueblo esta en deuda contigo")
    input("Presiona cualquier tecla para continuar")
    final_bueno=True

def guia_final_no_presentado():
    print("Hombre: Gracias, viajero desconocido, nuestro pueblo esta en deuda contigo")
    input("Presiona cualquier tecla para continuar")
    final_bueno=True

def perro():
    print("*Saludas al perro*")
    time.sleep(1)
    print("*El parece devolverte el saludo*")
    time.sleep(1)
    print("*Eres feliz*")
    input("Presiona cualquier opcion para continuar")

def combate_opciones():
    opciones="""
    1.Atacar
    2.Usar item
    3.Huir"""
    print(opciones)
    return input("Elije una opcion: ")