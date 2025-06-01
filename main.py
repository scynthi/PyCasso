from customtkinter import *
import pygame, threading, tkinter.colorchooser as cc

pygame.init()
WIDTH, HEIGHT = 600, 400
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))
thickness = 3
color = (0,0,0)
drawing = False
last_pos = None
shape = "rect"
color = (255, 0, 0)

def draw_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    global drawing, last_pos
    drawing = False
    last_pos = None

    while True:
        screen.blit(canvas, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start = event.pos
                last_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                if shape != "freehand":
                    end = event.pos
                    rect = pygame.Rect(*start, end[0]-start[0], end[1]-start[1])
                    rect.normalize()
                    if shape == "rect":
                        pygame.draw.rect(canvas, color, rect)
                    elif shape == "ellipse":
                        pygame.draw.ellipse(canvas, color, rect)
            elif event.type == pygame.MOUSEMOTION and drawing:
                if shape == "freehand" and last_pos:
                    pygame.draw.line(canvas, color, last_pos, event.pos, thickness)
                    last_pos = event.pos
        pygame.display.update()

def choose_color():
    global color
    c = cc.askcolor()[0]
    if c: color = tuple(map(int, c))

def set_thick(v):
    global thickness
    thickness = int(v)

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
app.geometry("300x300")
CTkSlider(app, from_=1, to=10, command=set_thick).pack(pady=10)
CTkButton(app, text="Színválasztó", command=choose_color).pack(pady=10)
CTkButton(app, text="Téglalap", command=set_shape_rect).pack(pady=10)
CTkButton(app, text="Ellipszis", command=set_shape_ellipse).pack(pady=10)
CTkButton(app, text="Piros", command=set_color_red).pack(pady=10)
CTkButton(app, text="Kék", command=set_color_blue).pack(pady=10)
threading.Thread(target=draw_loop, daemon=True).start()
app.mainloop()



