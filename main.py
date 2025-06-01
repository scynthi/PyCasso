import pygame
import sys
import os

WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)
SAVE_PATH = "saves/drawing.png"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rajzoló Program")
clock = pygame.time.Clock()


drawing = False
start_pos = None
current_shape = "rect"
fill = True
color = (255, 0, 0)


colors = {
    pygame.K_1: (255, 0, 0),     # piros
    pygame.K_2: (0, 255, 0),     # zöld
    pygame.K_3: (0, 0, 255)      # kék
}


canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BG_COLOR)

def draw_shape(surface, shape, color, rect, fill):
    if shape == "rect":
        if fill:
            pygame.draw.rect(surface, color, rect)
        else:
            pygame.draw.rect(surface, color, rect, width=2)
    elif shape == "ellipse":
        if fill:
            pygame.draw.ellipse(surface, color, rect)
        else:
            pygame.draw.ellipse(surface, color, rect, width=2)


while True:
    screen.fill(BG_COLOR)
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                start_pos = event.pos
                drawing = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                x, y = start_pos
                w, h = end_pos[0] - x, end_pos[1] - y
                rect = pygame.Rect(x, y, w, h)
                rect.normalize()
                draw_shape(canvas, current_shape, color, rect, fill)
                drawing = False
                start_pos = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_shape = "rect"
            elif event.key == pygame.K_e:
                current_shape = "ellipse"
            elif event.key == pygame.K_f:
                fill = True
            elif event.key == pygame.K_o:
                fill = False
            elif event.key in colors:
                color = colors[event.key]
            elif event.key == pygame.K_s:
                pygame.image.save(canvas, SAVE_PATH)
                print("Kép elmentve")

            elif event.key == pygame.K_l:
                if os.path.exists(SAVE_PATH):
                    loaded = pygame.image.load(SAVE_PATH)
                    canvas.blit(loaded, (0, 0))
                    print("Kép betöltve")
                else:
                    print("Kép nemtalálható")


    if drawing and start_pos:
        mouse_pos = pygame.mouse.get_pos()
        x, y = start_pos
        w, h = mouse_pos[0] - x, mouse_pos[1] - y

        preview_rect = pygame.Rect(x, y, w, h)
        preview_rect.normalize()
        draw_shape(screen, current_shape, color, preview_rect, fill)

    pygame.display.flip()
    clock.tick(60)