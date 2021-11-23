import pygame
import random
import math
import time
import threading
from pygame import mixer

# Iniciar pygame
pygame.init()

# Creacion de la ventana
pantalla = pygame.display.set_mode((1000, 800))

# Definir el fonde de pantalla
fondo = icon = pygame.image.load("imagenes/fondoRojo.png")

# Definir la musica de fondo
#mixer.music.load("MP3/Kobito of the Shining Needle_Little Princess.wav")
#mixer.music.set_volume(0.4)
#mixer.music.play(-1)

# Efecto de sonido
efectoDeSonidoExplosion = mixer.Sound("MP3/explosion sound effect.wav")

# Titulo e icono
pygame.display.set_caption("Bullet Punishment")
icon = pygame.image.load("imagenes/iconoBP.png")
pygame.display.set_icon(icon)

# Jugador
imagenJugador = pygame.image.load("imagenes/jugador.png")
jugadorX = 492
jugadorY = 386
jugadorX_Alternante = 0
jugadorY_Alternante = 0
eliminado = False


# bala roja
def crearPatron():
    patron = []
    imagenBalaRoja = []
    balaRojaX = []
    balaRojaY = []
    balaRojaX_Alternante = []
    balaRojaY_Alternante = []
    ordenAux = 0
    numBalas = 100

    # llamarlo como patron 1
    for i in range(numBalas):
        imagenBalaRoja.append(pygame.image.load("imagenes/bala_roja.png"))
        if ordenAux == 0:
            # posicion
            magico = random.randint(0, 1000)
            balaRojaX.append(magico)
            balaRojaY.append(-32)
            # trayectoria
            velocidad = random.uniform(0.4, 1.2)
            if magico < 500:
                balaRojaX_Alternante.append(velocidad)
            else:
                balaRojaX_Alternante.append(velocidad * -1)
            balaRojaY_Alternante.append(velocidad)

        if ordenAux == 1:
            # posicion
            magico = random.randint(0, 800)
            balaRojaX.append(1032)
            balaRojaY.append(magico)
            # trayectoria
            velocidad = random.uniform(0.4, 1.2)
            balaRojaX_Alternante.append(velocidad * -1)
            if magico < 400:
                balaRojaY_Alternante.append(velocidad)
            else:
                balaRojaY_Alternante.append(velocidad * -1)

        if ordenAux == 2:
            # posicion
            magico = random.randint(0, 1000)
            balaRojaX.append(magico)
            balaRojaY.append(832)
            # trayectoria
            velocidad = random.uniform(0.4, 1.2)
            if magico < 500:
                balaRojaX_Alternante.append(velocidad)
            else:
                balaRojaX_Alternante.append(velocidad * -1)
            balaRojaY_Alternante.append(velocidad * -1)

        if ordenAux == 3:
            # posicion
            magico = random.randint(0, 800)
            balaRojaX.append(-32)
            balaRojaY.append(magico)
            # trayectoria
            velocidad = random.uniform(0.4, 1.2)
            balaRojaX_Alternante.append(velocidad)
            if magico < 400:
                balaRojaY_Alternante.append(velocidad)
            else:
                balaRojaY_Alternante.append(velocidad * -1)

        ordenAux = ordenAux + 1
        if ordenAux == 4:
            ordenAux = 0

    patron.append(imagenBalaRoja)
    patron.append(balaRojaX)
    patron.append(balaRojaY)
    patron.append(balaRojaX_Alternante)
    patron.append(balaRojaY_Alternante)
    patron.append(numBalas)
    return patron


# Posiciones de todos los texto
posicionesTexto = [10, 10, 365, 150, 210, 350, 210, 420]


# tiempo en pantalla
def generarTemporizador():
    t = time.time()
    return t


tiempo = generarTemporizador()
textoTiempo = pygame.font.Font('freesansbold.ttf', 28)

# textos fin del juego
textoGO = pygame.font.Font('freesansbold.ttf', 38)
textoTF = pygame.font.Font('freesansbold.ttf', 32)
textoMen = pygame.font.Font('freesansbold.ttf', 32)


def mostrarTiempo(posTex):
    if not eliminado:
        tiempoDeSupervivencia = textoTiempo.render("Tiempo: " + str(segundosDeVida), True, (255, 255, 255))
        pantalla.blit(tiempoDeSupervivencia, (posTex[0], posTex[1]))
    else:
        mensajeGO = textoGO.render("¡Fin del juego!", True, (255, 255, 255))
        mensajeTF = textoTF.render("Tiempo sobrevivido: " + str(segundosDeVida) + " segundos", True, (255, 255, 255))
        mensaje = textoMen.render("Toca ENTER para volver a intentarlo", True, (255, 255, 255))
        pantalla.blit(mensajeGO, (posTex[2], posTex[3]))
        pantalla.blit(mensajeTF, (posTex[4], posTex[5]))
        pantalla.blit(mensaje, (posTex[6], posTex[7]))


def jugador(x, y):
    if not eliminado:
        pantalla.blit(imagenJugador, (x, y))


def balaRoja(imagen, x, y):
    if not fueraDePantalla:
        pantalla.blit(imagen, (x, y))


def colision(jugadorX, jugadorY, balaRojaX, balaRojaY):
    distancia = math.sqrt((math.pow(jugadorX - balaRojaX, 2)) + (math.pow(jugadorY - balaRojaY, 2)))
    if distancia < 24:
        return True

# variables de balas
contadorBalasFuera = 0
fueraDePantalla = False
balasEnPantalla = False


def moverBalas():
    for i in range(patron[5]):
        patron[1][i] += patron[3][i]
        patron[2][i] += patron[4][i]


# Bucle del Juego
corriendo = True
while corriendo:
    tiempoExe = time.time()
    if not eliminado:
        segundosDeVida = int((tiempo - tiempoExe) * -1)

    # Detalle al seguir ejecutando
    if not balasEnPantalla and segundosDeVida >= 1:
        patron = crearPatron()
        balasEnPantalla = True

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        # controlador del jugador
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugadorX_Alternante = -1.2

            if evento.key == pygame.K_RIGHT:
                jugadorX_Alternante = 1.2

            if evento.key == pygame.K_UP:
                jugadorY_Alternante = -1.2

            if evento.key == pygame.K_DOWN:
                jugadorY_Alternante = 1.2

            if evento.key == pygame.K_RETURN:
                if eliminado:
                    eliminado = False
                    jugadorX = 492
                    jugadorY = 386
                    contadorBalasFuera = 0
                    #mixer.music.play(-1)
                    tiempo = generarTemporizador()

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugadorX_Alternante = 0

            if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                jugadorY_Alternante = 0

    # RGB (red, green, blue) color de fondo
    pantalla.fill((0, 0, 0))

    # fondo de pantalla
    pantalla.blit(fondo, (0, 0))

    # limitante jugador
    jugadorX += jugadorX_Alternante
    jugadorY += jugadorY_Alternante

    if jugadorX <= 0:
        jugadorX = 0

    elif jugadorX >= 968:
        jugadorX = 968

    if jugadorY <= 0:
        jugadorY = 0

    elif jugadorY >= 768:
        jugadorY = 768

    # movimiento bala roja y sus limitante
    if segundosDeVida >= 1:
        threading.Thread(target=moverBalas()).start() # Donde de una vez todas las balas se mueven
        for i in range(patron[5]):
            if patron[1][i] <= -34:
                patron[3][i] = 0
                patron[4][i] = 0
                patron[1][i] = -33
                contadorBalasFuera = contadorBalasFuera + 1

            elif patron[1][i] >= 1034:
                patron[3][i] = 0
                patron[4][i] = 0
                patron[1][i] = 1033
                contadorBalasFuera = contadorBalasFuera + 1

            if patron[2][i] <= -34:
                patron[3][i] = 0
                patron[4][i] = 0
                patron[2][i] = -33
                contadorBalasFuera = contadorBalasFuera + 1

            elif patron[2][i] >= 834:
                patron[3][i] = 0
                patron[4][i] = 0
                patron[2][i] = 833
                contadorBalasFuera = contadorBalasFuera + 1

            # verificar si hubo colision con la bala roja
            huboColision = colision(jugadorX, jugadorY, patron[1][i], patron[2][i])
            if huboColision:
                eliminado = True
                mixer.music.stop()
                efectoDeSonidoExplosion.set_volume(0.3)
                efectoDeSonidoExplosion.play()

            # actualizar imagen de la bala
            if contadorBalasFuera < patron[5]:
                if not eliminado:
                    balaRoja(patron[0][i], patron[1][i], patron[2][i])
                else:
                    balasEnPantalla = False

            else:
                balasEnPantalla = False
                contadorBalasFuera = 0

    # actualizar imagen del jugador y del texto
    mostrarTiempo(posicionesTexto)
    jugador(jugadorX, jugadorY)
    pygame.display.update()
