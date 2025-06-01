import pygame, sys
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))
drawing = False
last_pos = None

while True:
    screen.blit(canvas, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
        if event.type == pygame.MOUSEMOTION and drawing:
            pygame.draw.line(canvas, (255,0,0), last_pos, event.pos, 2)
            last_pos = event.pos
    pygame.display.update()
