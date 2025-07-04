import pygame
from funciones import *
from terminado import pantalla_terminado
from datetime import datetime

def jugar_preguntados(pantalla, fuente_normal, fuente_pequena, reloj, config, sonidos, fondo_img):
    preguntas = cargar_preguntas_desde_csv()
    mezclar_lista(preguntas)

    tiempo_total = config['tiempo_segundos']
    vidas = config['cantidad_vidas']
    puntuacion = 0
    racha = 0
    comodines = {'bomba': False, 'x2': False, 'doble': False, 'pasar': False}

    nombre = cargar_nombre_pygame(pantalla, fuente_normal)

    for pregunta in preguntas:
        opciones = pregunta['opciones'].copy()
        mezclar_lista(opciones)
        correcta = pregunta['correcta']
        respondido = False
        tiempo_inicio = pygame.time.get_ticks()
        tiempo_pregunta = 15
        pregunta_inicio = pygame.time.get_ticks()

        fallo_en_doble_chance = False
        doble_chance_activo_para_pregunta = False

        while not respondido and vidas > 0:
            pantalla.blit(fondo_img, (0, 0))

            rect_pregunta = renderizar_texto_multilinea(pantalla, pregunta['texto'], fuente_normal, colores['negro'], 50, 80, pantalla_ancho - 100, colores['blanco'])

            rects_opciones = []
            for i, op in enumerate(opciones):
                rect_op = pygame.Rect(100, rect_pregunta.bottom + 20 + i * 50, 426, 40)
                dibujar_tarjeta(pantalla, f"{i+1}. {op}", fuente_pequena, rect_op, colores['blanco'], colores['negro'])
                rects_opciones.append(rect_op)

            for i, key in enumerate(comodines):
                if not comodines[key]:
                    rect = pygame.Rect(50 + i * 140, 500, 120, 40)
                    dibujar_tarjeta(pantalla, lista_comodines[i], fuente_pequena, rect, colores['gris'], colores['negro'])
                    rects_comodines.append((key, rect))

            tiempo_restante = tiempo_total - ((pygame.time.get_ticks() - tiempo_inicio) // 1000)

            mostrar_estado_juego(pantalla, fuente_pequena, tiempo_restante, vidas, puntuacion)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    for key, rect in rects_comodines:
                        if rect.collidepoint(mouse_pos) and not comodines[key]:
                            sonidos['click'].play()
                            if key == 'bomba':
                                opciones = usar_bomba(opciones, correcta)
                                comodines['bomba'] = True
                            elif key == 'pasar': 
                                respondido = usar_pasar()
                                comodines['pasar'] = True
                            elif key == 'doble': 
                                comodines['doble'] = True 
                                doble_chance_activo_para_pregunta = True 
                            elif key == 'x2':
                                comodines['x2'] = True

                    for idx, rect_op in enumerate(rects_opciones):
                        if rect_op.collidepoint(mouse_pos):
                            eleccion = idx
                            sonidos['click'].play()

                            if opciones[eleccion] == correcta:
                                puntos_extra = config['puntos_correcta']
                                if comodines['x2']: 
                                    puntos_extra = usar_x2(puntuacion,config_juego['puntos_correcta']) 

                                puntuacion += puntos_extra
                                racha += 1
                                sonidos['correcto'].play()
                                respondido = True 
                                fallo_en_doble_chance = False
                                doble_chance_activo_para_pregunta = False 
                            else:
                                if doble_chance_activo_para_pregunta and not fallo_en_doble_chance:
                                    sonidos['error'].play()
                                    fallo_en_doble_chance = True 

                                else:
                                    puntuacion += config['puntos_incorrecta']
                                    vidas -= 1
                                    racha = 0
                                    sonidos['error'].play()
                                    respondido = True 
                                    fallo_en_doble_chance = False 
                                    doble_chance_activo_para_pregunta = False 

                                if racha >= 5:
                                    tiempo_total += 10
                                    racha = 0
                                    

            if tiempo_restante <= 0 or (pygame.time.get_ticks() - pregunta_inicio) // 1000 > tiempo_pregunta:
                vidas -= 1
                puntuacion += config['puntos_incorrecta']
                respondido = True
                fallo_en_doble_chance = False 
                doble_chance_activo_para_pregunta = False 

            reloj.tick(30)

    guardar_preguntas_en_csv(preguntas)

    rankings = cargar_rankings()
    rankings.append({
        'nombre': nombre,
        'puntos': puntuacion,
        'fecha': datetime.now().strftime("%Y-%m-%d")
    })
    guardar_rankings(rankings)

    pantalla_terminado(pantalla, fuente_normal, fuente_pequena, puntuacion)

