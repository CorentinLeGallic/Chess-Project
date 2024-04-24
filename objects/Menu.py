import tkinter as tk
from tkinter import ttk

class Menu(ttk.Frame):
    def __init__(self, container, start_game) -> None:
        super().__init__(container, relief="groove", borderwidth=3, width=1000, height=1000)

        # self.canvas = tk.Canvas(self, width=1920, height=1080, borderwidth=2, relief="groove")
        # self.canvas.pack()

        # self.width = self.winfo_screenwidth()
        # self.height = self.winfo_screenheight()

        # self.texte1 = self.canvas.create_text((700, 100), text="Bienvenue dans", fill="black", font=('Roboto', 30), anchor="n")
        # self.texte2 = self.canvas.create_text((700, 200), text="PyChess", fill="black", font=("Arial", 50))

        # self.button1 = ttk.Button(text = "Play",command=start_game)

        # self.button1_width = self.button1.winfo_width()
        # self.button1_height = self.button1.winfo_height()

        # self.button1_canvas = self.canvas.create_window(self.width/2-(self.button1_width/2), self.height/2-(self.button1_height/2), anchor = "nw",window = self.button1)

        # self.pack(expand=True)

        self.container = tk.Frame(self)
        self.container.pack(expand=True, anchor=tk.CENTER)

        self.texte1 = tk.Label(self.container, text="Bienvenue dans", font=('Roboto', 30))
        self.texte2 = tk.Label(self.container, text="PyChess", font=("Arial", 50))

        self.texte1.pack()
        self.texte2.pack(pady=10)

        self.button1 = ttk.Button(self.container, text="Play", command=start_game)

        self.button1_width = self.button1.winfo_width()
        self.button1_height = self.button1.winfo_height()

        self.button1.pack(pady=30)

        self.pack(expand=True, fill=tk.BOTH)