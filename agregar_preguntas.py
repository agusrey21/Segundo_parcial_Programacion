from funciones import *
import os
import csv

def pantalla_agregar_preguntas(pantalla, fuente_normal, fuente_pequena, reloj, sonidos, fondo_img):
    opcion_seleccionada = 0
    opciones_menu = [
        "Agregar pregunta manualmente",
        "Cargar preguntas desde archivo CSV",
        "Guardar cambios",
        "Volver al menu principal"
    ]

    preguntas_temporales = []

    while True:
        pantalla.blit(fondo_img, (0, 0))

        rect = renderizar_texto_multilinea(pantalla, "Agregar Preguntas", fuente_pequena, colores['blanco'], pantalla_ancho // 2 - 200, 150, 400, colores['gris'])


        rects_opciones = []
        for i in range(len(opciones_menu)):
            opcion = opciones_menu[i]

            if i == opcion_seleccionada:
                color_texto = colores['amarillo']
                color_fondo = colores['gris']
            else:
                color_texto = colores['blanco']
                color_fondo = colores['gris']

            rect = renderizar_texto_multilinea(
                pantalla, opcion, fuente_pequena, color_texto,
                pantalla_ancho // 2 - 200, 150 + i * 60, 400, color_fondo
            )

            rects_opciones.append(rect)

        info = fuente_pequena.render(f"Preguntas en memoria: {len(preguntas_temporales)}", True, colores['celeste'])
        pantalla.blit(info, (pantalla_ancho // 2 - info.get_width() // 2, 500))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if evento.button == 1:
                    for i in range(len(rects_opciones)):
                        rect = rects_opciones[i]
                        if rect.collidepoint(pos):
                            sonidos['click'].play()
                            if i == 0:
                                pregunta = agregar_pregunta_manual(pantalla, fuente_normal, fuente_pequena, reloj, sonidos, fondo_img)
                                if pregunta:
                                    preguntas_temporales.append(pregunta)
                            elif i == 1:
                                cargar_desde_csv(pantalla, fuente_normal, fuente_pequena, reloj, sonidos, fondo_img, preguntas_temporales)
                            elif i == 2:
                                if len(preguntas_temporales) > 0:
                                    preguntas = cargar_preguntas_desde_csv()
                                    preguntas.extend(preguntas_temporales)
                                    guardar_preguntas_en_csv(preguntas)
                                    mostrar_mensaje(pantalla, fuente_normal, "Preguntas guardadas!", colores['verde'], fondo_img)
                                    preguntas_temporales.clear()
                            elif i == 3:
                                return

        reloj.tick(30)

def agregar_pregunta_manual(pantalla, fuente_normal, fuente_pequena, reloj, sonidos, fondo_img):
    inputs = ["", "", "", "", "", ""]  
    input_activo = 0

    while True:
        pantalla.blit(fondo_img, (0, 0))

        renderizar_texto_multilinea(pantalla, "Agregar Pregunta Manual", fuente_normal, colores['blanco'], pantalla_ancho // 2 - 200, 50, 400, colores['gris'])

        textos = [
            "Texto de la pregunta:",
            "Opción 1:",
            "Opción 2:",
            "Opción 3:",
            "Opción 4:",
            "Respuesta correcta (texto exacto):"
        ]

        for i in range(len(textos)):
            color = colores['amarillo'] if i == input_activo else colores['blanco']
            renderizar_texto_multilinea(pantalla, textos[i], fuente_pequena, color, 50, 120 + i * 50, 700, colores['gris'])

            renderizar_texto_multilinea(pantalla, inputs[i], fuente_pequena, colores['celeste'], 50, 140 + i * 50, 700, colores['gris'])

        renderizar_texto_multilinea(pantalla, "ENTER: Siguiente campo | TAB: Guardar | ESC: Cancelar", fuente_pequena, colores['gris'], pantalla_ancho // 2 - 250, 500, 500, colores['gris'])

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return None

                elif evento.key == pygame.K_TAB:
                    if all(inputs):
                        nueva_pregunta = {
                            "texto": inputs[0],
                            "opciones": inputs[1:5],
                            "correcta": inputs[5]
                        }
                        sonidos['correcto'].play()
                        return nueva_pregunta
                    else:
                        mostrar_mensaje(pantalla, fuente_normal, "¡Completa todos los campos!", colores['rojo'], fondo_img)

                elif evento.key == pygame.K_RETURN:
                    input_activo = (input_activo + 1) % 6

                elif evento.key == pygame.K_BACKSPACE:
                    inputs[input_activo] = inputs[input_activo][:-1]

                else:
                    if len(inputs[input_activo]) < 100:
                        inputs[input_activo] += evento.unicode

        reloj.tick(30)


def cargar_desde_csv(pantalla, fuente_normal, fuente_pequena, reloj, sonidos, fondo_img, preguntas_temporales):
    mensaje = "Ingrese nombre del archivo CSV (en la carpeta del juego):"
    nombre_archivo = ""

    while True:
        pantalla.blit(fondo_img, (0, 0))

        renderizar_texto_multilinea(pantalla, "Cargar Preguntas desde CSV", fuente_normal, colores['blanco'], pantalla_ancho // 2 - 200, 50, 400, colores['gris'])

        renderizar_texto_multilinea(pantalla, mensaje, fuente_pequena, colores['blanco'], pantalla_ancho // 2 - 200, 150, 400, colores['gris'])

        renderizar_texto_multilinea(pantalla, nombre_archivo, fuente_pequena, colores['celeste'], pantalla_ancho // 2 - 200, 200, 400, colores['gris'])

        renderizar_texto_multilinea(pantalla, "ENTER: Cargar | ESC: Cancelar", fuente_pequena, colores['gris'], pantalla_ancho // 2 - 200, 250, 400, colores['gris'])

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return

                elif evento.key == pygame.K_RETURN:
                    if nombre_archivo:
                        with open(nombre_archivo, 'r', encoding='utf-8') as f:
                            lector = csv.reader(f, delimiter=';')
                            next(lector)

                            preguntas_cargadas = 0
                            for fila in lector:
                                if len(fila) >= 6:
                                    nueva_pregunta = {
                                        "texto": fila[0],
                                        "opciones": fila[1:5],
                                        "correcta": fila[5]
                                    }
                                    preguntas_temporales.append(nueva_pregunta)
                                    preguntas_cargadas += 1

                            mensaje = f"¡{preguntas_cargadas} preguntas cargadas correctamente!"
                            sonidos['correcto'].play()
                            return

                elif evento.key == pygame.K_BACKSPACE:
                    nombre_archivo = nombre_archivo[:-1]

                else:
                    if len(nombre_archivo) < 50:
                        nombre_archivo += evento.unicode

        reloj.tick(30)


def mostrar_mensaje(pantalla, fuente, texto, color, fondo_img, duracion=2000):
    pantalla.blit(fondo_img, (0, 0))
    renderizar_texto_multilinea(pantalla, texto, fuente, color, pantalla_ancho // 2 - 200, pantalla_alto // 2, 400, colores['gris'])
    pygame.display.flip()
    pygame.time.delay(duracion)