import tkinter as tk

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("Chess Project")
        self.iconbitmap('./assets/medias/icon.ico')

        min_width = 1080
        min_height = 740

        max_width = 1920
        max_height = 1080

        self.minsize(min_width, min_height)
        self.maxsize(max_width, max_height)

        self.state("zoomed")