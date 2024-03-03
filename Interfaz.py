import pygame as pg
import pygame_textinput as pgtex
import Config as cf
import random as rd
import numpy as np

pg.init() 
panAlto = pg.display.Info().current_h - 75

class Pantalla():
    def __init__(self, nombre) -> None:
        # Sonidos
        if pg.mixer.get_init() != None:
            self.sondClick = pg.mixer.Sound("Sonidos\\click.mp3")
            self.sondExito = pg.mixer.Sound("Sonidos\\exito1.mp3")
            self.sondError = pg.mixer.Sound("Sonidos\\error1.mp3")
            self.sondPonerCelu1 = pg.mixer.Sound("Sonidos\\poner_celula1.mp3")
            self.sondPonerCelu2 = pg.mixer.Sound("Sonidos\\poner_celula2.mp3")
            self.sondPonerCelu3 = pg.mixer.Sound("Sonidos\\poner_celula3.mp3")
            self.sondQuitarCelu1 = pg.mixer.Sound("Sonidos\\quitar_celula1.mp3")
            self.sonfQuitarCelu2 = pg.mixer.Sound("Sonidos\\quitar_celula2.mp3")
            self.sonfQuitarCelu3 = pg.mixer.Sound("Sonidos\\quitar_celula3.mp3")

        # Pantalla
        self.panAlto = panAlto
        self.panAncho = self.panAlto
        self.panta = pg.display.set_mode((self.panAncho, self.panAlto))
        pg.display.set_caption(nombre)

        # Relox
        self.reloj = pg.time.Clock()

        # Proporciones
        self.tam_tex = int(self.panAlto / 14)

        # Mouse
        self.clickSolta = True
        self.clickPres = False
        self.clickPresDe = False
        self.mousePos = (0,0)

        #Teclado
        self.teclaEnter = False

        # Entrada de Texto
        self.textInput = pgtex.TextInputVisualizer(font_object=pg.font.Font(None, int(self.tam_tex/2)),
        font_color=cf.clr_texto, cursor_color=cf.clr_texto)

    def _input(self):
        events = pg.event.get()
        self.textInput.update(events)

        self.mousePos = pg.mouse.get_pos()

        for event in events:
            if event.type == pg.QUIT:
                return True
            if event.type == pg.MOUSEBUTTONUP:
                self.clickSolta = True
            if event.type == pg.MOUSEBUTTONDOWN:
                self.clickSolta = False
            if event.type == pg.KEYDOWN and event.key == 13:
                self.teclaEnter = True

        click = pg.mouse.get_pressed()
        self.clickPres = click[0]
        self.clickPresDe = click[2]
        
    def sonido_alea(self, sonidos , volumenmin, volumenmax):
        sonidos[rd.randint(0,len(sonidos)-1)].play().set_volume(rd.uniform(volumenmin, volumenmax))
    
    def _boton(self, texto, vertic, color, clrMouse, clrTexto, tamTexto = 30, accion=None):
        long = len(texto)+1
        
        text = pg.font.Font(None, tamTexto).render(texto, True, clrTexto)

        if vertic[0][0] < self.mousePos[0] < vertic[1][0] and vertic[0][1] < self.mousePos[1] < vertic[2][1]:
            
            pg.draw.polygon(self.panta, clrMouse, vertic)

            if self.clickPres and self.clickSolta == False and accion != None:
                self.sondClick.play().set_volume(0.5)
                accion()
                self.clickSolta = True

        else:
            pg.draw.polygon(self.panta, color, vertic)
        
        self.panta.blit(text, (vertic[0][0]+int(tamTexto/2*10/long),vertic[0][1]+int(tamTexto/2)))

class Game(Pantalla):
    def __init__(self, botPlay, botPausa, botModo):
        super().__init__("Juego de la vida")
        self.gen = 0
        self.genGuardada = 0
        self.celTipo = 0

        self.regresar = False

        self.guardando = False
        self.cargando = False

        # Tablero
        self.tablero =  np.empty(shape=(cf.alto_tablero+1,cf.ancho_tablero+1), dtype= list)

        for x in range(cf.ancho_tablero+1):
            for y in range(cf.alto_tablero+1):
                self.tablero[y][x] = [0,0]

        # Mensajes
        def generarmensaje(mensajes, tamano, color = cf.clr_texto):
            men = []
            for mensaje in mensajes: 
                men.append(pg.font.Font(None, int(tamano)).render(mensaje, True, color))
            return men
        
        self.mensa = 0

        self.mensajes = generarmensaje([ "La sostenibilidad es el camino hacia el futuro que queremos.",
            "El cambio climático no es una amenaza lejana, es una realidad presente.",
            "El agua es un recurso vital, protejámoslo.",
            "La igualdad de género es un derecho humano fundamental.",
            "La energía renovable es la clave para un futuro sostenible.",
            "La educación es la herramienta más poderosa para cambiar el mundo.",
            "La innovación y la tecnología son fundamentales para el desarrollo sostenible.",
            "La pobreza no es inevitable, podemos erradicarla.",
            "La biodiversidad es la base de la vida en la Tierra.",
            "La acción climática es esencial para proteger nuestro planeta."], self.tam_tex/2)
        
        # Botones
        self.botModo = botModo
        self.botPausa = botPausa
        self.modoText = generarmensaje(["Manual", "Automatico"], self.tam_tex/1.5, cf.clr_texto_realce)
        self.botones = [
                    ["Guardar", "Cargar", "Play", "Pausa", "Reiniciar", "Cel"],
                    [cf.clr_botones, cf.clr_botones, cf.clr_fondo_table_pau, cf.clr_botones, cf.clr_botones, cf.clr_celu[0]],
                    [self.botguardar, self.botcargar, botPlay, botPausa, self.botborrar, self.botcelula],
                    [cf.clr_botones_press, cf.clr_botones_press, cf.clr_botones_press, cf.clr_botones_press, cf.clr_botones_press, cf.clr_celu[2]]]

        #Proporciones
        self.arri = int(self.panAlto / 12)
        self.abaj = int(self.panAlto / 12)
        self.cent_arri = int(self.arri/1.8)

        self.tableDivix = int((self.panAlto-self.arri-self.abaj)/cf.ancho_tablero)
        self.tableDiviy = int((self.panAlto-self.arri-self.abaj)/cf.alto_tablero)

        self.botoDivi = int(self.panAncho/len(self.botones[0])+1)
        self.botoFondo = self.panAlto-self.abaj
        self.botoTextam = int(self.botoDivi/4)

    def botguardar(self, nombre = "", ruta = "Saves", directo = False):
        self.textInput.value = ""

        if self.guardando == False and directo == False:
            self.guardando = True
            return

        if nombre.strip() == "": return

        try:
            np.save(F"{ruta}\\{nombre}.npy", self.tablero)
            self.cargando = False
            if directo == False: 
                self.botPausa()
                self.sondExito.play().set_volume(0.5)

        except FileNotFoundError:
            self.sondError.play().set_volume(0.5)
            self.cargando = False
            return False
        
        self.guardando = False

    def botcargar(self, nombre  = "", ruta = "Saves", directo = False):
        self.textInput.value = ""

        if self.cargando == False and directo == False:
            self.cargando = True
            return
        
        if nombre.strip() == "": return

        try:
            self.tablero = np.load(F"{ruta}\\{nombre}.npy", allow_pickle=True)
            self.cargando = False
            self.botPausa()
            if directo == False: self.sondExito.play().set_volume(0.5)

        except FileNotFoundError:
            self.sondError.play().set_volume(0.5)
            self.cargando = False
            return False
        
        self.cargando = False

    def botborrar(self):
        self.gen = 0
        self.genGuardada = 0

        for x in range(cf.ancho_tablero):
            for y in range(cf.alto_tablero):
                self.tablero[y][x] = [0,0]

    def botgenantes(self):
        if self.botcargar(F"Generacion {self.gen-1}", "Saves\\Gen", True) == False: return

        self.gen -= 1
        self.mensa -= 1
        self.mensa %= len(self.mensajes)

    def botgendespues(self):
        if self.genGuardada <= self.gen: 
            self.sondError.play().set_volume(0.5)
            return
        
        if self.botcargar(F"Generacion {self.gen+1}", "Saves\\Gen", True) == False: return

        self.gen += 1
        self.mensa += 1
        self.mensa %= len(self.mensajes)

    def botregresar(self):
        self.regresar = True

    def botcelula(self):
        color = [cf.clr_celu[0], cf.clr_celu2[0], cf.clr_celu3[0]]
        colorPress = [cf.clr_celu[2], cf.clr_celu2[2], cf.clr_celu3[2]]

        self.celTipo += 1
        self.celTipo %= len(color)

        self.botones[1][5] = color[self.celTipo]
        self.botones[3][5] = colorPress[self.celTipo]

    def enterinput(self):
        if self.teclaEnter:
            if self.guardando: self.botguardar(self.textInput.value)
            elif self.cargando: self.botcargar(self.textInput.value)
            self.teclaEnter = False

    def nuevagen(self):
        self.gen += 1
        self.genGuardada = self.gen
        self.mensa += 1
        self.mensa %= len(self.mensajes)

    def _botones(self, estado):
        divi = self.botoDivi
        fondo = self.botoFondo
        textTam = self.botoTextam

        cerox = int(self.panAncho/2.7)
        ceroy = 0
        self._boton("", [(cerox,ceroy),(cerox+self.arri*3,ceroy),(cerox+self.arri*3,self.arri-1),(cerox,self.arri-1)], cf.clr_botones, cf.clr_botones_press, cf.clr_texto, 1, accion=self.botModo)

        self.botones[1][2] = cf.clr_fondo_table if estado == "Pausa" else cf.clr_botones
        self.botones[1][3] = cf.clr_fondo_table_pau if estado == "Play" else cf.clr_botones

        for i in range(len(self.botones[0])):
            x = int(i*divi)
            texto = self.botones[0][i]
            color = self.botones[1][i]
            accion = self.botones[2][i]
            colorPress = self.botones[3][i]

            self._boton(texto,[(x,fondo),(x+divi,fondo),(x+divi,self.panAlto),(x,self.panAlto)], color, colorPress, cf.clr_texto, textTam, accion)

        if estado != "Pausa": return
        y = self.panAlto - fondo

        self._boton(">   ",[(x+ divi/2,fondo - y),(self.panAncho,fondo - y),(self.panAncho,fondo),(x+ divi/2,fondo)], cf.clr_botones, cf.clr_botones_press, cf.clr_texto, textTam, self.botgendespues)
        self._boton("<   ",[(0,fondo - y),(divi/2,fondo - y),(divi/2,fondo),(0,fondo)], cf.clr_botones, cf.clr_botones_press, cf.clr_texto, textTam, self.botgenantes)

    def _informacion(self, modo):
        fps = round(pg.time.Clock.get_fps(self.reloj))

        pg.draw.rect(self.panta, cf.clr_botones, (0,0,self.panAncho,self.arri))
        pg.draw.rect(self.panta, cf.clr_botones_ligh, (0,int(self.cent_arri*1.2),self.panAncho,int(self.cent_arri*0.67)))

        self.panta.blit(pg.font.Font(None, self.tam_tex).render(F"Gen: {self.gen}", True, cf.clr_texto), (int(self.panAncho/20),int(self.arri/8)))
        self.panta.blit(pg.font.Font(None, int(self.tam_tex)).render(F"FPS: {fps}", True, cf.clr_texto), (int(self.panAncho/1.3),int(self.arri/8)))

        if modo == "Manual": self.panta.blit(self.modoText[0], (int(self.panAncho/2.35),int(self.arri/5)))
        else: self.panta.blit(self.modoText[1], (int(self.panAncho/2.5),int(self.arri/5)))
        
        if self.guardando or self.cargando: self.panta.blit(self.textInput.surface, (self.panAncho/40,int(self.cent_arri*1.26)))
        else: self.panta.blit(self.mensajes[self.mensa], (self.panAncho/40,int(self.cent_arri*1.26)))

    def _tablero(self):
        divix = self.tableDivix
        diviy = self.tableDiviy

        for numx in range(cf.ancho_tablero):
            for numy in range(cf.alto_tablero):
                x = numx*divix + (self.panAncho - cf.ancho_tablero*divix)/2
                y = numy*diviy + self.arri*1.1
                coord = [(x,y),(x+divix,y),(x+divix,y+diviy),(x,y+diviy)]

                # Clicks
                if coord[0][0] <= self.mousePos[0] <= coord[1][0] and coord[0][1] <= self.mousePos[1] <= coord[2][1]:

                    if self.clickSolta == False and self.clickPres:
                        if self.tablero[numy][numx][0] == 0: 
                            self.tablero[numy][numx] = [self.celTipo+1,0] 
                            self.sonido_alea([self.sondPonerCelu1, self.sondPonerCelu2, self.sondPonerCelu3], 0.5, 1.5)

                        else: 
                            self.tablero[numy][numx] = [0,0]
                            self.sonido_alea([self.sondQuitarCelu1, self.sonfQuitarCelu2, self.sonfQuitarCelu3], 0.5, 0.6)

                        self.clickSolta = True

                    if self.clickPresDe and self.tablero[numy][numx][0] == 0:
                        self.tablero[numy][numx] = [self.celTipo+1,0]
                        try: self.sonido_alea([self.sondPonerCelu1, self.sondPonerCelu2, self.sondPonerCelu3], 0.5, 1.5)
                        except: pass

                # Dibujar
                if self.tablero[numy][numx][0] == 0:
                    pg.draw.polygon(self.panta, cf.clr_celu_muer, coord)

                if self.tablero[numy][numx][0] == 1:
                    pg.draw.polygon(self.panta, cf.clr_celu[self.tablero[numy][numx][1]], coord)

                if self.tablero[numy][numx][0] == 2:
                    pg.draw.polygon(self.panta, cf.clr_celu2[self.tablero[numy][numx][1]], coord)

                if self.tablero[numy][numx][0] == 3:
                    pg.draw.polygon(self.panta, cf.clr_celu3[self.tablero[numy][numx][1]], coord)

    def bucle(self, estado, modo):
        if estado == "Pausa": self.panta.fill(cf.clr_fondo_table_pau)
        else: self.panta.fill(cf.clr_fondo_table)

        if self._input(): return True
        self.enterinput()

        self._botones(estado)
        self._informacion(modo)
        self._tablero()

        cerox = int(self.panAncho/1.033)
        ceroy = 0
        self._boton(" ",[(cerox,ceroy),(self.panAncho,ceroy),(self.panAncho,self.arri*3/8),(cerox,self.arri*3/8)],cf.clr_celu2[1], cf.clr_botones_press, cf.clr_texto, self.tam_tex, self.botregresar)
 
        pg.display.flip()
        self.reloj.tick(60)

class Inicio(Pantalla):
    def __init__(self):
        super().__init__("Juego de la vida")
        self.jugando = False

        self.imagMute = pg.transform.scale(pg.image.load("Imagenes\\mute.png").convert_alpha(), (self.panAncho/12,self.panAlto/12))
        self.imagActiv = pg.transform.scale(pg.image.load("Imagenes\\active.png").convert_alpha(), (self.panAncho/12,self.panAlto/12))

        self.texTablero = pg.font.Font(None, int(self.tam_tex)).render("Dimension del tablero", True, "#FFFFFF")
                    
    def botjugar(self):
        self.jugando = True
        pass

    def botsalir(self):
        exit()

    def bottableromas(self):
        cf.ancho_tablero += 1
        cf.alto_tablero += 1

    def bottableromen(self):
        if cf.ancho_tablero > 1 and cf.alto_tablero > 1:
            cf.ancho_tablero -= 1
            cf.alto_tablero -= 1
    
    def botmute(self):
        if pg.mixer.music.get_busy():
            self.sondClick.play().set_volume(0.5)
            pg.mixer.music.pause()	
        else: 
            pg.mixer_music.play()

    def _botones(self):
        textTam = self.tam_tex

        self._boton("Play",[(self.panAncho/4,self.panAlto*3/16),(self.panAncho*3/4,self.panAlto*3/16),(self.panAncho*3/4,self.panAlto*5/16),(self.panAncho/4,self.panAlto*5/16)], cf.clr_botones, cf.clr_botones_press, cf.clr_texto, textTam, self.botjugar)
        self._boton("-    ",[(self.panAncho*2/8,self.panAlto*6/16),(self.panAncho*3/8,self.panAlto*6/16),(self.panAncho*3/8,self.panAlto*8/16),(self.panAncho*2/8,self.panAlto*8/16)], cf.clr_botones, cf.clr_botones_press, cf.clr_texto, textTam, self.bottableromen)
        self._boton("+    ",[(self.panAncho*5/8,self.panAlto*6/16),(self.panAncho*6/8,self.panAlto*6/16),(self.panAncho*6/8,self.panAlto*8/16),(self.panAncho*5/8,self.panAlto*8/16)], cf.clr_botones, cf.clr_botones_press, cf.clr_texto, textTam, self.bottableromas)
        self._boton("Salir",[(self.panAncho/4,self.panAlto*9/16),(self.panAncho*3/4,self.panAlto*9/16),(self.panAncho*3/4,self.panAlto*11/16),(self.panAncho/4,self.panAlto*11/16)], cf.clr_botones, cf.clr_botones_press, cf.clr_texto, textTam, self.botsalir)
        
        self._boton("",[(self.panAncho-self.panAncho/16 ,0),(self.panAncho,0),(self.panAncho,self.panAlto/16),(self.panAncho-self.panAncho/16,self.panAlto/16)], cf.clr_botones, cf.clr_botones_press, cf.clr_texto, textTam, self.botmute)
        if pg.mixer.music.get_busy():
            self.panta.blit(self.imagActiv, (self.panAncho-self.panAncho/15,-6))
        else:
            self.panta.blit(self.imagMute, (self.panAncho-self.panAncho/15,-6))
            

    def _informacion(self):
        
        self.panta.blit(self.texTablero, (self.panAncho/4.13,self.panAlto/3.1))
        pg.draw.rect(self.panta, "#FFFFFF", (self.panAncho*3/8,self.panAlto*6/16,self.panAncho/4,self.panAncho/8))
        self.panta.blit(pg.font.Font(None, int(self.tam_tex)).render(F"{cf.ancho_tablero}", True, "#000000"), (self.panAncho*3/8+self.panAncho/10,self.panAlto*6/16+self.panAncho/20))

    def bucle(self):
        self.panta.fill(cf.clr_fondo_table)

        if self._input(): return "Salir"
        if self.jugando: return "Comenzar"

        self._informacion()
        self._botones()
        

        pg.display.flip()
        self.reloj.tick(60)

class Logo(Pantalla):
    def __init__(self):
        super().__init__("Juego de la vida")
        self.alpha = 0
        self.imgLogo = pg.transform.scale(pg.image.load("Imagenes\\logo.png").convert_alpha(), (self.panAncho,self.panAlto))


    def bucle(self):
        self.panta.fill(cf.clr_fondo_table)
        if self._input(): return "Salir"

        imgLogo_copy = self.imgLogo.copy()
        imgLogo_copy.set_alpha(self.alpha)
        self.panta.blit(imgLogo_copy, (0,0))
        self.alpha += 3

        if self.clickPres and self.clickSolta == False: self.clickSolta = True ; return "Comenzar"

        if self.alpha >= 450: return "Comenzar"

        pg.display.flip()
        self.reloj.tick(60)
        
    