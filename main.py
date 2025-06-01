import pygame, sys, os
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))

def save():
    pygame.image.save(canvas, "save.png")

def load():
    if os.path.exists("save.png"):
        img = pygame.image.load("save.png")
        canvas.blit(img, (0, 0))

while True:
    screen.blit(canvas, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: save()
            if event.key == pygame.K_l: load()
        if event.type == pygame.MOUSEBUTTONDOWN:
            start = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            end = event.pos
            rect = pygame.Rect(*start, end[0]-start[0], end[1]-start[1])
            pygame.draw.rect(canvas, (255, 0, 0), rect)
    pygame.display.update()

