from customtkinter import *
import pygame, threading

set_appearance_mode("light")
WIDTH, HEIGHT = 600, 400
BG_COLOR = (255, 255, 255)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BG_COLOR)
shape = "rect"
color = (255, 0, 0)

def draw_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    while True:
        screen.blit(canvas, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                end = event.pos
                rect = pygame.Rect(*start, end[0]-start[0], end[1]-start[1])
                rect.normalize()
                if shape == "rect":
                    pygame.draw.rect(canvas, color, rect)
                elif shape == "ellipse":
                    pygame.draw.ellipse(canvas, color, rect)
        pygame.display.update()

def set_shape_rect():
    global shape
    shape = "rect"

def set_shape_ellipse():
    global shape
    shape = "ellipse"

def set_color_red():
    global color
    color = (255, 0, 0)

def set_color_blue():
    global color
    color = (0, 0, 255)

app = CTk()
app.geometry("300x400")
CTkButton(app, text="Téglalap", command=set_shape_rect).pack(pady=10)
CTkButton(app, text="Ellipszis", command=set_shape_ellipse).pack(pady=10)
CTkButton(app, text="Piros", command=set_color_red).pack(pady=10)
CTkButton(app, text="Kék", command=set_color_blue).pack(pady=10)

threading.Thread(target=draw_loop, daemon=True).start()
app.mainloop()
