import pygame
import ctypes
import os
import threading
from tkinter import colorchooser, filedialog
from customtkinter import *
from PIL import Image
from os import path

# Konstansok
WIDTH, HEIGHT = 600, 400
BG_COLOR = (255, 255, 255)
DEFAULT_SAVE = "./saves/drawing.png"

color_map = {
    "Piros": (255, 0, 0),
    "Zöld": (0, 255, 0),
    "Kék": (0, 0, 255)
}

class BootApp(CTk):
    def __init__(self):
        super().__init__()
        pygame.init()

        self.resizable(False, False)
        self.geometry_centered(500, 300)

        self.overrideredirect(True)
        self.lift()
        self.attributes('-topmost', True)
        self.after(10, lambda: self.attributes('-topmost', False))

        image_path = path.join("Assets", "Images", "boot.png")
        image = CTkImage(Image.open(image_path), size=(500, 300))
        CTkLabel(master=self, text="", image=image, fg_color="black").grid(row=0, column=0)

    def geometry_centered(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")



class MainApp(CTk):
    def __init__(self):
        super().__init__()
        self.lift()
        self.attributes('-topmost', True)
        self.after(10, lambda: self.attributes('-topmost', False))

        self.title("PyCasso")
        self.iconbitmap(path.join("Assets", "Images", "icon.ico"))
        self.geometry("950x450")
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)

        self.drawing_state = self.init_state()
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.canvas.fill(BG_COLOR)
        self.history = []

        self.pygame_frame = CTkFrame(self, width=WIDTH, height=HEIGHT)
        self.pygame_frame.grid(row=0, column=1, padx=20, pady=20)

        self.sidebar = CTkScrollableFrame(self, width=300, label_text="Eszközök")
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.build_controls()

        self.thread = threading.Thread(target=self.embed_pygame, daemon=True)
        self.thread.start()


    def init_state(self):
        return {
            "drawing": False,
            "start_pos": None,
            "last_pos": None,
            "shape": "rect",
            "fill": True,
            "color": (255, 0, 0),
            "thickness": 2,
            "mouse_pos": (0, 0),
            "current_tool": "Téglalap"
        }

    def build_controls(self):
        self.sidebar.grid_columnconfigure(0, weight=1)

        CTkLabel(self.sidebar, text="Formák:", font=("Arial", 14)).grid(row=0, column=0, pady=(10, 5), sticky="w")
        CTkButton(self.sidebar, text="□", command=lambda: self.set_shape("rect", "Téglalap")).grid(row=1, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="O", command=lambda: self.set_shape("ellipse", "Ellipszis")).grid(row=2, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="/", command=lambda: self.set_shape("line", "Vonal")).grid(row=3, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="    ✍️", command=lambda: self.set_shape("freehand", "Szabadkéz")).grid(row=4, column=0, pady=2, sticky="ew")

        CTkLabel(self.sidebar, text="Kitöltés:", font=("Arial", 14)).grid(row=5, column=0, pady=(15, 5), sticky="w")
        CTkButton(self.sidebar, text="■", command=lambda: self.set_fill(True)).grid(row=6, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="□", command=lambda: self.set_fill(False)).grid(row=7, column=0, pady=2, sticky="ew")

        CTkLabel(self.sidebar, text="Színek:", font=("Arial", 14)).grid(row=8, column=0, pady=(15, 5), sticky="w")
        CTkButton(self.sidebar, text="Piros", command=lambda: self.set_color((255, 0, 0))).grid(row=9, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="Zöld", command=lambda: self.set_color((0, 255, 0))).grid(row=10, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="Kék", command=lambda: self.set_color((0, 0, 255))).grid(row=11, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="Színválasztó", command=self.choose_color).grid(row=12, column=0, pady=5, sticky="ew")

        CTkLabel(self.sidebar, text="Vastagság:", font=("Arial", 14)).grid(row=13, column=0, pady=(15, 5), sticky="w")
        slider = CTkSlider(self.sidebar, from_=1, to=10, number_of_steps=9, command=lambda v: self.set_thickness(int(v)))
        slider.set(self.drawing_state["thickness"])
        slider.grid(row=14, column=0, pady=5, sticky="ew")

        CTkLabel(self.sidebar, text="Műveletek:", font=("Arial", 14)).grid(row=15, column=0, pady=(15, 5), sticky="w")
        CTkButton(self.sidebar, text="💾", command=self.save_canvas).grid(row=16, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="💾📁", command=self.save_as).grid(row=17, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="📂📄", command=self.load_canvas).grid(row=18, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="🆑", command=self.clear_canvas).grid(row=19, column=0, pady=2, sticky="ew")
        CTkButton(self.sidebar, text="↩️", command=self.undo).grid(row=20, column=0, pady=2, sticky="ew")

    def embed_pygame(self):
        os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
        hwnd = self.pygame_frame.winfo_id()

        pygame.display.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

        if os.name == "nt":
            ctypes.windll.user32.SetParent(pygame.display.get_wm_info()["window"], hwnd)

        self.run_pygame_loop(screen)

    def run_pygame_loop(self, screen):
        clock = pygame.time.Clock()

        while True:
            screen.fill(BG_COLOR)
            screen.blit(self.canvas, (0, 0))
            self.drawing_state["mouse_pos"] = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.drawing_state["start_pos"] = event.pos
                    self.drawing_state["last_pos"] = event.pos
                    self.drawing_state["drawing"] = True
                    if self.drawing_state["shape"] == "freehand":
                        self.history.append(self.canvas.copy())

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.drawing_state["drawing"]:
                        if self.drawing_state["shape"] != "freehand":
                            end_pos = event.pos
                            rect = pygame.Rect(*self.drawing_state["start_pos"], end_pos[0] - self.drawing_state["start_pos"][0], end_pos[1] - self.drawing_state["start_pos"][1])
                            rect.normalize()
                            self.history.append(self.canvas.copy())
                            if self.drawing_state["shape"] == "line":
                                pygame.draw.line(self.canvas, self.drawing_state["color"], self.drawing_state["start_pos"], end_pos, self.drawing_state["thickness"])
                            else:
                                self.draw_shape(self.canvas, self.drawing_state["shape"], self.drawing_state["color"], rect, self.drawing_state["fill"])
                    self.drawing_state["drawing"] = False
                    self.drawing_state["start_pos"] = None
                    self.drawing_state["last_pos"] = None

                elif event.type == pygame.MOUSEMOTION and self.drawing_state["drawing"]:
                    if self.drawing_state["shape"] == "freehand" and self.drawing_state["last_pos"]:
                        pygame.draw.line(self.canvas, self.drawing_state["color"], self.drawing_state["last_pos"], event.pos, self.drawing_state["thickness"])
                        self.drawing_state["last_pos"] = event.pos

            pygame.display.update()
            clock.tick(60)

    def draw_shape(self, surface, shape, color, rect, fill):
        width = 0 if fill else self.drawing_state["thickness"]
        if shape == "rect":
            pygame.draw.rect(surface, color, rect, width)
        elif shape == "ellipse":
            pygame.draw.ellipse(surface, color, rect, width)

    def set_shape(self, shape, label):
        self.drawing_state["shape"] = shape
        self.drawing_state["current_tool"] = label

    def set_fill(self, val):
        self.drawing_state["fill"] = val

    def set_color(self, color):
        self.drawing_state["color"] = color

    def choose_color(self):
        color = colorchooser.askcolor()[0]
        if color:
            self.set_color(tuple(map(int, color)))

    def set_thickness(self, val):
        self.drawing_drawing_state["thickness"] = val

    def save_canvas(self):
        pygame.image.save(self.canvas, DEFAULT_SAVE)

    def save_as(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if filepath:
            pygame.image.save(self.canvas, filepath)

    def load_canvas(self):
        filepath = filedialog.askopenfilename(filetypes=[("PNG", "*.png")])
        if filepath and os.path.exists(filepath):
            loaded = pygame.image.load(filepath)
            self.canvas.blit(loaded, (0, 0))

    def clear_canvas(self):
        self.history.append(self.canvas.copy())
        self.canvas.fill(BG_COLOR)

    def undo(self):
        if self.history:
            last = self.history.pop()
            self.canvas.blit(last, (0, 0))


if __name__ == "__main__":
    boot = BootApp()
    boot.after(3000, lambda: boot.destroy())
    boot.mainloop()

    app = MainApp()
    app.mainloop()
