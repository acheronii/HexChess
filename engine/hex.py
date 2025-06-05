from .piece import Piece

COLORS = ["maroon", "navajowhite", "gray"]


class Hex:
    """
    Class for representing a single hex for my board
    """

    def __init__(
        self, q: int, r: int, s: int = None, piece: Piece = None, color: int = 0
    ):
        if not s:
            s = -q + -r
        assert q + r + s == 0
        self.q = q
        self.r = r
        self.s = s
        self.piece = piece
        self.color = COLORS[color]
        self.selected = False
        self.highlighted = False
        self.center_x = None
        self.center_y = None
        self.points = []

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

    def __repr__(self):
        return f"Hex: {self.q=}, {self.r=}, {self.piece=}"

    def set_piece(self, piece: Piece):
        self.piece = piece
