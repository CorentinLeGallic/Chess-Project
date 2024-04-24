import tkinter as tk
from tkinter import ttk
from objects.Menu import Menu
from objects.Game import Game
from utils import open_link

class Router(ttk.Frame):
    def __init__(self, container) -> None:
        super().__init__(container)

        self.selectedFrame = "Menu"
        self.frames = {
            "Menu":Menu(container, start_game=self.start_game),
            "Game":Game(container, show_rules=self.afficher_regles, open_menu=self.open_menu)
        }

        self.frames["Game"].forget()

    def afficher_regles(self):
        rules_file = open("./assets/rules.txt", encoding='utf-8')
        regles = rules_file.read()
        
        popup = tk.Toplevel(self.winfo_toplevel(), bg="#FFF")

        popup_width = 450
        popup_height = 450
        popup_left_margin = int(self.winfo_screenwidth()/2 - popup_width/2)
        popup_top_margin = int(self.winfo_screenheight()/2 - popup_height/2)

        popup.geometry(f"{popup_width}x{popup_height}+{popup_left_margin}+{popup_top_margin}")
        popup.title("Règles du jeu d'échecs")
        popup.resizable(False, False)

        tk.Label(popup, text="Règles du jeu d'échecs :", font=('SegoeUI 18 bold'), bg="#FFF").pack(fill=tk.X, pady=10)
        tk.Label(popup, text=regles, font=('Roboto 10'), justify=tk.LEFT, wraplength=popup_width - 20, bg="#FFF").pack(padx=10)
        tk.Label(popup, text="Pour en savoir plus sur les règles des échecs :", font=('Roboto 10'), bg="#FFF").pack(fill=tk.X)

        link = "https://ecole.apprendre-les-echecs.com/regles-echecs/"
        link_button = tk.Button(popup, text=link, borderwidth=0, fg="#0000EE", cursor="hand2", bg="#FFF")
        link_button.pack()

        link_button.bind("<Button-1>", lambda _: open_link(link))

    def start_game(self):
        self.switch_frame("Game")
        self.frames["Game"].start()
        
    def open_menu(self):
        self.switch_frame("Menu")

    def switch_frame(self, frame):
        self.frames[self.selectedFrame].forget()
        self.selectedFrame = frame
        if(frame == "Game"):
            self.frames[self.selectedFrame].pack(expand=True)
        else:
            self.frames[self.selectedFrame].pack(expand=True, fill=tk.BOTH)