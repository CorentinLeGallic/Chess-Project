import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

from objects.Square import Square
from objects.Piece import Roi, Reine, Tour, Fou, Cavalier, Pion

from utils import hex_to_rgb

class Game(ttk.Frame):
    def __init__(self, container, show_rules, open_menu) -> None:
        super().__init__(container)

        self.playing_color = "White"
        self.moves_logs = []
        
        ipadding = {'ipadx': 10, 'ipady': 10}
        
        self.chessboard = tk.Canvas(self, width=677, height=677)
        self.chessboard.bind('<Motion>', self.mouseMove)
        self.chessboard.bind('<Button-1>', self.mouseClick)
        self.chessboard.pack()

        self.squares = self.__creer_plateau()
        self.pieces = self.__creer_pieces()

        self.selected_piece = None

        image = Image.open("./assets/medias/plateau.png")
        self.resized_background = image.resize((682, 682))

        self.background = ImageTk.PhotoImage(self.resized_background)

        self.chessboard_background = self.chessboard.create_image(0, 0, image=self.background, anchor="nw")

        self.images = []

        self.promotion_panel = None

        self.Frame1 = tk.Frame(self, relief="groove")
        self.Frame1.pack(**ipadding )
        
        self.rulesGameBtn = ttk.Button(self.Frame1, text='Rules', command=show_rules,width=80)
        self.rulesGameBtn.pack(ipadx=10, ipady=10, padx=10, pady=10)
        self.pack(expand=True)

        self.open_menu = open_menu

    def start(self):
        # print("Starting the game !")
        for piece in self.pieces["White"] + self.pieces["Black"]:
            piece.place()
        for piece in self.pieces["White"] + self.pieces["Black"]:
            piece.allowed_squares = piece.get_allowed_squares(self.squares, self.pieces, self.moves_logs)

    def switch_to_menu(self):
        self.popup.destroy()
        self.reset()
        self.open_menu()

    def play_again(self):
        self.popup.destroy()
        self.reset()
        self.start()

    def stop(self, reason):
        self.popup = tk.Toplevel(self.winfo_toplevel(), bg="#FFF")

        self.popup_width = 350
        self.popup_height = 200
        self.popup_left_margin = int(self.winfo_screenwidth()/2 - self.popup_width/2)
        self.popup_top_margin = int(self.winfo_screenheight()/2 - self.popup_height/2)

        self.popup.geometry(f"{self.popup_width}x{self.popup_height}+{self.popup_left_margin}+{self.popup_top_margin}")
        self.popup.title("Fin de la partie")

        self.popup.resizable(False, False)
        self.popup.protocol("WM_DELETE_WINDOW", lambda _: print("Trying to close"))

        self.popup.grab_set()

        tk.Label(self.popup, text="Egalité" if reason in ["STALEMATE", "MATERIAL"] else f"Victoire des {'blancs' if self.playing_color == 'White' else 'noirs'}", font=('SegoeUI 18 bold'), bg="#FFF").pack(fill=tk.X, pady=10)
        tk.Label(self.popup, text="par PAT" if reason == "STALEMATE" else "par manque de matériel" if reason == "MATERIAL" else "par échec et mat", font=('Roboto 12'), bg="#FFF").pack(fill=tk.X, pady=10)

        tk.Button(self.popup, text="Menu", command=self.switch_to_menu).pack(side=tk.LEFT, fill=tk.X, padx=20, expand=True)
        tk.Button(self.popup, text="Rejouer", command=self.play_again).pack(side=tk.RIGHT, fill=tk.X, padx=20, expand=True)

    def reset(self):
        self.playing_color = "White"
        self.moves_logs = []
        self.selected_piece = None
        self.promotion_panel = None
        self.images = []

        self.squares = self.__creer_plateau()
        self.pieces = self.__creer_pieces()
        
    def log(self, piece, old_square, new_square, take, promotion=False, roque=False, grand_roque=False):
        self.moves_logs.append({
            "piece": piece,
            "old_square": old_square,
            "new_square": new_square,
            "take": take,
            "promotion": promotion,
            "roque": roque,
            "grand_roque": grand_roque
        })

    def next_turn(self):
        precedent_king = [piece for piece in self.pieces[self.playing_color] if piece.type == "King"][0]
        if precedent_king.is_checked:
            precedent_king.uncheck()

        next_color = "White" if self.playing_color == "Black" else "Black"
        king = [piece for piece in self.pieces[next_color] if piece.type == "King"][0]
        king_attackers = king.square.get_attacking_pieces(self.squares, self.pieces[self.playing_color], self.moves_logs)
        if len(king_attackers) > 1:
            king.check(attacking_pieces=king_attackers, double_check=True)
        elif len(king_attackers) == 1:
            king_attacker = king_attackers[0]
            if king_attacker.type == "Knight":
                king.check(attacking_pieces=king_attackers, knight_check=True)
            elif king_attacker.type == "Pawn":
                king.check(attacking_pieces=king_attackers, pawn_check=True)
            else:
                king.check(attacking_pieces=king_attackers)

        allowed_moves = []
        for piece in self.pieces[next_color]:
            piece.allowed_squares = piece.get_allowed_squares(self.squares, self.pieces, self.moves_logs)
            allowed_moves += piece.allowed_squares
        if len(allowed_moves) == 0:
            if king.is_checked:
                # print("CHECKMATE !")
                self.stop("CHECKMATE")
            else:
                # print("STALEMATE !")
                self.stop("STALEMATE")
        else:
            white_lack_of_material = False
            if len(self.pieces["White"]) == 1:
                white_lack_of_material = True
            elif len(self.pieces["White"]) == 2:
                for piece in self.pieces["White"]:
                    if piece.type in ["Knight, Bishop"]:
                        white_lack_of_material = True

            black_lack_of_material = False
            if len(self.pieces["Black"]) == 1:
                black_lack_of_material = True
            elif len(self.pieces["Black"]) == 2:
                for piece in self.pieces["Black"]:
                    if piece.type in ["Knight, Bishop"]:
                        black_lack_of_material = True

            if white_lack_of_material and black_lack_of_material:
                # print("DRAW - LACK OF MATERIAL")
                self.stop("MATERIAL")
            else:
                self.playing_color = next_color
    
    def get_piece_from_event(self, event):
        for piece in self.pieces["White"] + self.pieces["Black"]:
            piece_coords = self.chessboard.coords(piece.canvas_image)
            if piece_coords[0] < event.x < piece_coords[0] + 85.3 and piece_coords[1] < event.y < piece_coords[1] + 85.3:
                return piece
        return None
    
    def show_promotion_panel(self):
        panel_canvas = tk.Canvas(self.chessboard, width=81.3, height=337, background="#FCFCFC", borderwidth=0, highlightthickness=2, highlightbackground="#DDDDDD", cursor="hand2")
        panel_canvas.bind('<Button-1>', self.promote)

        x_coord = (self.selected_piece.square.coordonnees[0]-1)*85.3
        y_coord = (8-self.selected_piece.square.coordonnees[1])*85 if self.selected_piece.color == "White" else (8-self.selected_piece.square.coordonnees[1]+1)*85 - 339
        self.promotion_panel = self.chessboard.create_window(x_coord, y_coord, window=panel_canvas, anchor=tk.NW)

        knight_image = Image.open(f"./assets/medias/pieces/{self.selected_piece.color.lower()}Knight.png").resize((85, 85))
        self.promotion_knight_image = ImageTk.PhotoImage(knight_image)
        panel_canvas.create_image(0, 0, anchor=tk.NW, image=self.promotion_knight_image)

        bishop_image = Image.open(f"./assets/medias/pieces/{self.selected_piece.color.lower()}Bishop.png").resize((85, 85))
        self.promotion_bishop_image = ImageTk.PhotoImage(bishop_image)
        panel_canvas.create_image(0, 85.3, anchor=tk.NW, image=self.promotion_bishop_image)

        rook_image = Image.open(f"./assets/medias/pieces/{self.selected_piece.color.lower()}Rook.png").resize((85, 85))
        self.promotion_rook_image = ImageTk.PhotoImage(rook_image)
        panel_canvas.create_image(0, 170.6, anchor=tk.NW, image=self.promotion_rook_image)

        queen_image = Image.open(f"./assets/medias/pieces/{self.selected_piece.color.lower()}Queen.png").resize((85, 85))
        self.promotion_queen_image = ImageTk.PhotoImage(queen_image)
        panel_canvas.create_image(0, 255.9, anchor=tk.NW, image=self.promotion_queen_image)

    def hide_promotion_panel(self):
        if self.promotion_panel:
            self.chessboard.delete(self.promotion_panel)
            self.promotion_panel = None

    def get_square_from_event(self, event):
        for square in self.squares:
            if ((square.coordonnees[0]-1) * 85.3 <= event.x < square.coordonnees[0] * 85.3) and ((square.coordonnees[1]-1) * 85.3 <= 682-event.y < square.coordonnees[1] * 85.3):
                return square
        return None
    
    def __create_circle(self, x1, y1, x2, y2, is_empty = False, width = 10, alpha = 1, **kwargs):
        alpha = int(alpha * 275)
        rgb_color = hex_to_rgb(kwargs.pop('fill').replace("#", "")) + (alpha,)
        image = Image.new('RGBA', (int(x2-x1), int(y2-y1)), rgb_color)

        offset = 1
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, image.size[0] - offset, image.size[1] - offset), fill=alpha)

        if is_empty:
            draw.ellipse((width, width, image.size[0] - width, image.size[1] - width), fill=0)

        masked_image = image.copy()
        masked_image.putalpha(mask)

        self.images.append(ImageTk.PhotoImage(masked_image))
        return self.chessboard.create_image(x1, y1, image=self.images[-1], anchor='nw')

    def mouseMove(self, event):
        piece = self.get_piece_from_event(event)
        if piece and piece.color == self.playing_color and not self.promotion_panel:
            self.chessboard.config(cursor="hand2")
        else:
            self.chessboard.config(cursor="")

    def promote(self, event):
        knight_y = (0, 85.3)
        bishop_y = (85.3, 170.6)
        rook_y = (170.6, 255.9)
        queen_y = (255.9, 341.2)
        if knight_y[0] <= event.y <= queen_y[1]:
            king = [piece for piece in self.pieces["White"] + self.pieces["Black"] if piece.type == "King" and piece.color == self.promotion_status["piece"].color][0]
            if knight_y[0] <= event.y <= knight_y[1]:
                new_piece = Cavalier(self.chessboard, self.promotion_status["piece"].color, [square for square in self.squares if square.coordonnees == self.promotion_status["piece"].square.coordonnees][0], king)
                self.pieces[self.promotion_status["piece"].color].append(new_piece)
                # print(f"Knight promotion - {self.playing_color}")
            elif bishop_y[0] < event.y <= bishop_y[1]:
                new_piece = Fou(self.chessboard, self.promotion_status["piece"].color, [square for square in self.squares if square.coordonnees == self.promotion_status["piece"].square.coordonnees][0], king)
                self.pieces[self.promotion_status["piece"].color].append(new_piece)
                # print(f"Bishop promotion - {self.playing_color}")
            elif rook_y[0] < event.y <= rook_y[1]:
                new_piece = Tour(self.chessboard, self.promotion_status["piece"].color, [square for square in self.squares if square.coordonnees == self.promotion_status["piece"].square.coordonnees][0], king)
                self.pieces[self.promotion_status["piece"].color].append(new_piece)
                # print(f"Rook promotion - {self.playing_color}")
            elif queen_y[0] < event.y <= queen_y[1]:
                new_piece = Reine(self.chessboard, self.promotion_status["piece"].color, [square for square in self.squares if square.coordonnees == self.promotion_status["piece"].square.coordonnees][0], king)
                self.pieces[self.promotion_status["piece"].color].append(new_piece)
                # print(f"Queen promotion - {self.playing_color}")
            new_piece.place()

            self.log(
                piece=self.promotion_status["piece"],
                old_square=self.promotion_status["old_square"],
                new_square=self.promotion_status["new_square"],
                take=self.promotion_status["take"],
                promotion=True
            )
            self.next_turn()

            self.promotion_status["piece"].take()
            self.pieces[self.promotion_status["piece"].color].remove(self.promotion_status["piece"])
            self.promotion_status = {}
            self.hide_promotion_panel()
        else:
            print("Error with promotion_panel clic coords")

    def mouseClick(self, event):
        if not self.promotion_panel:
            clicked_square = self.get_square_from_event(event)
            clicked_piece = self.get_piece_from_event(event)
            if self.selected_piece and clicked_piece != self.selected_piece:
                if clicked_square in self.selected_piece.allowed_squares:
                    if self.selected_piece.type == "Pawn" and clicked_square.coordonnees[1] in [1, 8]:
                        # print(f"{self.playing_color} is promoting")

                        if clicked_piece:
                            clicked_piece.take()
                            self.pieces[clicked_piece.color].remove(clicked_piece)
                        
                        self.promotion_status = {
                            "piece": self.selected_piece,
                            "take": clicked_piece,
                            "old_square": self.selected_piece.square,
                            "new_square": clicked_square,
                        }
                        self.selected_piece.place(clicked_square)

                        self.promotion_status["piece"] = self.selected_piece
                        self.show_promotion_panel()

                        self.selected_piece.unselect()
                        self.selected_piece = None
                        self.hide_allowed_squares()
                    else:
                        if self.selected_piece.type == "Rook" and not self.selected_piece.has_already_moved:
                            king = [piece for piece in self.pieces[self.selected_piece.color] if piece.type == "King"][0]
                            if self.selected_piece.square.coordonnees[0] == 1:
                                king.has_a_rook_moved = True
                            elif self.selected_piece.square.coordonnees[0] == 8:
                                king.has_h_rook_moved = True
                        if clicked_piece:
                            if self.selected_piece.type == "King" and clicked_piece.color == self.selected_piece.color and clicked_piece.type == "Rook":
                                if clicked_piece.square.coordonnees[0] == 1:
                                    clicked_piece.place([square for square in self.squares if square.coordonnees == [4, self.selected_piece.square.coordonnees[1]]][0])
                                    self.selected_piece.place([square for square in self.squares if square.coordonnees == [3, self.selected_piece.square.coordonnees[1]]][0])
                                    self.log(
                                        piece=self.selected_piece,
                                        old_square=self.selected_piece.square,
                                        new_square=clicked_square,
                                        take=False,
                                        grand_roque=True
                                    )
                                elif clicked_piece.square.coordonnees[0] == 8:
                                    clicked_piece.place([square for square in self.squares if square.coordonnees == [6, self.selected_piece.square.coordonnees[1]]][0])
                                    self.selected_piece.place([square for square in self.squares if square.coordonnees == [7, self.selected_piece.square.coordonnees[1]]][0])
                                    self.log(
                                        piece=self.selected_piece,
                                        old_square=self.selected_piece.square,
                                        new_square=clicked_square,
                                        take=False,
                                        roque=True
                                    )
                                self.selected_piece.unselect()
                                self.selected_piece = None
                                self.hide_allowed_squares()
                                self.next_turn()
                            else:
                                self.log(
                                    piece=self.selected_piece,
                                    old_square=self.selected_piece.square,
                                    new_square=clicked_square,
                                    take=True
                                )
                                clicked_piece.take()
                                self.pieces[clicked_piece.color].remove(clicked_piece)
                                self.selected_piece.place(clicked_square)

                                self.selected_piece.unselect()
                                self.selected_piece = None
                                self.hide_allowed_squares()
                                self.next_turn()
                        else:
                            distance = 1 if self.selected_piece.color == "White" else -1
                            if self.selected_piece.type == "Pawn" and clicked_square.coordonnees in [[self.selected_piece.square.coordonnees[0] + 1, self.selected_piece.square.coordonnees[1] + distance], [self.selected_piece.square.coordonnees[0] - 1, self.selected_piece.square.coordonnees[1] + distance]]:
                                self.moves_logs[-1]["piece"].take()
                                self.pieces[self.moves_logs[-1]["piece"].color].remove(self.moves_logs[-1]["piece"])
                                self.log(
                                    piece=self.selected_piece,
                                    old_square=self.selected_piece.square,
                                    new_square=clicked_square,
                                    take=True
                                )
                            else:
                                self.log(
                                    piece=self.selected_piece,
                                    old_square=self.selected_piece.square,
                                    new_square=clicked_square,
                                    take=False
                                )
                            self.selected_piece.place(clicked_square)
                            
                            self.selected_piece.unselect()
                            self.selected_piece = None
                            self.hide_allowed_squares()

                            self.next_turn()
                elif clicked_piece and clicked_piece.color == self.playing_color:
                    self.selected_piece.unselect()
                    self.selected_piece = None
                    self.hide_allowed_squares()

                    self.selected_piece = clicked_piece
                    clicked_piece.select()
                    self.show_allowed_squares()

                elif not clicked_piece:
                    self.selected_piece.unselect()
                    self.selected_piece = None
                    self.hide_allowed_squares()
            elif clicked_piece and clicked_piece != self.selected_piece:
                if clicked_piece.color == self.playing_color:
                    self.selected_piece = clicked_piece
                    clicked_piece.select()
                    self.show_allowed_squares()
            elif self.selected_piece and clicked_piece and clicked_piece == self.selected_piece:
                self.selected_piece.unselect()
                self.selected_piece = None
                self.hide_allowed_squares()

    def show_allowed_squares(self):
        if self.selected_piece:
            self.allowed_squares = self.selected_piece.allowed_squares
            self.allowed_circles = []

            for square in self.allowed_squares:
                if square.contain_piece:
                    self.allowed_circles.append(self.__create_circle((square.coordonnees[0]-1) * 85.3 - 1, 682-(square.coordonnees[1]) * 85.3, (square.coordonnees[0]) * 85.3, 682-(square.coordonnees[1]-1) * 85.3, is_empty=True, width=10, alpha=.1, fill="#000000", outline=""))
                else:
                    self.allowed_circles.append(self.__create_circle((square.coordonnees[0]-1) * 85.3 - 1 + 27, 682-(square.coordonnees[1]) * 85.3 + 27, (square.coordonnees[0]) * 85.3 - 27, 682-(square.coordonnees[1]-1) * 85.3 - 27, alpha=.1, fill="#000000", outline=""))

    def hide_allowed_squares(self):
        if self.allowed_squares:
            for circle in self.allowed_circles:
                self.chessboard.delete(circle)

    def __creer_plateau(self):
        L = []
        i = 0
        for a in reversed(range(8)):
            for b in range(8):   
                i += 1
                L.append(Square(i, [b + 1, a + 1]))
        return L
    
    def __creer_pieces(self):
        white_king = Roi(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [5, 1]][0])
        black_king = Roi(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [5, 8]][0])
        return {
            "White": [
                Tour(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [1, 1]][0], white_king),
                Cavalier(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [2, 1]][0], white_king),
                Fou(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [3, 1]][0], white_king),
                Reine(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [4, 1]][0], white_king),
                white_king,
                Fou(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [6, 1]][0], white_king),
                Cavalier(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [7, 1]][0], white_king),
                Tour(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [8, 1]][0], white_king),
                Pion(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [1, 2]][0], white_king),
                Pion(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [2, 2]][0], white_king),
                Pion(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [3, 2]][0], white_king),
                Pion(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [4, 2]][0], white_king),
                Pion(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [5, 2]][0], white_king),
                Pion(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [6, 2]][0], white_king),
                Pion(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [7, 2]][0], white_king),
                Pion(self.chessboard, "White", [square for square in self.squares if square.coordonnees == [8, 2]][0], white_king),
            ],
            "Black": [
                Tour(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [1, 8]][0], black_king),
                Cavalier(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [2, 8]][0], black_king),
                Fou(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [3, 8]][0], black_king),
                Reine(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [4, 8]][0], black_king),
                black_king,
                Fou(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [6, 8]][0], black_king),
                Cavalier(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [7, 8]][0], black_king),
                Tour(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [8, 8]][0], black_king),
                Pion(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [1, 7]][0], black_king),
                Pion(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [2, 7]][0], black_king),
                Pion(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [3, 7]][0], black_king),
                Pion(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [4, 7]][0], black_king),
                Pion(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [5, 7]][0], black_king),
                Pion(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [6, 7]][0], black_king),
                Pion(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [7, 7]][0], black_king),
                Pion(self.chessboard, "Black", [square for square in self.squares if square.coordonnees == [8, 7]][0], black_king),
            ]
        }

