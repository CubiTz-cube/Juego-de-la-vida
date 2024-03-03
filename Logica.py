from Interfaz import *
from Celula import cel1, cel2 ,cel3

intro = Logo()
while True:
    var = intro.bucle()
    if var == "Salir": exit()
    elif var == "Comenzar": break

pg.mixer_music.load("Sonidos\\Fondo.mp3")
pg.mixer_music.play(-1, fade_ms=300)
pg.mixer_music.set_volume(0.4)

while True:
    inicio = Inicio()

    while True:
        var = inicio.bucle()
        if var == "Salir": exit()
        elif var == "Comenzar": break

    cf.guardartxt()

    def play():
        global pause, estado

        pause = False
        estado = "Play"

    def pausa():
        global pause, estado

        pause = True
        estado = "Pausa"

    def cambiomodo():
        global modo

        if modo == "Manual": modo = "Automatico"
        else: modo = "Manual"

    juego = Game(play, pausa, cambiomodo)

    estado = "Pausa"
    modo = "Automatico"

    vuelta = 0
    acciones = []

    while True:
        if juego.bucle(estado, modo): pg.quit()
        if juego.regresar: break

        if vuelta >= cf.frame_espera and estado == "Play":
            juego.botguardar(F"Generacion {juego.gen}", "Saves\\Gen", True)

            for x in range(cf.ancho_tablero):
                for y in range(cf.alto_tablero):
                    if cel1.nacer(x,y,juego.tablero):
                        acciones.append(["nac",y,x])

                    if cel1.morir(x,y,juego.tablero):
                        acciones.append(["mor",y,x])

                    if cel2.nacer(x,y,juego.tablero):
                        acciones.append(["nac2",y,x])

                    if cel2.morir(x,y,juego.tablero):
                        acciones.append(["mor2",y,x])

                    if cel3.nacer(x,y,juego.tablero):
                        acciones.append(["nac3",y,x])

                    if cel3.morir(x,y,juego.tablero):
                        acciones.append(["mor3",y,x])

                    if juego.tablero[y][x][1] < 8 and juego.tablero[y][x][0] != 0:
                        juego.tablero[y][x][1] += 1
            
            for i in acciones:
                if i[0] == "nac" and juego.tablero[i[1]][i[2]][0] == 0: juego.tablero[i[1]][i[2]][0] = 1
                if i[0] == "mor" and juego.tablero[i[1]][i[2]][0] == 1: juego.tablero[i[1]][i[2]] = [0,0]

                if i[0] == "nac2" and juego.tablero[i[1]][i[2]][0] == 0: juego.tablero[i[1]][i[2]][0] = 2
                if i[0] == "mor2" and juego.tablero[i[1]][i[2]][0] == 2: juego.tablero[i[1]][i[2]] = [0,0]

                if i[0] == "nac3" and juego.tablero[i[1]][i[2]][0] == 0: juego.tablero[i[1]][i[2]][0] = 3
                if i[0] == "mor3" and juego.tablero[i[1]][i[2]][0] == 3: juego.tablero[i[1]][i[2]] = [0,0]
                
            acciones = []
            juego.nuevagen()
            juego.botguardar(F"Generacion {juego.gen}", "Saves\\Gen", True)
            if modo == "Manual": estado = "Pausa"

        vuelta += 1
        vuelta %= cf.frame_espera+1
