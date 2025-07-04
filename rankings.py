from config import *
from funciones import *

def mostrar_rankings_pygame(pantalla, fuente_normal, fuente_pequena):
    rankings = cargar_rankings()
    pantalla.fill(colores['negro'])

    titulo = fuente_normal.render("Rankings", True, colores['rojo'])
    pantalla.blit(titulo, (pantalla_ancho // 2 * 0.95 - titulo.get_width() // 2, 50))

    if not rankings:
        mensaje = fuente_pequena.render("No hay registros todavia.", True, colores['blanco'])
        pantalla.blit(mensaje, (pantalla_ancho // 2 - mensaje.get_width() // 2, 150))
    else:
        for i, r in enumerate(rankings[-10:][::-1]):
            texto = fuente_pequena.render(f"{i+1}. {r['nombre']} - {r['puntos']} puntos ({r['fecha']})", True, colores['blanco'])
            pantalla.blit(texto, (100, 150 + i * 30))

    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_RETURN:
                    esperando = False
