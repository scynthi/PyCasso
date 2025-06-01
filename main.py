from customtkinter import *
import pygame, os, ctypes, threading

WIDTH, HEIGHT = 600, 400
pygame.init()
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255,255,255))

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x500")
        self.pygame_frame = CTkFrame(self, width=WIDTH, height=HEIGHT)
        self.pygame_frame.pack(padx=20, pady=20)
        threading.Thread(target=self.embed_pygame, daemon=True).start()

    def embed_pygame(self):
        hwnd = self.pygame_frame.winfo_id()
        os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
        if os.name == "nt":
            ctypes.windll.user32.SetParent(pygame.display.get_wm_info()["window"], hwnd)
        while True:
            screen.blit(canvas, (0, 0))
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.circle(canvas, (255,0,0), e.pos, 10)
            pygame.display.update()

App().mainloop()
