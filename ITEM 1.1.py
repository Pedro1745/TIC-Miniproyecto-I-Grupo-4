#IMPORTACION LIBRERIA

from gpiozero import RGBLED, Button, Buzzer
from time import sleep, time
import random

#CONFIGURACION HARDWARE

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
frecuencia_fallo = 1500

def sonido_bocina(bocina, frecuencia, duracion = 1):
    termino = time() + duracion
    while time() < termino:
        bocina.on()
        sleep(1/frecuencia)
        bocina.off()
        sleep(1/frecuencia)

#CONFIGURACION PARTIDA

def validacion_entrada(texto):
    while True:
        entrada = input(texto)
        if entrada.isnumeric() and int(entrada) > 0:
            return int(entrada)
        print("ENTRADA INVALIDA")

def validacion_continuacion(texto):
    while True:
        entrada = input(texto).lower()
        if entrada == "si" or entrada =="no":
            return entrada
        print("ENTRADA INVALIDA")

def entradas_partida():
    print("-------------- ACTIVATE --------------")
    print("---- INGRESE LOS DATOS PARA JUGAR ----")
    jugadores = validacion_entrada("JUGADORES: ")
    rondas = validacion_entrada("RONDAS: ")
    tiempo = validacion_entrada("TIEMPO TURNO EN SEGUNDOS: ")
    return jugadores, rondas, tiempo

#FUNCIONES JUEGO

def inicio_juego(bocina):
    sonido_bocina(bocina, frecuencia_aviso, duracion = 1)
    print("---------- EMPIEZA EL JUEGO ----------")

def mostrar_puntaje(puntajes):
    for i, PUNTAJE in enumerate(puntajes):
        print(f"PUNTAJE DEL JUGADOR {i + 1}: {PUNTAJE}")

def randomizador_colores(color, led):
    for i in range(5):
        color[i] = random.randint(0, 1)
        if color[i] == 0:
            led[i].color = (1, 0, 0)
        else:
            led[i].color = (0, 0, 1)

def turno(led, boton, bocina, tiempo, puntajes, jugador):

    for i in range(5):
        led[i].color = (0, 0, 0)
    sleep(1)

    color = [0, 0, 0, 0, 0]
    randomizador_colores(color, led)

    botones_presionados = [False] * 5  
    tiempo_inicio = time()
    while time() - tiempo_inicio < tiempo:

        if boton[0].is_pressed and not botones_presionados[0]:
            botones_presionados[0] = True
            led[0].color = (0, 0, 0)
            if color[0] == 1:
                puntajes[jugador] += 1
                sonido_bocina(bocina, frecuencia_acierto, duracion = 0.1)
            else:
                puntajes[jugador] -= 1
                sonido_bocina(bocina, frecuencia_fallo, duracion = 0.1)
        elif not boton[0].is_pressed:
            botones_presionados[0] = False

        if boton[1].is_pressed and not botones_presionados[1]:
            botones_presionados[1] = True
            led[1].color = (0, 0, 0)
            if color[1] == 1:
                puntajes[jugador] += 1
                sonido_bocina(bocina, frecuencia_acierto, duracion = 0.1)
            else:
                puntajes[jugador] -= 1
                sonido_bocina(bocina, frecuencia_fallo, duracion = 0.1)
        elif not boton[1].is_pressed:
            botones_presionados[1] = False 

        if boton[2].is_pressed and not botones_presionados[2]:
            botones_presionados[2] = True
            led[2].color = (0, 0, 0)
            if color[2] == 1:
                puntajes[jugador] += 1
                sonido_bocina(bocina, frecuencia_acierto, duracion = 0.1)
            else:
                puntajes[jugador] -= 1
                sonido_bocina(bocina, frecuencia_fallo, duracion = 0.1)
        elif not boton[2].is_pressed:
            botones_presionados[2] = False

        if boton[3].is_pressed and not botones_presionados[3]:
            botones_presionados[3] = True
            led[3].color = (0, 0, 0)
            if color[3] == 1:
                puntajes[jugador] += 1
                sonido_bocina(bocina, frecuencia_acierto, duracion = 0.1)
            else:
                puntajes[jugador] -= 1
                sonido_bocina(bocina, frecuencia_fallo, duracion = 0.1)
        elif not boton[3].is_pressed:
            botones_presionados[3] = False

        if boton[4].is_pressed and not botones_presionados[4]:
            botones_presionados[4] = True
            led[4].color = (0, 0, 0)
            if color[4] == 1:
                puntajes[jugador] += 1
                sonido_bocina(bocina, frecuencia_acierto, duracion = 0.1)
            else:
                puntajes[jugador] -= 1
                sonido_bocina(bocina, frecuencia_fallo, duracion = 0.1)
        elif not boton[4].is_pressed:
            botones_presionados[4] = False

    for i in range(5):
        led[i].color = (0, 0, 0)
    sleep(1)

#MAIN

jugadores, rondas, tiempo = entradas_partida()
puntajes = [1] * jugadores

while True:

    inicio_juego(bocina)
    ronda_actual = 0
    juego_valido = True

    while ronda_actual < rondas and juego_valido == True:
        print(f"============== RONDA {ronda_actual + 1} ==============")
        tiempo = tiempo * 0.95
        for jugador in range(jugadores):
            print(f".......... TURNO JUGADOR {jugador + 1} ..........")
            turno(led, boton, bocina, tiempo, puntajes, jugador)
            mostrar_puntaje(puntajes)
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