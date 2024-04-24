import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from math import sqrt

class Piece:
    def __init__(self, chessboard, color, square, imagePath, piece_type) :
        self.color = color
        self.square = square
        self.canvas = chessboard
        self.type = piece_type

        self.__image = Image.open(imagePath).resize((85, 85))
        self.__piece_image = ImageTk.PhotoImage(self.__image)

        self.has_already_moved = False
        self.has_been_taken = False

        self.allowed_squares = []

        # self.tab_bind = f"{square.coordonnees[0]}-{square.coordonnees[1]}"

    def place(self, newSquare=False):
        if newSquare:
            self.square.contain_piece = False
            self.square = newSquare
            # self.tab_bind = f"{newSquare.coordonnees[0]}-{newSquare.coordonnees[1]}"
        # print("Self.square : ", self.square)
        self.square.contain_piece = self.color
        if hasattr(self, "canvas_image"):
            self.canvas.coords(self.canvas_image, (self.square.coordonnees[0]-1) * 85.3, (8-self.square.coordonnees[1]) * 85.3)
            self.has_already_moved = True
        else:
            self.canvas_image = self.canvas.create_image((self.square.coordonnees[0]-1) * 85.3, (8-self.square.coordonnees[1]) * 85.3, anchor=tk.NW, image=self.__piece_image)

    def take(self):
        self.forget()
        self.has_been_taken = True

    def forget(self):
        self.canvas.delete(self.canvas_image)
        self.square.contain_piece = False
        self.square = None

    def select(self):
        # print(f"{self.color} selected {self}")
        self.selection_rectangle = self.canvas.create_rectangle(((self.square.coordonnees[0]-1) * 85.3 - 1, 682-(self.square.coordonnees[1]-1) * 85.3), ((self.square.coordonnees[0]) * 85.3, 682-(self.square.coordonnees[1]) * 85.3), fill="#ABA23A", outline="")
        self.canvas.tag_raise(self.canvas_image)

    def unselect(self):
        # print(f"{self.color} unselected {self}")
        self.canvas.delete(self.selection_rectangle)

    def __str__(self) -> str:
        return f"{self.type} - {self.color} - {self.square.coordonnees}"
    
    def get_orthogonal_pin(self, pieces, squares, move_logs):
        king = [piece for piece in pieces[self.color] if piece.type == "King"][0]
        if self.square.coordonnees[0] == king.square.coordonnees[0]:
            pining_piece = [piece for piece in pieces["White" if self.color == "Black" else "Black"] if piece.type in ["Rook", "Queen"] and piece.square.coordonnees[0] == self.square.coordonnees[0] and (piece.square.coordonnees[1] > self.square.coordonnees[1] > king.square.coordonnees[1] or piece.square.coordonnees[1] < self.square.coordonnees[1] < king.square.coordonnees[1]) and self.square in piece.get_attacked_squares(squares, move_logs)]
            if len(pining_piece) > 0:
                between_squares = [square for square in squares if square.coordonnees[0] == self.square.coordonnees[0] and (self.square.coordonnees[1] > square.coordonnees[1] > king.square.coordonnees[1] or self.square.coordonnees[1] < square.coordonnees[1] < king.square.coordonnees[1]) and square.contain_piece]
                if len(between_squares) == 0:
                    return {
                        "vertical": True,
                        "horizontal": False
                    }
            return {
                "vertical": False,
                "horizontal": False
            }
        elif self.square.coordonnees[1] == king.square.coordonnees[1]:
            pining_piece = [piece for piece in pieces["White" if self.color == "Black" else "Black"] if piece.type in ["Rook", "Queen"] and piece.square.coordonnees[1] == self.square.coordonnees[1] and (piece.square.coordonnees[0] > self.square.coordonnees[0] > king.square.coordonnees[0] or piece.square.coordonnees[0] < self.square.coordonnees[0] < king.square.coordonnees[0]) and self.square in piece.get_attacked_squares(squares, move_logs)]
            if len(pining_piece) > 0:
                between_squares = [square for square in squares if square.coordonnees[1] == self.square.coordonnees[1] and (self.square.coordonnees[0] > square.coordonnees[0] > king.square.coordonnees[0] or self.square.coordonnees[0] < square.coordonnees[0] < king.square.coordonnees[0]) and square.contain_piece]
                if len(between_squares) == 0:
                    return {
                        "vertical": False,
                        "horizontal": True
                    }
            return {
                "vertical": False,
                "horizontal": False
            }
        else:
            return {
                "vertical": False,
                "horizontal": False
            }
        
    def get_diagonal_pin(self, pieces, squares, move_logs):
        king = [piece for piece in pieces[self.color] if piece.type == "King"][0]

        top_to_bottom_squares = []
        bottom_to_top_squares = []

        right_top_squares = [square for square in squares if square.index % 7 == king.square.index % 7 and square.index < king.square.index and square.index != king.square.index]
        if not king.square.coordonnees[0] == 8:
            for square in reversed(right_top_squares):
                bottom_to_top_squares.append(square)
                if square.coordonnees[0] == 8:
                    break
        
        left_top_squares = [square for square in squares if square.index % 9 == king.square.index % 9 and square.index < king.square.index and square.index != king.square.index]
        if not king.square.coordonnees[0] == 1:
            for square in reversed(left_top_squares):
                top_to_bottom_squares.append(square)
                if square.coordonnees[0] == 1:
                    break
        
        left_bottom_squares = [square for square in squares if square.index % 7 == king.square.index % 7 and square.index > king.square.index and square.index != king.square.index]
        if not king.square.coordonnees[0] == 1:
            for square in left_bottom_squares:
                bottom_to_top_squares.append(square)
                if square.coordonnees[0] == 1:
                    break
        
        right_bottom_squares = [square for square in squares if square.index % 9 == king.square.index % 9 and square.index > king.square.index and square.index != king.square.index]
        if not king.square.coordonnees[0] == 8:
            for square in right_bottom_squares:
                top_to_bottom_squares.append(square)
                if square.coordonnees[0] == 8:
                    break

        if self.square in top_to_bottom_squares:
            pining_piece = [piece for piece in pieces["White" if self.color == "Black" else "Black"] if piece.type in ["Bishop", "Queen"] and piece.square in top_to_bottom_squares and (piece.square.coordonnees[1] > self.square.coordonnees[1] > king.square.coordonnees[1] or piece.square.coordonnees[1] < self.square.coordonnees[1] < king.square.coordonnees[1]) and self.square in piece.get_attacked_squares(squares, move_logs)]
            if len(pining_piece) > 0:
                between_squares = [square for square in squares if square in top_to_bottom_squares and (self.square.coordonnees[1] > square.coordonnees[1] > king.square.coordonnees[1] or self.square.coordonnees[1] < square.coordonnees[1] < king.square.coordonnees[1]) and square.contain_piece]
                if len(between_squares) == 0:
                    return {
                        "top_to_bottom": True,
                        "bottom_to_top": False
                    }
            return {
                "top_to_bottom": False,
                "bottom_to_top": False
            }
        elif self.square in bottom_to_top_squares:
            pining_piece = [piece for piece in pieces["White" if self.color == "Black" else "Black"] if piece.type in ["Bishop", "Queen"] and piece.square in bottom_to_top_squares and (piece.square.coordonnees[1] > self.square.coordonnees[1] > king.square.coordonnees[1] or piece.square.coordonnees[1] < self.square.coordonnees[1] < king.square.coordonnees[1]) and self.square in piece.get_attacked_squares(squares, move_logs)]
            if len(pining_piece) > 0:
                between_squares = [square for square in squares if square in bottom_to_top_squares and (self.square.coordonnees[1] > square.coordonnees[1] > king.square.coordonnees[1] or self.square.coordonnees[1] < square.coordonnees[1] < king.square.coordonnees[1]) and square.contain_piece]
                if len(between_squares) == 0:
                    return {
                        "top_to_bottom": False,
                        "bottom_to_top": True
                    }
            return {
                "top_to_bottom": False,
                "bottom_to_top": False
            }
        else:
            return {
                "top_to_bottom": False,
                "bottom_to_top": False
            }
                    
class Roi(Piece):
    def __init__(self, canvas, color, square):
        super().__init__(canvas, color, square, f"./assets/medias/pieces/{color.lower()}King.png", "King")

        self.has_a_rook_moved = False
        self.has_h_rook_moved = False

        self.is_checked = False
        self.check_status = {
            "double_check": False,
            "knight_check": False,
            "pawn_check": False,
            "regular_check": False,
            "attacking_pieces": []
        }

    def select(self):
        super().select()
        if self.is_checked:
            self.canvas.tag_raise(self.canvas_check_image)
            self.canvas.tag_raise(self.canvas_image)

    def check(self, attacking_pieces, double_check=False, knight_check=False, pawn_check=False):

        # imgsize = (85, 85) #The size of the image

        # image = Image.new('RGBA', imgsize) #Create the image

        # innerColor = [255, 0, 0, 255] #Color at the center
        # outerColor = [0, 0, 0, 0] #Color at the corners


        # for y in range(imgsize[1]):
        #     for x in range(imgsize[0]):

        #         distanceToCenter = sqrt((x - imgsize[0]/2) ** 2 + (y - imgsize[1]/2) ** 2)

        #         distanceToCenter = float(distanceToCenter) / (sqrt(2) * imgsize[0]/2)

        #         r = innerColor[0]
        #         g = innerColor[1]
        #         b = innerColor[2]
        #         a = outerColor[3] * distanceToCenter + innerColor[3] * (1 - distanceToCenter)

        #         image.putpixel((x, y), (int(r), int(g), int(b), int(a)))
        
        # image.save("./assets/medias/check.png")

        # print(f"{self.color} king is checked")

        image = Image.open("./assets/medias/check.png").resize((85, 85))
        self.check_image = ImageTk.PhotoImage(image)
        self.canvas_check_image = self.canvas.create_image((self.square.coordonnees[0]-1) * 85.3, (8-self.square.coordonnees[1]) * 85.3, anchor=tk.NW, image=self.check_image)
        self.canvas.tag_raise(self.canvas_image)

        self.is_checked = True
        self.check_status = {
            "double_check": double_check,
            "knight_check": knight_check,
            "pawn_check": pawn_check,
            "regular_check": True if not (double_check or knight_check or pawn_check) else False,
            "attacking_pieces": attacking_pieces
        }

    def uncheck(self):

        # print(f"{self.color} king is unchecked")

        self.is_checked = False
        self.check_status = {
            "double_check": False,
            "knight_check": False,
            "pawn_check": False,
            "regular_check": False,
            "attacking_pieces": []
        }
        self.canvas.delete(self.canvas_check_image)

    def get_attacked_squares(self, squares, move_logs):
        return [square for square in squares if square.coordonnees[0] in [self.square.coordonnees[0] - 1, self.square.coordonnees[0], self.square.coordonnees[0] + 1] and square.coordonnees[1] in [self.square.coordonnees[1] - 1, self.square.coordonnees[1], self.square.coordonnees[1] + 1] and square.index != self.square.index]
        
    def get_allowed_squares(self, squares, pieces, move_logs):
        castle_is_allowed = True if not self.has_already_moved and not self.has_h_rook_moved and len([square for square in squares if square.coordonnees in [[self.square.coordonnees[0] + 1, self.square.coordonnees[1]], [self.square.coordonnees[0] + 2, self.square.coordonnees[1]]] and square.get_attacking_pieces(squares, pieces["White" if self.color == "Black" else "Black"], move_logs) == [] and not square.contain_piece]) == 2 and not self.is_checked else False
        long_castle_is_allowed = True if not self.has_already_moved and not self.has_a_rook_moved and len([square for square in squares if ((square.coordonnees in [[self.square.coordonnees[0] - 1, self.square.coordonnees[1]], [self.square.coordonnees[0] - 2, self.square.coordonnees[1]]] and square.get_attacking_pieces(squares, pieces["White" if self.color == "Black" else "Black"], move_logs) == []) or square.coordonnees == [2, self.square.coordonnees[1]]) and not square.contain_piece]) == 3 and not self.is_checked else False
        castle_squares = []
        if castle_is_allowed:
            castle_squares += [square for square in squares if square.coordonnees == [8, self.square.coordonnees[1]]]
        if long_castle_is_allowed:
            castle_squares += [square for square in squares if square.coordonnees == [1, self.square.coordonnees[1]]]
        
        attacked_squares = self.get_attacked_squares(squares, move_logs)
        if self.is_checked:
            for i in range(len(self.check_status["attacking_pieces"])):
                attacking_piece = self.check_status["attacking_pieces"][i]
                if self.square.coordonnees[0] == attacking_piece.square.coordonnees[0]:
                    # print("Vertical check")
                    attacked_squares = [square for square in attacked_squares if square.coordonnees[0] != self.square.coordonnees[0] or square == attacking_piece.square] 
                elif self.square.coordonnees[1] == attacking_piece.square.coordonnees[1]:
                    # print("Horizontal check")
                    attacked_squares = [square for square in attacked_squares if square.coordonnees[1] != self.square.coordonnees[1] or square == attacking_piece.square]
                elif abs(attacking_piece.square.coordonnees[0] - self.square.coordonnees[0]) == abs(attacking_piece.square.coordonnees[1] - self.square.coordonnees[1]) and attacking_piece.type != "Pawn":
                    # print("Diagonal check")
                    attacked_squares = [square for square in attacked_squares if not abs(square.coordonnees[0] - attacking_piece.square.coordonnees[0]) == abs(square.coordonnees[1] - attacking_piece.square.coordonnees[1]) or square == attacking_piece.square]
        return [square for square in attacked_squares if not square.contain_piece == self.color and not square.get_attacking_pieces(squares, pieces["White" if self.color == "Black" else "Black"], move_logs)] + castle_squares

class Pion(Piece):
    def __init__(self, canvas, color, square, king):
        super().__init__(canvas, color, square, f"./assets/medias/pieces/{color.lower()}Pawn.png", "Pawn")
        self.king = king

    def get_attacked_squares(self, squares, move_logs):
        distance = 1 if self.color == "White" else -1
        return [square for square in squares if square.coordonnees in [[self.square.coordonnees[0] - 1, self.square.coordonnees[1] + distance], [self.square.coordonnees[0] + 1, self.square.coordonnees[1] + distance]] not in [self.color, False]]

    def get_allowed_squares(self, squares, pieces, move_logs):
        allowed_squares = []
        attacked_squares = [square for square in self.get_attacked_squares(squares, move_logs) if square.contain_piece not in [False, self.color]]
        move_squares = []
        en_passant_square = []
        
        if self.color == "White":
            top_square = [square for square in squares if square.coordonnees == [self.square.coordonnees[0], self.square.coordonnees[1] + 1]][0]
            move_squares = [square for square in squares if (square.coordonnees == [self.square.coordonnees[0], self.square.coordonnees[1] + 1] or (self.square.coordonnees[1] == 2 and square.coordonnees == [self.square.coordonnees[0], self.square.coordonnees[1] + 2] and not [square for square in squares if square.coordonnees == [self.square.coordonnees[0], self.square.coordonnees[1] + 2]][0].contain_piece)) and not top_square.contain_piece]
            if move_logs != [] and move_logs[-1]["piece"].type == "Pawn" and move_logs[-1]["old_square"].coordonnees == [move_logs[-1]["new_square"].coordonnees[0], move_logs[-1]["new_square"].coordonnees[1] + 2]:
                if move_logs[-1]["new_square"].coordonnees == [self.square.coordonnees[0] - 1, self.square.coordonnees[1]]:
                    en_passant_square = [square for square in squares if square.coordonnees == [self.square.coordonnees[0] - 1, self.square.coordonnees[1] + 1]]
                elif move_logs[-1]["new_square"].coordonnees == [self.square.coordonnees[0] + 1, self.square.coordonnees[1]]:
                    en_passant_square = [square for square in squares if square.coordonnees == [self.square.coordonnees[0] + 1, self.square.coordonnees[1] + 1]]
        elif self.color == "Black":
            bottom_square = [square for square in squares if square.coordonnees == [self.square.coordonnees[0], self.square.coordonnees[1] - 1]][0]
            move_squares = [square for square in squares if (square.coordonnees == [self.square.coordonnees[0], self.square.coordonnees[1] - 1] or (self.square.coordonnees[1] == 7 and square.coordonnees == [self.square.coordonnees[0], self.square.coordonnees[1] - 2] and not [square for square in squares if square.coordonnees == [self.square.coordonnees[0], self.square.coordonnees[1] - 2]][0].contain_piece)) and not bottom_square.contain_piece]
            if move_logs != [] and move_logs[-1]["piece"].type == "Pawn" and move_logs[-1]["old_square"].coordonnees == [move_logs[-1]["new_square"].coordonnees[0], move_logs[-1]["new_square"].coordonnees[1] - 2]:
                if move_logs[-1]["new_square"].coordonnees == [self.square.coordonnees[0] - 1, self.square.coordonnees[1]]:
                    en_passant_square = [square for square in squares if square.coordonnees == [self.square.coordonnees[0] - 1, self.square.coordonnees[1] - 1]]
                elif move_logs[-1]["new_square"].coordonnees == [self.square.coordonnees[0] + 1, self.square.coordonnees[1]]:
                    en_passant_square = [square for square in squares if square.coordonnees == [self.square.coordonnees[0] + 1, self.square.coordonnees[1] - 1]]
        
        orthogonal_pin = self.get_orthogonal_pin(pieces=pieces, squares=squares, move_logs=move_logs)
        if orthogonal_pin["horizontal"]:
            return []
        elif orthogonal_pin["vertical"]:
            allowed_squares = move_squares
        else:
            diagonal_pin = self.get_diagonal_pin(pieces=pieces, squares=squares, move_logs=move_logs)
            if diagonal_pin["top_to_bottom"]:
                left_attacked_square = [square for square in attacked_squares if square.coordonnees == [self.square.coordonnees[0] - 1, self.square.coordonnees[1] + (1 if self.color == "White" else -1)]]
                if len(left_attacked_square) == 1:
                    allowed_squares = [left_attacked_square[0]]
                else:
                    return []
            elif diagonal_pin["bottom_to_top"]:
                right_attacked_square = [square for square in attacked_squares if square.coordonnees == [self.square.coordonnees[0] - 1, self.square.coordonnees[1] + (1 if self.color == "White" else -1)]]
                if len(right_attacked_square) == 1:
                    allowed_squares = [right_attacked_square[0]]
                else:
                    return []
            else:
                allowed_squares = move_squares + attacked_squares + en_passant_square        
        
        if self.king.is_checked:
            if self.king.check_status["knight_check"] or self.king.check_status["pawn_check"]:
                return [square for square in attacked_squares if square in allowed_squares and square == self.king.check_status["attacking_pieces"][0].square]
            elif self.king.check_status["regular_check"]:
                attacking_piece = self.king.check_status["attacking_pieces"][0]
                if self.king.square.coordonnees[0] == attacking_piece.square.coordonnees[0]:
                    # return [square for square in allowed_squares if square.coordonnees[0] == self.king.square.coordonnees[0] and ((attacking_piece.square.coordonnees[1] <= square.coordonnees[1] < self.king.square.coordonnees[1]) or (attacking_piece.square.coordonnees[1] > square.coordonnees[1] > self.king.square.coordonnees[1]))]
                    return [square for square in allowed_squares if square == attacking_piece.square]
                elif self.king.square.coordonnees[1] == attacking_piece.square.coordonnees[1]:
                    return [square for square in allowed_squares if square.coordonnees[1] == self.king.square.coordonnees[1] and ((attacking_piece.square.coordonnees[0] <= square.coordonnees[0] < self.king.square.coordonnees[0]) or (attacking_piece.square.coordonnees[0] > square.coordonnees[0] > self.king.square.coordonnees[0]))]
                elif abs(attacking_piece.square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(attacking_piece.square.coordonnees[1] - self.king.square.coordonnees[1]):
                    return [square for square in allowed_squares if abs(square.coordonnees[0] - attacking_piece.square.coordonnees[0]) == abs(square.coordonnees[1] - attacking_piece.square.coordonnees[1]) and abs(square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(square.coordonnees[1] - self.king.square.coordonnees[1]) and (self.king.square.coordonnees[0] < square.coordonnees[0] <= attacking_piece.square.coordonnees[0] or self.king.square.coordonnees[0] > square.coordonnees[0] >= attacking_piece.square.coordonnees[0])]
            elif self.king.check_status["double_check"]:
                return []
        else:
            return allowed_squares

class Tour(Piece):
    def __init__(self, canvas, color, square, king):
        super().__init__(canvas, color, square, f"./assets/medias/pieces/{color.lower()}Rook.png", "Rook")
        self.king = king

    def get_attacked_squares(self, squares, move_logs):
        accessible_squares = []
        left_squares = [square for square in squares if square.coordonnees[1] == self.square.coordonnees[1] and square.index < self.square.index]
        for square in reversed(left_squares):
            accessible_squares.append(square)
            if square.contain_piece:
                break
        right_squares = [square for square in squares if square.coordonnees[1] == self.square.coordonnees[1] and square.index > self.square.index]
        for square in right_squares:
            accessible_squares.append(square)
            if square.contain_piece:
                break
        top_squares = [square for square in squares if square.coordonnees[0] == self.square.coordonnees[0] and square.index < self.square.index]
        i = 0
        for square in reversed(top_squares):
            i += 1
            accessible_squares.append(square)
            if square.contain_piece:
                break
        bottom_squares = [square for square in squares if square.coordonnees[0] == self.square.coordonnees[0] and square.index > self.square.index]
        for square in bottom_squares:
            accessible_squares.append(square)
            if square.contain_piece:
                break
        return accessible_squares
    
    def get_allowed_squares(self, squares, pieces, move_logs):
        allowed_squares = []
        for pin_value in self.get_diagonal_pin(pieces=pieces, squares=squares, move_logs=move_logs).values():
            if pin_value:
                return []
        orthogonal_pin = self.get_orthogonal_pin(pieces=pieces, squares=squares, move_logs=move_logs)
        if orthogonal_pin["vertical"]:
            allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color and square.coordonnees[0] == self.square.coordonnees[0]]
        elif orthogonal_pin["horizontal"]:
            allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color and square.coordonnees[1] == self.square.coordonnees[1]]
        else:
            allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color]
        
        if self.king.is_checked:
            if self.king.check_status["knight_check"] or self.king.check_status["pawn_check"]:
                return [square for square in allowed_squares if square in allowed_squares and square == self.king.check_status["attacking_pieces"][0].square]
            elif self.king.check_status["regular_check"]:
                attacking_piece = self.king.check_status["attacking_pieces"][0]
                if self.king.square.coordonnees[0] == attacking_piece.square.coordonnees[0]:
                    return [square for square in allowed_squares if square.coordonnees[0] == self.king.square.coordonnees[0] and ((attacking_piece.square.coordonnees[1] <= square.coordonnees[1] < self.king.square.coordonnees[1]) or (attacking_piece.square.coordonnees[1] > square.coordonnees[1] > self.king.square.coordonnees[1]))]
                elif self.king.square.coordonnees[1] == attacking_piece.square.coordonnees[1]:
                    return [square for square in allowed_squares if square.coordonnees[1] == self.king.square.coordonnees[1] and ((attacking_piece.square.coordonnees[0] <= square.coordonnees[0] < self.king.square.coordonnees[0]) or (attacking_piece.square.coordonnees[0] > square.coordonnees[0] > self.king.square.coordonnees[0]))]
                elif abs(attacking_piece.square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(attacking_piece.square.coordonnees[1] - self.king.square.coordonnees[1]): # Echec diagonal
                    return [square for square in allowed_squares if abs(square.coordonnees[0] - attacking_piece.square.coordonnees[0]) == abs(square.coordonnees[1] - attacking_piece.square.coordonnees[1]) and abs(square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(square.coordonnees[1] - self.king.square.coordonnees[1]) and (self.king.square.coordonnees[0] < square.coordonnees[0] <= attacking_piece.square.coordonnees[0] or self.king.square.coordonnees[0] > square.coordonnees[0] >= attacking_piece.square.coordonnees[0])]
            elif self.king.check_status["double_check"]:
                return []
        else:
            return allowed_squares

class Cavalier(Piece):
    def __init__(self, canvas, color, square, king):
        super().__init__(canvas, color, square, f"./assets/medias/pieces/{color.lower()}Knight.png", "Knight")
        self.king = king

    def get_attacked_squares(self, squares, move_logs):
        return [square for square in squares if square.coordonnees in [[self.square.coordonnees[0] - 1, self.square.coordonnees[1] - 2], [self.square.coordonnees[0] + 1, self.square.coordonnees[1] - 2], [self.square.coordonnees[0] + 2, self.square.coordonnees[1] - 1], [self.square.coordonnees[0] + 2, self.square.coordonnees[1] + 1], [self.square.coordonnees[0] + 1, self.square.coordonnees[1] + 2], [self.square.coordonnees[0] - 1, self.square.coordonnees[1] + 2], [self.square.coordonnees[0] - 2, self.square.coordonnees[1] + 1], [self.square.coordonnees[0] - 2, self.square.coordonnees[1] - 1]]]
    
    def get_allowed_squares(self, squares, pieces, move_logs):
        for pin_value in {**self.get_diagonal_pin(pieces=pieces, squares=squares, move_logs=move_logs), **self.get_orthogonal_pin(pieces=pieces, squares=squares, move_logs=move_logs)}.values():
            if pin_value:
                return []
            
        allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color]
        if self.king.is_checked:
            if self.king.check_status["knight_check"] or self.king.check_status["pawn_check"]:
                return [square for square in allowed_squares if square in allowed_squares and square == self.king.check_status["attacking_pieces"][0].square]
            elif self.king.check_status["regular_check"]:
                attacking_piece = self.king.check_status["attacking_pieces"][0]
                if self.king.square.coordonnees[0] == attacking_piece.square.coordonnees[0]:
                    return [square for square in allowed_squares if square.coordonnees[0] == self.king.square.coordonnees[0] and ((attacking_piece.square.coordonnees[1] <= square.coordonnees[1] < self.king.square.coordonnees[1]) or (attacking_piece.square.coordonnees[1] > square.coordonnees[1] > self.king.square.coordonnees[1]))]
                elif self.king.square.coordonnees[1] == attacking_piece.square.coordonnees[1]:
                    return [square for square in allowed_squares if square.coordonnees[1] == self.king.square.coordonnees[1] and ((attacking_piece.square.coordonnees[0] <= square.coordonnees[0] < self.king.square.coordonnees[0]) or (attacking_piece.square.coordonnees[0] > square.coordonnees[0] > self.king.square.coordonnees[0]))]
                elif abs(attacking_piece.square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(attacking_piece.square.coordonnees[1] - self.king.square.coordonnees[1]): # Echec diagonal
                    return [square for square in allowed_squares if abs(square.coordonnees[0] - attacking_piece.square.coordonnees[0]) == abs(square.coordonnees[1] - attacking_piece.square.coordonnees[1]) and abs(square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(square.coordonnees[1] - self.king.square.coordonnees[1]) and (self.king.square.coordonnees[0] < square.coordonnees[0] <= attacking_piece.square.coordonnees[0] or self.king.square.coordonnees[0] > square.coordonnees[0] >= attacking_piece.square.coordonnees[0])]
            elif self.king.check_status["double_check"]:
                return []
        else:
            return allowed_squares

class Fou(Piece):
    def __init__(self, canvas, color, square, king):
        super().__init__(canvas, color, square, f"./assets/medias/pieces/{color.lower()}Bishop.png", "Bishop")
        self.king = king

    def get_attacked_squares(self, squares, move_logs):
        accessible_squares = []

        right_top_squares = [square for square in squares if square.index % 7 == self.square.index % 7 and square.index < self.square.index and square.index != self.square.index]
        if not self.square.coordonnees[0] == 8:
            for square in reversed(right_top_squares):
                accessible_squares.append(square)
                if square.coordonnees[0] == 8 or square.contain_piece:
                    break
        
        left_top_squares = [square for square in squares if square.index % 9 == self.square.index % 9 and square.index < self.square.index and square.index != self.square.index]
        if not self.square.coordonnees[0] == 1:
            for square in reversed(left_top_squares):
                accessible_squares.append(square)
                if square.coordonnees[0] == 1 or square.contain_piece:
                    break
        
        left_bottom_squares = [square for square in squares if square.index % 7 == self.square.index % 7 and square.index > self.square.index and square.index != self.square.index]
        if not self.square.coordonnees[0] == 1:
            for square in left_bottom_squares:
                accessible_squares.append(square)
                if square.coordonnees[0] == 1 or square.contain_piece:
                    break
        
        right_bottom_squares = [square for square in squares if square.index % 9 == self.square.index % 9 and square.index > self.square.index and square.index != self.square.index]
        if not self.square.coordonnees[0] == 8:
            for square in right_bottom_squares:
                accessible_squares.append(square)
                if square.coordonnees[0] == 8 or square.contain_piece:
                    break
        return accessible_squares
    
    def get_allowed_squares(self, squares, pieces, move_logs):
        allowed_squares = []
        
        for pin_value in self.get_orthogonal_pin(pieces=pieces, squares=squares, move_logs=move_logs).values():
            if pin_value:
                return []
        
        diagonal_pin = self.get_diagonal_pin(pieces=pieces, squares=squares, move_logs=move_logs)
        if diagonal_pin["top_to_bottom"]:
            allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color and not (square.index % 7 == self.square.index % 7 and square.index < self.square.index and square.index != self.square.index) and not (square.index % 7 == self.square.index % 7 and square.index > self.square.index and square.index != self.square.index)]
        elif diagonal_pin["bottom_to_top"]:
            allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color and not (square.index % 9 == self.square.index % 9 and square.index < self.square.index and square.index != self.square.index) and not (square.index % 9 == self.square.index % 9 and square.index > self.square.index and square.index != self.square.index)]
        else:
            allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color]
        
        if self.king.is_checked:
            if self.king.check_status["knight_check"] or self.king.check_status["pawn_check"]:
                return [square for square in allowed_squares if square in allowed_squares and square == self.king.check_status["attacking_pieces"][0].square]
            elif self.king.check_status["regular_check"]:
                attacking_piece = self.king.check_status["attacking_pieces"][0]
                if self.king.square.coordonnees[0] == attacking_piece.square.coordonnees[0]:
                    return [square for square in allowed_squares if square.coordonnees[0] == self.king.square.coordonnees[0] and ((attacking_piece.square.coordonnees[1] <= square.coordonnees[1] < self.king.square.coordonnees[1]) or (attacking_piece.square.coordonnees[1] > square.coordonnees[1] > self.king.square.coordonnees[1]))]
                elif self.king.square.coordonnees[1] == attacking_piece.square.coordonnees[1]:
                    return [square for square in allowed_squares if square.coordonnees[1] == self.king.square.coordonnees[1] and ((attacking_piece.square.coordonnees[0] <= square.coordonnees[0] < self.king.square.coordonnees[0]) or (attacking_piece.square.coordonnees[0] > square.coordonnees[0] > self.king.square.coordonnees[0]))]
                elif abs(attacking_piece.square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(attacking_piece.square.coordonnees[1] - self.king.square.coordonnees[1]): # Echec diagonal
                    return [square for square in allowed_squares if abs(square.coordonnees[0] - attacking_piece.square.coordonnees[0]) == abs(square.coordonnees[1] - attacking_piece.square.coordonnees[1]) and abs(square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(square.coordonnees[1] - self.king.square.coordonnees[1]) and (self.king.square.coordonnees[0] < square.coordonnees[0] <= attacking_piece.square.coordonnees[0] or self.king.square.coordonnees[0] > square.coordonnees[0] >= attacking_piece.square.coordonnees[0])]
            elif self.king.check_status["double_check"]:
                return []
        else:
            return allowed_squares

class Reine(Piece):
    def __init__(self, canvas, color, square, king):
        super().__init__(canvas, color, square, f"./assets/medias/pieces/{color.lower()}Queen.png", "Queen")
        self.king = king

    def get_attacked_squares(self, squares, move_logs):
        accessible_squares = []
        # Fou
        right_top_squares = [square for square in squares if square.index % 7 == self.square.index % 7 and square.index < self.square.index and square.index != self.square.index]
        if not self.square.coordonnees[0] == 8:
            for square in reversed(right_top_squares):
                accessible_squares.append(square)
                if square.coordonnees[0] == 8 or square.contain_piece:
                    break
        
        left_top_squares = [square for square in squares if square.index % 9 == self.square.index % 9 and square.index < self.square.index and square.index != self.square.index]
        if not self.square.coordonnees[0] == 1:
            for square in reversed(left_top_squares):
                accessible_squares.append(square)
                if square.coordonnees[0] == 1 or square.contain_piece:
                    break
        
        right_bottom_squares = [square for square in squares if square.index % 7 == self.square.index % 7 and square.index > self.square.index and square.index != self.square.index]
        if not self.square.coordonnees[0] == 1:
            for square in right_bottom_squares:
                accessible_squares.append(square)
                if square.coordonnees[0] == 1 or square.contain_piece:
                    break
        
        left_bottom_squares = [square for square in squares if square.index % 9 == self.square.index % 9 and square.index > self.square.index and square.index != self.square.index]
        if not self.square.coordonnees[0] == 8:
            for square in left_bottom_squares:
                accessible_squares.append(square)
                if square.coordonnees[0] == 8 or square.contain_piece:
                    break
        # Tour
        left_squares = [square for square in squares if square.coordonnees[1] == self.square.coordonnees[1] and square.index < self.square.index]
        for square in reversed(left_squares):
            accessible_squares.append(square)
            if square.contain_piece:
                break
        right_squares = [square for square in squares if square.coordonnees[1] == self.square.coordonnees[1] and square.index > self.square.index]
        for square in right_squares:
            accessible_squares.append(square)
            if square.contain_piece:
                break
        top_squares = [square for square in squares if square.coordonnees[0] == self.square.coordonnees[0] and square.index < self.square.index]
        i = 0
        for square in reversed(top_squares):
            i += 1
            accessible_squares.append(square)
            if square.contain_piece:
                break
        bottom_squares = [square for square in squares if square.coordonnees[0] == self.square.coordonnees[0] and square.index > self.square.index]
        for square in bottom_squares:
            accessible_squares.append(square)
            if square.contain_piece:
                break
        return accessible_squares
    
    def get_allowed_squares(self, squares, pieces, move_logs):
        allowed_squares = []
        orthogonal_pin = self.get_orthogonal_pin(pieces=pieces, squares=squares, move_logs=move_logs)
        if orthogonal_pin["vertical"]:
            allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color and square.coordonnees[0] == self.square.coordonnees[0]]
        elif orthogonal_pin["horizontal"]:
            allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color and square.coordonnees[1] == self.square.coordonnees[1]]
        else:
            diagonal_pin = self.get_diagonal_pin(pieces=pieces, squares=squares, move_logs=move_logs)
            if diagonal_pin["top_to_bottom"]:
                allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color and not (square.index % 7 == self.square.index % 7 and square.index < self.square.index and square.index != self.square.index) and not (square.index % 7 == self.square.index % 7 and square.index > self.square.index and square.index != self.square.index) and not (self.square.coordonnees[0] == square.coordonnees[0] or self.square.coordonnees[1] == square.coordonnees[1])]
            elif diagonal_pin["bottom_to_top"]:
                allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color and not (square.index % 9 == self.square.index % 9 and square.index < self.square.index and square.index != self.square.index) and not (square.index % 9 == self.square.index % 9 and square.index > self.square.index and square.index != self.square.index) and not (self.square.coordonnees[0] == square.coordonnees[0] or self.square.coordonnees[1] == square.coordonnees[1])]
            else:
                allowed_squares = [square for square in self.get_attacked_squares(squares, move_logs) if not square.contain_piece == self.color]
        
        if self.king.is_checked:
            if self.king.check_status["knight_check"] or self.king.check_status["pawn_check"]:
                return [square for square in allowed_squares if square in allowed_squares and square == self.king.check_status["attacking_pieces"][0].square]
            elif self.king.check_status["regular_check"]:
                attacking_piece = self.king.check_status["attacking_pieces"][0]
                if self.king.square.coordonnees[0] == attacking_piece.square.coordonnees[0]:
                    return [square for square in allowed_squares if square.coordonnees[0] == self.king.square.coordonnees[0] and ((attacking_piece.square.coordonnees[1] <= square.coordonnees[1] < self.king.square.coordonnees[1]) or (attacking_piece.square.coordonnees[1] > square.coordonnees[1] > self.king.square.coordonnees[1]))]
                elif self.king.square.coordonnees[1] == attacking_piece.square.coordonnees[1]:
                    return [square for square in allowed_squares if square.coordonnees[1] == self.king.square.coordonnees[1] and ((attacking_piece.square.coordonnees[0] <= square.coordonnees[0] < self.king.square.coordonnees[0]) or (attacking_piece.square.coordonnees[0] > square.coordonnees[0] > self.king.square.coordonnees[0]))]
                elif abs(attacking_piece.square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(attacking_piece.square.coordonnees[1] - self.king.square.coordonnees[1]): # Echec diagonal
                    return [square for square in allowed_squares if abs(square.coordonnees[0] - attacking_piece.square.coordonnees[0]) == abs(square.coordonnees[1] - attacking_piece.square.coordonnees[1]) and abs(square.coordonnees[0] - self.king.square.coordonnees[0]) == abs(square.coordonnees[1] - self.king.square.coordonnees[1]) and (self.king.square.coordonnees[0] < square.coordonnees[0] <= attacking_piece.square.coordonnees[0] or self.king.square.coordonnees[0] > square.coordonnees[0] >= attacking_piece.square.coordonnees[0])]
            elif self.king.check_status["double_check"]:
                return []
        else:
            return allowed_squares