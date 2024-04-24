class Square():
    def __init__(self, index, coordonnees):
        self.contain_piece = False
        self.index = index
        self.coordonnees = coordonnees

    def __str__(self) -> str:
        return (f"Index : {self.index} - Coordonnées : {self.coordonnees}")
    
    def get_attacking_pieces(self, squares, pieces, move_logs):
        attacking_pieces = []
        for piece in pieces:
            if not piece.has_been_taken and self in piece.get_attacked_squares(squares, move_logs):
                attacking_pieces.append(piece)
        return attacking_pieces