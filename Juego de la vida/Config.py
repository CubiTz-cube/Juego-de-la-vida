_cargar_txt = True

# Tablero
alto_tablero = 30
ancho_tablero = 30

#Interfaz Grafica
clr_fondo_table = "#2F0C34"
clr_fondo_table_pau = "#330C24" 

clr_texto = "#F3FFFF"
clr_texto_realce = "#BEBEFF"

clr_botones = "#5A8CD1"
clr_botones_ligh = "#5381C2"
clr_botones_press = "#7BADF4"

clr_celu = ["#05f2f2", "#1fe4d8", "#3ad6bd", "#54c8a3", "#6eba89", "#89ac6e", "#a39e54", "#bd903a", "#d8821f", "#f27405"]
clr_celu2 = ["#f43e39", "#df5240", "#ca6747", "#b57b4f", "#a08f56", "#8ca45d", "#77b864", "#62cc6c", "#4de173", "#38f57a"]
clr_celu3 = ["#7047f5", "#7f58e2", "#8e6ace", "#9c7bbb", "#ab8da8", "#ba9e94", "#c9b081", "#d7c16e", "#e6d35a", "#f5e447"]
clr_celu_muer = "#FFFFFF"

# Bucle
frame_espera = 10

##### Reglas del juego #####
# Muere (meno igual a: , mayor igual a:)
# Nace (si es igual a:)

#Normal
muere_celula = (1,4)
nace_nuevacelula = (3,3)

#Ciudades
muere_celula2 = (1,6) 
nace_nuevacelula2 = (4,5,6,7,8) 

#Laberinto
muere_celula3 = (0,6) 
nace_nuevacelula3 = (3,3) 


from os import mkdir

try: mkdir("Saves") 
except: pass
try: mkdir("Saves\\Gen")
except: pass

try:
    config = open("Saves\\Config.txt", "x")
    config.close()
    config = open("Saves\\Config.txt", "w")

    for escri in open("Config.py", "r").readlines()[0:40]:
        config.write(escri)

    config.close()
except:
    config = open("Saves\\Config.txt", "r").read()
    exec(config)

    print("Configuracion cargada")

def sobrelinea(archivo, lineaNum, tex):
    with open(archivo, 'r') as file:
        lines = file.readlines()

    lines[lineaNum - 1] = tex + '\n'

    with open(archivo, 'w') as file:
        file.writelines(lines)

def guardartxt():
    sobrelinea('Saves\\Config.txt', 4, F'ancho_tablero = {ancho_tablero}')
    sobrelinea('Saves\\Config.txt', 5, F'alto_tablero = {alto_tablero}')

    print("Configuracion guardada")
