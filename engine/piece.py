VALID_TYPES = [
    "Rook", "R", "r",
    "Knight", "N", "n",
    "Bishop", "B", "b",
    "Queen", "Q", "q",
    "King", "K", "k",
    "Pawn", "P", "p"
]

class Piece:
    """
    Piece class to represent what piece type and color a piece is.
    Given color is 0 for white and 1 for black
    """
    def __init__(self, piece_type:str, color:int):
        assert piece_type in VALID_TYPES
        self.piece_type = covert_piece_to_string(piece_type)
        self.color = color
        self.color_string = "White" if color == 0 else "Black"
        # self.image_ref = "game/assets/"
        self.image_ref = "w_" if color == 0 else "b_"

    def __repr__(self):
        return f"Piece: {self.color_string} {self.piece_type}"

        
class Rook(Piece):
    def __init__(self, color:int):
        super().__init__("R", color)
        self.image_ref += "rook.png"

class Pawn(Piece):
    def __init__(self, color:int):
        super().__init__("P", color)
        self.image_ref += "pawn.png"

class Knight(Piece):
    def __init__(self, color:int):
        super().__init__("N", color)
        self.image_ref += "knight.png"

class Queen(Piece):
    def __init__(self, color:int):
        super().__init__("Q", color)
        self.image_ref += "queen.png"

class King(Piece):
    def __init__(self, color:int):
        super().__init__("K", color)
        self.image_ref += "king.png"

class Bishop(Piece):
    def __init__(self, color:int):
        super().__init__("B", color)
        self.image_ref += "bishop.png"

def covert_piece_to_string(string:str):
    if string in ["Rook", "R", "r"]:
        return "Rook"
    if string in ["Knight", "N", "n"]:
        return "Knight"
    if string in ["Bishop", "B", "b"]:
        return "Bishop"
    if string in ["Queen", "Q", "q"]:
        return "Queen"
    if string in ["King", "K", "k"]:
        return "King"
    if string in ["Pawn", "P", "p"]:
        return "Pawn"
    
def make_piece(piece_type, color):
    if piece_type in ["Rook", "R", "r"]:
        return Rook(color)
    if piece_type in ["Knight", "N", "n"]:
        return Knight(color)
    if piece_type in ["Bishop", "B", "b"]:
        return Bishop(color)
    if piece_type in ["Queen", "Q", "q"]:
        return Queen(color)
    if piece_type in ["King", "K", "k"]:
        return King(color)
    if piece_type in ["Pawn", "P", "p"]:
        return Pawn(color)