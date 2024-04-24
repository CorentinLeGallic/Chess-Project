import tkinter as tk
from tkinter import ttk

class Rules(ttk.Frame):
    def __init__(self, container, rulesGames) -> None:
        super().__init__(container, borderwidth=3, relief="groove")
                
        ipadding = {'ipadx': 10, 'ipady': 10}
        self.label1 = tk.Label(self, text='RULES', bg="red", fg="white")
        self.label1.pack(**ipadding, expand=True, fill=tk.BOTH, side=tk.LEFT, anchor="n")

        self.startGameBtn = ttk.Button(self, text='Play', command=rulesGames, width=80)
        self.startGameBtn.pack(expand=True, ipady=10, anchor='center', pady=10)