import math

from .hex import Hex
from .piece import make_piece, Rook, Knight, Bishop, Queen, King, Pawn

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


class Board:
    """
    A class with a set of hexes for the board
    Default radius of 5, gamestate of the standard start state
    Will contain a set of methods for finding adjacent hexes and such
    """

    def __init__(self, radius: int = 5, initial_state=None, size=30, center=(400, 400)):
        self.size = None
        if initial_state is None:
            initial_state = START_STATE

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
                    color = (r - q) % 3
                    hexes.append(Hex(q, r, s, piece, color))
        self.hexes = hexes
        self.board_center = center
        self.set_size(size)
        self.selected_hex = None
        self.turn = 0

    def on_click(self, q: int, r: int):
        # get the hex that was clicked on
        tile = self.get_hex(q, r)

        # if we have a hex selected, check if we can move the piece
        #  to the clicked on tile
        if self.selected_hex:
            # if we can move the piece to this hex, do it and swap turns
            if tile in self.get_legal_moves(self.selected_hex.q, self.selected_hex.r):
                tile = (self.selected_hex.q, self.selected_hex.r)
                self.__unselect_piece()
                self.move_piece(tile, (q, r))
                self.__next_turn()
                return True # return true since we changed turns
            if not tile.piece:
                self.__unselect_piece()
            # if we clicked on another owned piece, select it instead
            elif tile.piece.color == self.turn:
                self.__unselect_piece()
                self.__select_piece(q, r)
            # if we clicked on a hex that we cant move to and we cant select,
            # just unselect what we have selected
            else:
                self.__unselect_piece()

        # if we don't have a selected hex, and the hex we clicked on is selectable, select it
        elif tile.piece and tile.piece.color == self.turn:
            self.__select_piece(q, r)
        return False # return false since we did not change turns

    def __unselect_piece(self):
        self.selected_hex.selected = False
        for tile in self.get_legal_moves(self.selected_hex.q, self.selected_hex.r):
            tile.highlighted = False
        self.selected_hex = None

    def __select_piece(self, q, r):
        self.selected_hex = self.get_hex(q, r)
        for tile in self.get_legal_moves(self.selected_hex.q, self.selected_hex.r):
            tile.highlighted = True
        self.selected_hex.selected = True

    def get_hex(self, q: int, r: int) -> Hex | None:
        """
        Returns the hex at the given q, r coordinate,
        or None if it is out of bounds.
        """
        for hex in self.hexes:
            if hex.q == q and hex.r == r:
                return hex
        return None

    def __next_turn(self):
        self.turn = 1 if self.turn == 0 else 0

    def get_legal_moves(self, q: int, r: int):
        """
        Given hex coordinates, give a list of hexes
        that are legal moves for the piece at the hex
        """
        piece = self.get_hex(q, r).piece
        if not piece:  # no moves for an empty hex
            return []
        match piece:
            case Rook():
                return self.__get_moves_rook(q, r, piece.color)
            case Knight():
                return self.__get_moves_knight(q, r, piece.color)
            case Bishop():
                return self.__get_moves_bishop(q, r, piece.color)
            case Queen():
                return self.__get_moves_queen(q, r, piece.color)
            case King():
                return self.__get_moves_king(q, r, piece.color)
            case Pawn():
                return self.__get_moves_pawn(q, r, piece.color)
            case _:
                raise NotImplementedError(
                    f"{type(piece)}: is not an implemented Piece!"
                )

    def __get_moves_rook(self, q, r, color):
        out = []
        # movement along files
        directions = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
        # for each file
        for move in directions:
            # keep going until we hit the border or a piece
            dest: Hex = self.get_hex(q + move[0], r + move[1])
            while dest:
                if not dest.piece:
                    out.append(dest)
                else:
                    if dest.piece.color != color:
                        out.append(dest)
                    break
                dest = self.get_hex(dest.q + move[0], dest.r + move[1])
        return out

    def __get_moves_knight(self, q, r, color) -> list[tuple[int, int]]:
        out = []
        directions = [
            (2, 1),
            (3, -1),
            (3, -2),
            (2, -3),
            (1, -3),
            (-1, -2),
            (-2, -1),
            (-3, 1),
            (-2, 3),
            (-3, 2),
            (-1, 3),
            (1, 2),
        ]
        # just check the exact hexes we could move to
        for move in directions:
            dest: Hex = self.get_hex(q + move[0], r + move[1])
            if dest:
                if not dest.piece or dest.piece.color != color:
                    out.append(dest)
        return out

    def __get_moves_bishop(self, q, r, color):
        out = []
        directions = [(1, 1), (-1, 2), (-2, 1), (-1, -1), (1, -2), (2, -1)]
        # for each diagonal
        for move in directions:
            # keep going until we hit the border or a piece
            dest: Hex = self.get_hex(q + move[0], r + move[1])
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
        out += self.__get_moves_bishop(q, r, color)
        out += self.__get_moves_rook(q, r, color)
        return out

    def __get_moves_king(self, q, r, color):
        out = []
        directions = [
            (0, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, 0),
            (-1, 1),
            (1, 1),
            (-1, 2),
            (-2, 1),
            (-1, -1),
            (1, -2),
            (2, -1),
        ]
        # check each direction
        for move in directions:
            dest: Hex = self.get_hex(q + move[0], r + move[1])
            # if the destination is in bounds and no piece there, add it the hex
            # if there is an enemy piece, add it
            if dest:
                if self.__is_under_threat(dest.q, dest.r, color):
                    continue
                if not dest.piece:
                    out.append(dest)
                    continue
                if dest.piece.color != color:
                    out.append(dest)
        return out

    def __get_moves_pawn(self, q, r, color):
        """TODO: implement en passant is we i want to"""
        white_start_hexes = [
            (-4, -1),
            (-3, -1),
            (-2, -1),
            (-1, -1),
            (0, -1),
            (1, -2),
            (2, -3),
            (3, -4),
            (4, -5),
        ]
        black_start_hexes = [
            (0, 1),
            (1, 1),
            (2, 1),
            (3, 1),
            (4, 1),
            (-1, 2),
            (-2, 3),
            (-3, 4),
            (-4, 5),
        ]
        out = []
        # if white pawn
        if color == 0:
            # moving forward
            dest: Hex = self.get_hex(q, r + 1)
            if dest and not dest.piece:
                out.append(dest)
                if (q, r) in white_start_hexes:
                    dest = self.get_hex(q, r + 2)
                    if not dest.piece:
                        out.append(dest)

            # check for taking
            dest = self.get_hex(q + 1, r)
            if dest and dest.piece and dest.piece.color != color:
                out.append(dest)
            dest = self.get_hex(q - 1, r + 1)
            if dest and dest.piece and dest.piece.color != color:
                out.append(dest)

        # if black pawn
        if color == 1:
            # moving forward
            dest: Hex = self.get_hex(q, r - 1)
            if dest and not dest.piece:
                out.append(dest)
                if (q, r) in black_start_hexes:
                    dest = self.get_hex(q, r - 2)
                    if not dest.piece:
                        out.append(dest)

            # check for taking
            # check for taking
            dest = self.get_hex(q - 1, r)
            if dest and dest.piece and dest.piece.color != color:
                out.append(dest)
            dest = self.get_hex(q + 1, r - 1)
            if dest and dest.piece and dest.piece.color != color:
                out.append(dest)

        return out

    def __is_under_threat(self, q, r, color):
        # check for knights
        for tile in self.__get_moves_knight(q, r, color):
            if tile.piece and tile.piece.color != color and type(tile.piece) is Knight:
                return True
        # check for queens/rooks
        for tile in self.__get_moves_rook(q, r, color):
            if (
                tile.piece
                and tile.piece.color != color
                and (type(tile.piece) is Queen or type(tile.piece) is Rook)
            ):
                return True
        # check for queens/bishops
        for tile in self.__get_moves_bishop(q, r, color):
            if (
                tile.piece
                and tile.piece.color != color
                and (type(tile.piece) is Queen or type(tile.piece) is Bishop)
            ):
                return True
        # check for pawns
        if color == 1:
            pawn_checks = [self.get_hex(q - 1, r), self.get_hex(q + 1, r - 1)]
        else:
            pawn_checks = [self.get_hex(q - 1, r + 1), self.get_hex(q + 1, r)]
        for tile in pawn_checks:
            if (
                tile
                and tile.piece
                and tile.piece.color != color
                and type(tile.piece) is Pawn
            ):
                return True

        return False

    def move_piece(self, fro: tuple, to: tuple):
        """
        Move a piece from hex_start to hex_end. returns true if valid and false otherwise
        In practice this should always return true
        """
        hex_start = self.get_hex(fro[0], fro[1])
        hex_end = self.get_hex(to[0], to[1])
        # make sure we never try to move a piece illegally (should be checked by front end)
        if hex_end not in self.get_legal_moves(hex_start.q, hex_start.r):
            return False
        hex_end.set_piece(hex_start.piece)
        hex_start.set_piece(None)
        return True

    def set_size(self, new_size: int):
        self.size = new_size
        for tile in self.hexes:
            self.__calculate_points(tile)

    def __calculate_points(self, tile: Hex):
        sqrt3 = math.sqrt(3)
        # First calculate the center of a hex
        center_x = self.board_center[0] + 1.5 * self.size * tile.q
        center_y = self.board_center[1] - sqrt3 * self.size * (tile.r + tile.q / 2)
        # calculate the points, self.size is the distance from the center
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            points.append(
                f"{center_x + self.size * math.cos(angle)},\
                          {center_y + self.size * math.sin(angle)}"
            )
        tile.center_x = center_x
        tile.center_y = center_y
        tile.points = " ".join(points)
        
        # repeat with flipped board
        # calculate center of hex
        center_x_flip = self.board_center[0] - 1.5 * self.size * tile.q
        center_y_flip = self.board_center[1] + sqrt3 * self.size * (tile.r + tile.q / 2)
        # calculate points, with self.size as distance from center
        points_flipped = []
        for i in range(6):
            angle = i * math.pi / 3
            points_flipped.append(
                f"{center_x_flip + self.size * math.cos(angle)},\
                          {center_y_flip + self.size * math.sin(angle)}"
            )
        tile.center_x_flip = center_x_flip
        tile.center_y_flip = center_y_flip
        tile.points_flipped = " ".join(points_flipped)

    def as_json(self, flipped):
        """
        Output a JSON representation of the board state.
        """
        state = []
        for tile in self.hexes:
            piece = tile.piece
            center_x = tile.center_x_flip if flipped else tile.center_x
            center_y = tile.center_y_flip if flipped else tile.center_y
            x = center_x- self.size / 2
            y = center_y - self.size / 2
            points = tile.points_flipped if flipped else tile.points

            state.append(
                {
                    "q": tile.q,
                    "r": tile.r,
                    "center_x": center_x,
                    "center_y": center_y,
                    "piece_x": x,
                    "piece_y": y,
                    "piece": (piece.piece_type, piece.color) if piece else None,
                    "piece_path": piece.image_ref if piece else None,
                    "points": points,
                    "color": tile.color,
                    "selected": tile.selected,
                    "highlighted": tile.highlighted,
                }
            )
        return state
