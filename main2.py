import pygame, sys
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))
shape, color, fill = "rect", (255, 0, 0), True

while True:
    screen.blit(canvas, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: shape = "rect"
            if event.key == pygame.K_e: shape = "ellipse"
            if event.key == pygame.K_f: fill = not fill
        if event.type == pygame.MOUSEBUTTONDOWN:
            start = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            end = event.pos
            rect = pygame.Rect(*start, end[0]-start[0], end[1]-start[1])
            rect.normalize()
            if shape == "rect":
                pygame.draw.rect(canvas, color, rect, 0 if fill else 2)
            else:
                pygame.draw.ellipse(canvas, color, rect, 0 if fill else 2)
    pygame.display.update()
