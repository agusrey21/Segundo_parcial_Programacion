import pygame
pygame.init()

# Pantalla
pantalla_ancho = 626
pantalla_alto = 626

fondo_img = pygame.image.load("fondo.png")
fondo_img = pygame.transform.scale(fondo_img, (pantalla_alto, pantalla_ancho))
fondo_juego = pygame.image.load("fondo_juego.png")
fondo_juego = pygame.transform.scale(fondo_juego, (pantalla_alto, pantalla_ancho))

fuente_normal = pygame.font.SysFont("Arial", 28)
fuente_pequena = pygame.font.SysFont("Arial", 20)

reloj = pygame.time.Clock()

# Archivos
archivo_preguntas_csv = "preguntas.csv"
archivo_partidas_json = "partidas.json"
archivo_config_json = "config.json"
archivo_rankings_json = "rankings.json"

# Valores por defecto de configuracion
config_juego = {
    "cantidad_vidas": 5,
    "puntos_correcta": 10,
    "puntos_incorrecta": -5,
    "tiempo_segundos": 60,
    "segundos_extra": 10,
    "volumen" : 10
}

sonidos = {
    'click': pygame.mixer.Sound("click.mp3"),
    'correcto': pygame.mixer.Sound("correcto.mp3"),
    'error': pygame.mixer.Sound("error.mp3")
}

# Colores
colores = {
    'negro': (0, 0, 0),
    'blanco': (255, 255, 255),
    'rojo': (255, 0, 0),
    'verde': (0, 255, 0),
    'azul': (0, 0, 255),
    'amarillo': (255, 255, 0),
    'celeste': (0, 255, 255),
    'gris': (180, 180, 180)
}

#comodines
rects_comodines = []
lista_comodines = ['Bomba', 'X2', 'Doble', 'Pasar']
comodines_activos = {'bomba': False, 'x2': False, 'doble': False, 'pasar': False}

tiempo_total = config_juego['tiempo_segundos']
vidas = config_juego['cantidad_vidas']
puntuacion = 0
racha = 0
