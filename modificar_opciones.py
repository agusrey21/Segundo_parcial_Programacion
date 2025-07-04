from config import *
from funciones import *

def pantalla_modificar_opciones(pantalla, fuente_normal, fuente_pequena, reloj, config, sonidos, fondo_img):
    opciones = [
        ("Vidas", "cantidad_vidas", 1, 10),
        ("Tiempo total", "tiempo_segundos", 30, 300),
        ("Puntos correcta", "puntos_correcta", 1, 20),
        ("Puntos incorrecta", "puntos_incorrecta", -10, 0),
        ("Dificultad", "dificultad", ["Facil", "Medio", "Dificil"]),
        ("Volumen", "volumen", 0, 10)
    ]

    seleccionado = 0

    if 'dificultad' not in config:
        config['dificultad'] = "Medio"

    def aplicar_dificultad(dificultad):
        if dificultad == "Facil":
            config.update({'cantidad_vidas': 5, 'puntos_correcta': 10, 'puntos_incorrecta': -2, 'tiempo_segundos': 90})
        elif dificultad == "Medio":
            config.update({'cantidad_vidas': 3, 'puntos_correcta': 15, 'puntos_incorrecta': -5, 'tiempo_segundos': 60})
        elif dificultad == "Dificil":
            config.update({'cantidad_vidas': 1, 'puntos_correcta': 20, 'puntos_incorrecta': -10, 'tiempo_segundos': 30})

    while True:
        pantalla.blit(fondo_img, (0, 0))

        renderizar_texto_multilinea(pantalla, "Opciones de Juego", fuente_normal, colores['blanco'], pantalla_ancho // 2 - 200, 30, 400, colores['gris'])

        rects_opciones = []
        for i in range(len(opciones)):
            nombre = opciones[i][0]
            clave = opciones[i][1]

            if i == seleccionado:
                color_texto = colores['amarillo']
                color_fondo = colores['gris']
            else:
                color_texto = colores['blanco']
                color_fondo = colores['gris']

            valor = config[clave]
            if clave == "dificultad":
                valor = config['dificultad']

            texto = f"{nombre}: {valor}"

            rect = renderizar_texto_multilinea(pantalla, texto, fuente_pequena, color_texto, pantalla_ancho // 2 - 150, 150 + i * 60, 300, color_fondo)

            rects_opciones.append((clave, rect))

        renderizar_texto_multilinea(pantalla, "Click: Cambiar | Boton derecho: Volver", fuente_pequena, colores['negro'], pantalla_ancho // 2 - 200, pantalla_alto - 80, 400, colores['gris'])
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if evento.button == 1:
                    for idx in range(len(rects_opciones)):
                        clave, rect = rects_opciones[idx]
                        if rect.collidepoint(pos):
                            sonidos['click'].play()
                            seleccionado = idx
                            if clave == "dificultad":
                                idx_actual = opciones[4][2].index(config['dificultad'])
                                idx_nuevo = (idx_actual + 1) % len(opciones[4][2])
                                config['dificultad'] = opciones[4][2][idx_nuevo]
                                aplicar_dificultad(config['dificultad'])
                            elif clave == "volumen":
                                config['volumen'] = (config['volumen'] + 1) % 11
                                pygame.mixer.music.set_volume(config['volumen'] / 10)
                                for s in sonidos.values():
                                    s.set_volume(config['volumen'] / 10)
                            else:
                                config[clave] += 1

                if evento.button == 3:
                    guardar_configuracion(config)
                    sonidos['click'].play()
                    return

        reloj.tick(30)
