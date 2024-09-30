# IMPORTACION LIBRERIA

from gpiozero import RGBLED, Button, Buzzer
from time import sleep, time
import random

# CONFIGURACION HARDWARE
led_1 = RGBLED(red = 21, green =  0, blue = 20)
led_2 = RGBLED(red = 26, green =  1, blue = 19)
led_3 = RGBLED(red = 16, green =  9, blue = 13)
led_4 = RGBLED(red = 12, green = 10, blue =  6)
led_5 = RGBLED(red =  2, green = 11, blue =  3)

led = [led_1, led_2, led_3, led_4, led_5]

boton_1 = Button(18)
boton_2 = Button(23)
boton_3 = Button(22)
boton_4 = Button(15)
boton_5 = Button(14)

boton = [boton_1, boton_2, boton_3, boton_4, boton_5]

bocina = Buzzer(5)
frecuencia_aviso = 3000
frecuencia_acierto = 2000
frecuencia_fallo = 1000

def sonido_bocina(bocina, frecuencia, duracion = 1):
    termino = time() + duracion
    while time() < termino:
        bocina.on()
        sleep(1/ frecuencia)
        bocina.off()
        sleep(1/frecuencia)

# CONFIGURACION PARTIDA

def validacion_entrada(texto):
    while True:
        entrada = input(texto)
        if entrada.isnumeric() and int(entrada) > 0:
            return int(entrada)
        print("ENTRADA INVALIDA")

def validacion_continuacion(texto):
    while True:
        entrada = input(texto).lower()
        if entrada == "si" or entrada == "no":
            return entrada
        print("ENTRADA INVALIDA")

def entradas_partida():
    print("-------------- ACTIVATE --------------")
    print("---- INGRESE LOS DATOS PARA JUGAR ----")
    jugadores = validacion_entrada("JUGADORES: ")
    rondas = validacion_entrada("RONDAS: ")
    tiempo = validacion_entrada("TIEMPO TURNO EN SEGUNDOS: ")
    return jugadores, rondas, tiempo

# FUNCIONES JUEGO

def inicio_juego(bocina):
    sonido_bocina(bocina, frecuencia_aviso, duracion = 1)
    print("---------- EMPIEZA EL JUEGO ----------")

def mostrar_puntaje(puntajes, rachas):
    for i, PUNTAJE in enumerate(puntajes):
        print(f"PUNTAJE DEL JUGADOR {i + 1}: {PUNTAJE}")
    for j, RACHA in enumerate(rachas):
        if RACHA >= 4 and RACHA < 8:
            BONIFICACION = 2
        elif RACHA >= 8 and RACHA < 16:
            BONIFICACION = 3
        elif RACHA >= 16 and RACHA < 32:
            BONIFICACION = 5
        elif RACHA >= 32:
            BONIFICACION = 7
        else:
            BONIFICACION = 0
        print(f"RACHA DEL JUGADOR {j + 1}: {RACHA} / BONIFICACION: +{BONIFICACION}")

def color_led(led, color):
    if color == 1:
        led.color = (1, 0, 0)
    else:
        led.color = (0, 0, 1)

def patrones():
    detector = random.randint(0, 1)
    if detector == 0:
        patron = [1, 1, 0, 0, 0]
    else:
        patron = [1, 1, 1, 0, 0]
    return patron

def turno(led, boton, bocina, tiempo, puntajes, jugador, rachas, bonificacion, color):
    
    botones_presionados = [False] * 5
    tiempo_inicio = time()

    while time() - tiempo_inicio < tiempo:
        for i in range(5):
            if boton[i].is_pressed and not botones_presionados[i]:
                botones_presionados[i] = True
                led[i].color = (0, 0, 0)
                if color[i] == 0:
                    puntajes[jugador] += 1
                    rachas[jugador] += 1
                    sonido_bocina(bocina, frecuencia_acierto, duracion = 0.1)
                else:
                    puntajes[jugador] -= 1
                    rachas[jugador] = 0
                    bonificacion[jugador] = 0
                    sonido_bocina(bocina, frecuencia_fallo, duracion = 0.1)
            elif not boton[i].is_pressed:
                botones_presionados[i] = False

    if rachas[jugador] >= 32:
        puntajes[jugador] += 8
    elif rachas[jugador] >= 16:
        puntajes[jugador] += 5
    elif rachas[jugador] >= 8:
        puntajes[jugador] += 3
    elif rachas[jugador] >= 4:
        puntajes[jugador] += 2

    for i in range(5):
        led[i].color = (0, 0, 0)
    sleep(1)

# MAIN

jugadores, rondas, tiempo = entradas_partida()
puntajes = [1] * jugadores
rachas = [0] * jugadores
bonificacion = [0] * jugadores

while True:

    inicio_juego(bocina)
    ronda_actual = 0
    juego_valido = True

    while ronda_actual < rondas and juego_valido:
        print(f"============== RONDA {ronda_actual + 1} ==============")
        tiempo = tiempo * 0.95
        for jugador in range(jugadores):
            print(f".......... TURNO JUGADOR {jugador + 1} ..........")
            for i in range(5):
                led[i].color = (0, 0, 0)
            sleep(1)
            patron = patrones()
            random.shuffle(patron)
            for i in range(5):
                color_led(led[i], patron[i])
            turno(led, boton, bocina, tiempo, puntajes, jugador, rachas, bonificacion, patron)
            mostrar_puntaje(puntajes, rachas)
            if puntajes[jugador] <= 0:
                print(f"JUGADOR {jugador + 1} HA SIDO ELIMINADO")
                juego_valido = False
                break
        ronda_actual += 1

    sonido_bocina(bocina, frecuencia_aviso, duracion = 1)
    print("----------- JUEGO TERMINADO -----------")

    respuesta = validacion_continuacion("DESEA VOLVER A JUGAR (SI O NO): ")
    if respuesta == "si":
        print("----- PREPARESE PARA OTRA PARTIDA -----")
    elif respuesta == "no":
        print("---------- GRACIAS POR JUGAR ----------")
        break
