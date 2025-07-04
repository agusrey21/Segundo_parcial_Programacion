import pygame
from config import *
from funciones import *
from menus import menu_principal

pygame.init()

pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
pygame.display.set_caption("Preguntados")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)

pygame.mixer.music.load("fondo.mp3")
pygame.mixer.music.play(-1)

menu_principal(pantalla, fuente_normal, fuente_pequena, sonidos, fondo_img, reloj, config_juego, fondo_juego)


