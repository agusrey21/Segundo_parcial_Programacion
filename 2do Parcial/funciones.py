import pygame
import csv
import json
import os
import random
from config import *

def mejor_ranking(mejor, rankin):
    for i in rankin:
        if i['puntos'] > mejor['puntos']:
            mejor = i
    return mejor

def dibujar_tarjeta(pantalla, texto, fuente, rect, color_fondo, color_texto):
    pygame.draw.rect(pantalla, color_fondo, rect, border_radius=10)
    pygame.draw.rect(pantalla, color_texto, rect, 2, border_radius=10)
    
    texto_render = fuente.render(texto, True, color_texto)
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)
    
def renderizar_texto_multilinea(pantalla, texto, fuente, color, x, y, ancho_max, color_fondo):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba = linea_actual + palabra + " "
        if fuente.size(prueba)[0] <= ancho_max - 20:
            linea_actual = prueba
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "
    lineas.append(linea_actual)

    alto_total = len(lineas) * (fuente.get_height() + 5) + 10
    rect = pygame.Rect(x, y, ancho_max, alto_total)

    pygame.draw.rect(pantalla, color_fondo, rect, border_radius=10)

    offset_y = y + 5
    for linea in lineas:
        superficie = fuente.render(linea.strip(), True, color)
        pantalla.blit(superficie, (x + 10, offset_y))
        offset_y += fuente.get_height() + 5

    return rect  


def cargar_preguntas_desde_csv():
    preguntas = []
    with open(archivo_preguntas_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader) 
        for row in reader:
            pregunta = {
                'texto': row[0],
                'opciones': [row[1], row[2], row[3], row[4]],
                'correcta': row[5],
            }
            preguntas.append(pregunta)
    return preguntas

def guardar_preguntas_en_csv(preguntas):
    with open(archivo_preguntas_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['texto', 'opcion1', 'opcion2', 'opcion3', 'opcion4',
                         'correcta'])
        for p in preguntas:
            writer.writerow([
                p['texto'],
                p['opciones'][0],
                p['opciones'][1],
                p['opciones'][2],
                p['opciones'][3],
                p['correcta'],
            ])

def cargar_rankings():
    if os.path.exists(archivo_rankings_json):
        with open(archivo_rankings_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_rankings(rankings):
    with open(archivo_rankings_json, 'w', encoding='utf-8') as f:
        json.dump(rankings, f, indent=4, ensure_ascii=False)

def cargar_nombre_pygame(pantalla, fuente):
    nombre = ""
    input_activo = True
    while input_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(nombre) >= 3:
                    input_activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 15:
                        nombre += evento.unicode

        pantalla.fill(colores['negro'])
        mensaje = fuente.render("Ingrese su nombre (min. 3 letras)", True, colores['blanco'])
        pantalla.blit(mensaje, (pantalla_ancho // 2 - mensaje.get_width() // 2, 200))

        nombre_texto = fuente.render(nombre, True, colores['celeste'])
        pantalla.blit(nombre_texto, (pantalla_ancho // 2 - nombre_texto.get_width() // 2, 250))

        pygame.display.flip()
    return nombre


def guardar_configuracion(config):
    with open("config.json", "w") as archivo:
        json.dump(config, archivo, indent=4)


def cargar_configuracion():
    if os.path.exists(archivo_config_json):
        with open(archivo_config_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            "cantidad_vidas": 5,
            "puntos_correcta": 10,
            "puntos_incorrecta": -5,
            "tiempo_segundos": 60
        }
        
def usar_bomba(opciones, correcta):
    nuevas_opciones = [correcta]
    contador = 0

    for opcion in opciones:
        if opcion != correcta:
            if contador < 1:
                nuevas_opciones.append(opcion)
                contador += 1

    random.shuffle(nuevas_opciones)
    return nuevas_opciones


def usar_x2(puntuacion, puntos_correcta):
    return puntuacion + puntos_correcta * 2

def usar_doble_chance(fallo_anterior):
    return not fallo_anterior  

def usar_pasar():
    return True

def mostrar_estado_juego(pantalla, fuente, tiempo, vidas, puntos):
    rect_tiempo = pygame.Rect(pantalla_ancho - 550 , 30, 120, 40)
    rect_vidas = pygame.Rect(pantalla_ancho - 400 , 30, 120, 40)
    rect_puntos = pygame.Rect(pantalla_ancho - 250 , 30, 120, 40)
    
    dibujar_tarjeta(pantalla, f"Tiempo: {tiempo}s", fuente, rect_tiempo, colores['blanco'], colores['amarillo'])
    dibujar_tarjeta(pantalla, f"Vidas: {vidas}", fuente, rect_vidas, colores['blanco'], colores['rojo'])
    dibujar_tarjeta(pantalla, f"Puntos: {puntos}", fuente, rect_puntos, colores['blanco'], colores['verde'])

def mezclar_lista(lista_preguntas:list):
    random.shuffle(lista_preguntas)
    
def mostrar_mensaje(pantalla, fuente, texto, color, fondo_img, duracion=2000):
    pantalla.blit(fondo_img, (0, 0))
    renderizar_texto_multilinea(pantalla, texto, fuente, color, pantalla_ancho // 2 - 200, pantalla_alto // 2, 400, colores['gris'])
    pygame.display.flip()
    pygame.time.delay(duracion)
    
def pantalla_ajuste(fondo, pantalla):
    pantalla.blit(fondo, (0, 0))