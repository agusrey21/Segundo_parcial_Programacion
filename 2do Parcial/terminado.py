import pygame
from funciones import *
from config import *

def pantalla_terminado(pantalla, fuente_normal, fuente_pequena, puntos):
    pantalla.fill(colores['negro'])

    texto_final = fuente_normal.render(f"Puntos finales: {puntos}", True, colores['blanco'])
    pantalla.blit(texto_final, (pantalla.get_width() // 2 - texto_final.get_width() // 2, 200))

    texto_info = fuente_pequena.render("¡Gracias por jugar!", True, colores['blanco'])
    pantalla.blit(texto_info, (pantalla.get_width() // 2 - texto_info.get_width() // 2, 250))

    pygame.display.flip()
    pygame.time.delay(3000)
