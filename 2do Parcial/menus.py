import pygame
from funciones import *
from juego import jugar_preguntados
from modificar_opciones import pantalla_modificar_opciones
from agregar_preguntas import pantalla_agregar_preguntas
from rankings import mostrar_rankings_pygame

def menu_principal(pantalla, fuente_normal, fuente_pequena, sonidos, fondo_img, reloj, config, fondo_juego):
    opciones = ["Jugar", "Opciones", "Ranking","Agregar Preguntas", "Salir"]

    while True:
        pantalla_ajuste(fondo_img, pantalla)

        rects_opciones = []
        for i in range(len(opciones)):
            opcion = opciones[i]
            texto = fuente_pequena.render(opcion, True, colores["blanco"])
            rect = texto.get_rect(center=(pantalla_ancho // 2, 300 + i * 50))
            pantalla.blit(texto, rect)
            rects_opciones.append(rect)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(rects_opciones)):
                        rect = rects_opciones[i]
                        if rect.collidepoint(pos):
                            sonidos['click'].play()
                            if i == 0:
                                jugar_preguntados(pantalla, fuente_normal, fuente_pequena, reloj, config, sonidos, fondo_juego)
                            elif i == 1:
                                pantalla_modificar_opciones(pantalla, fuente_normal, fuente_pequena, reloj, config, sonidos, fondo_juego)
                            elif i == 2:
                                mostrar_rankings_pygame(pantalla, fuente_normal, fuente_pequena)
                            elif i == 3:
                                pantalla_agregar_preguntas(pantalla, fuente_normal, fuente_pequena, reloj, sonidos, fondo_juego)
                            elif i == 3:
                                pygame.quit()
                                exit()

        reloj.tick(30)


