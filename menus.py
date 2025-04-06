import os, time, json
def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def bienvenida():
    print("="*42)
    print(" "*15,"  CROSS CAVE")
    print("="*42)

def mostrar_reglas():
    reglas="""
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
    print("Hombre: Viajero, me presento, soy Lucius, el jefe de este pueblo")
    time.sleep(1)
    print("Hombre: Nuestro pueblo ha sido maldito, un demonio robò nuestra cruz y huyò a la cueva")
    time.sleep(1)
    print("Hombre: Ayudanos a recuperarla, y te recompensaremos")
    time.sleep(1)
    print("Hombre: Puede que esto te ayude")
    time.sleep(1)
    print("*Obtuviste medallòn vampiro*")
    time.sleep(1)
    print("Absorbe vida al derrotar enemigos y te permite superar")
    print("los limites de tu propia salud")
    time.sleep(1)
    input("Presione cualquier tecla para continuar")

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

def clases_menu():
    clases_menu="""
    =========Escoja una clase=======
    1.Guerrero:
      Daño 15, Defensa: 5, Vida: 100
    2.Mago:
      Daño 7, Defensa: 5, Vida: 130
      +Pociones
      Absorbe daño de los enemigos
    3.Enano:
      Daño: 12, Defensa: 15, Vida: 85
      +Comida
    4.Tanque:
      Daño:5, Defensa: 20, Vida: 110
      +Pociones
    =================================
    """
    print(clases_menu)
    return input("Selecciona: ")