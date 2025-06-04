
from hex import Hex
from piece import *

TESTING = True

"""
Represents the start state as a list of pieces on the board at the start
each piece is represented as (q, r, s, type, color)
"""
START_STATE = {
    # white pieces
    (-4, -1): ("P", 0),
    (-3, -1): ("P", 0),
    (-2, -1): ("P", 0),
    (-1, -1): ("P", 0),
    (0, -1): ("P", 0),
    (1, -2): ("P", 0),
    (2, -3): ("P", 0),
    (3, -4): ("P", 0),
    (4, -5): ("P", 0),
    (1, -5): ("K", 0),
    (-1, -4): ("Q", 0),
    (0, -5): ("B", 0),
    (0, -4): ("B", 0),
    (0, -3): ("B", 0),
    (3, -5): ("R", 0),
    (-3, -2): ("R", 0),
    (-2, -3): ("N", 0),
    (2, -5): ("N", 0),
    
    # black pieces
    (0, 1): ("P", 1),
    (1, 1): ("P", 1),
    (2, 1): ("P", 1),
    (3, 1): ("P", 1),
    (4, 1): ("P", 1),
    (-1, 2): ("P", 1),
    (-2, 3): ("P", 1),
    (-3, 4): ("P", 1),
    (-4, 5): ("P", 1),
    (1, 4): ("K", 1),
    (-1, 5): ("Q", 1),
    (0, 5): ("B", 1),
    (0, 4): ("B", 1),
    (0, 3): ("B", 1),
    (-3, 5): ("R", 1),
    (3, 2): ("R", 1),
    (2, 3): ("N", 1),
    (-2, 5): ("N", 1),
}

"""
Add HEX_DIRECTIONS["{direction}"] to a hex to get the coordinates of the 
hex that should be in that direction of it
"""
HEX_DIRECTIONS = {
    "North": Hex(0, 1),
    "South": Hex(0, -1),
    "Northwest": Hex(-1, 1),
    "Southeast": Hex(1, -1),
    "Northeast": Hex(1, 0),
    "Southwest": Hex(-1, 0)
}

"""
TODO: implement checking behavior
"""

class Board:
    """
    A class with a set of hexes for the board
    Default radius of 5, gamestate of the standard start state 
    Will contain a set of methods for finding adjacent hexes and such
    """
    def __init__(self, radius:int=5, initial_state=START_STATE):
        hexes = []
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                s = -q + -r
                if -radius <= s <= radius:
                    # piece is none by default
                    piece = None
                    # get if there is a piece on the hex
                    key = (q, r)
                    if key in initial_state:
                        piece_type, color = initial_state[key]
                        piece = make_piece(piece_type, color)
                    hexes.append(Hex(q, r, s, piece))
        self.hexes = hexes
        self.selected_hex = None
        self.turn = 0

    def get_hex(self, q:int, r:int):
        """
        Returns the hex at the given q, r coordinate, 
        or None if it is out of bounds.
        """
        for hex in self.hexes:
            if hex.q == q and hex.r == r:
                return hex
        return None

    def select_hex(self, q:int, r:int):
        self.selected_hex = self.get_hex(q, r)

    def next_turn(self):
        self.turn = 1 if self.turn == 0 else 0

    def get_legal_moves(self, q:int, r:int):
        """
        Given hex coordinates, give a list of hexes 
        that are legal moves for the piece at the hex
        """
        piece = self.get_hex(q, r).piece
        if not piece: # no moves for an empty hex
            return []
        # get moves based on the type of piece it is
        if type(piece) == Rook:
            return self.__get_moves_rook(q, r, piece.color)
        if type(piece) == Knight:
            return self.__get_moves_knight(q, r, piece.color)
        if type(piece) == Bishop:
            return self.__get_moves_bishop(q, r, piece.color)
        if type(piece) == Queen:
            return self.__get_moves_queen(q, r, piece.color)
        if type(piece) == King:
            return self.__get_moves_king(q, r, piece.color)
        if type(piece) == Pawn:
            return self.__get_moves_pawn(q, r, piece.color)
        
    def __get_moves_rook(self, q, r, color):
        out = []
        # movement along files
        directions = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
        # for each file
        for move in directions:
            # keep going until we hit the border or a piece
            dest:Hex = self.get_hex(q + move[0], r + move[1])
            while dest:
                if not dest.piece:
                    out.append(dest)
                else:
                    if dest.piece.color != color:
                        out.append(dest)
                    break
                dest = self.get_hex(dest.q + move[0], dest.r + move[1])
        return out

    def __get_moves_knight(self, q, r, color):
        out = []
        directions = [(2, 1), (3, -1), (3, -2), (2, -3), (1, -3), (-1, -2),
                      (-2, -1), (-3, 1), (-2, 3), (-3, 2), (-1, 3), (1, 2)]
        # just check the exact hexes we could move to
        for move in directions:
            dest:Hex = self.get_hex(q + move[0], r + move[1])
            if  dest: 
                if not dest.piece or dest.piece.color != color:
                    out.append(dest)
        return out

    def __get_moves_bishop(self, q, r, color):
        out = []
        directions = [(1, 1), (-1, 2), (-2, 1), (-1, -1), (1, -2), (2, -1)]
        # for each diagonal
        for move in directions:
            # keep going until we hit the border or a piece
            dest:Hex = self.get_hex(q + move[0], r + move[1])
            while dest:
                # if there is no piece there, add the hex
                if not dest.piece:
                    out.append(dest)
                # if there is a piece but its not ours, add the hex
                else:
                    if dest.piece.color != color:
                        out.append(dest)
                    # break cuz we hit a piece
                    break
                # go to next hex
                dest = self.get_hex(dest.q + move[0], dest.r + move[1])
        return out

    def __get_moves_queen(self, q, r, color):
        # just combine the rook and bishop
        out = []
        out.append(self.__get_moves_bishop(q, r, color))
        out.append(self.__get_moves_rook(q, r, color))
        return out

    def __get_moves_king(self, q, r, color):
        out = []
        directions = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1),
        (1, 1), (-1, 2), (-2, 1), (-1, -1), (1, -2), (2, -1)]
        # check each direction
        for move in directions:
            dest:Hex = self.get_hex(q + move[0], r + move[1])
            # if the destination is in bounds and no piece there, add it the hex
            # if there is an enemy piece, add it
            if  dest: 
                if not dest.piece and not self.is_under_threat(dest.piece.q, dest.piece.r):
                    out.append(dest)
                elif dest.piece and dest.piece.color != color:
                    out.append(dest)
        return out

    def __get_moves_pawn(self, q, r, color):
        "TODO: implement en passant is we i want to "
        white_start_hexes = [(-4, -1), (-3, -1), (-2, -1), (-1, -1), 
                             (0, -1), (1, -2), (2, -3), (3, -4), (4, -5)]
        black_start_hexes = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), 
                             (-1, 2), (-2, 3), (-3, 4), (-4, 5)]
        out = []
        # if white pawn
        if color == 0:
            # moving forward
            dest:Hex = self.get_hex(q, r + 1)
            if dest and not dest.piece:
                out.append(dest)
                if (q, r) in white_start_hexes:
                    dest = self.get_hex(q, r + 2)
                    if not dest.piece:
                        out.append(dest)
            
            # check for taking 
            dest = self.get_hex(q + 1, r)
            if  dest and dest.piece and dest.piece.color != color: 
                out.append(dest)
            dest = self.get_hex(q - 1, r + 1)
            if  dest and dest.piece and dest.piece.color != color: 
                out.append(dest)

            
        # if black pawn
        if color == 1:
            # moving forward
            dest:Hex = self.get_hex(q, r - 1)
            if dest and not dest.piece:
                out.append(dest)
                if (q, r) in black_start_hexes:
                    dest = self.get_hex(q, r - 2)
                    if not dest.piece:
                        out.append(dest)
            
            # check for taking
            # check for taking 
            dest = self.get_hex(q - 1, r)
            if  dest and dest.piece and dest.piece.color != color: 
                out.append(dest)
            dest = self.get_hex(q + 1, r - 1)
            if  dest and dest.piece and dest.piece.color != color: 
                out.append(dest)

        return out

    def is_under_threat(self, q, r, color):
        check = []
        check.append(self.__get_moves_knight(q, r, color))
        check.append(self.__get_moves_queen(q, r, color))
        check.append(self.__get_moves_pawn(q, r, color))
        for tile in check:
            if tile.piece.color != color:
                return True
        return False
    
    def move_piece(self, fro:tuple, to:tuple):
        """
        Move a piece from hex_start to hex_end. returns true if valid and false otherwise
        In practice this should always return true
        """
        hex_start = self.get_hex(fro[0], fro[1])
        hex_end = self.get_hex(to[0], to[1])
        # make sure we never try to move a piece illegally (should be checked by front end)
        if hex_end not in self.get_legal_moves(hex_start.q,hex_start.r):
            return False
        hex_end.set_piece(hex_start.piece)
        hex_start.set_piece(None)
        return True

    def calculate_points(self, tile:Hex):
        return ""


    def as_json(self):
        """
        Output a JSON representation of the board state.
        """
        state = []
        for tile in self.hexes:
            state.append({
                "q": tile.q,
                "r": tile.r,
                "piece": (tile.piece.piece_type, tile.piece.color) if tile.piece else None,
                "points": self.calculate_points(tile),
                "color": tile.color
            })
        return state