from .Piece import Piece
from .Color import Color


class Pawn(Piece):
    def __init__(self, color: Color, x: int, y: int):
        super(Pawn, self).__init__(color, x, y)
        self._captures:list[list[int]] = []

    @property
    def movement(self) -> list[list[int]]:
        """Returns the lists of potential moves in any given position"""
        self._list_moves.clear()
        if self.in_row_boundary:
            return self._list_moves.copy()
        if self.color == Color.White:
            self._list_moves.append([self.y + 1, self.x])
            if not self.has_moved:
                self._list_moves.append([self.y + 2, self.x])
        else:
            self._list_moves.append([self.y - 1, self.x])
            if not self.has_moved:
                self._list_moves.append([self.y - 2, self.x])
        return self._list_moves.copy()

    @property
    def captures(self) -> list[list[int]]:
        """Returns the lists of potential captures in any given position"""
        self._captures.clear()
        if self.in_row_boundary:
            return self._captures.copy()
        if self.color == Color.White:
            for square in range(self.x - 1, self.x + 2, 2):
                if 0 <= square <= 7:
                    self._captures.append([self.y + 1, square])
        else:
            for square in range(self.x - 1, self.x + 2, 2):
                if 0 <= square <= 7:
                    self._captures.append([self.y - 1, square])
        return self._captures.copy()

    def legal_moves(self, situation: list[list]) -> list[list[int]]:
        """Restricts the list of movements to only legal moves.
        Receives the situation of the board, a matrix with all the instances in the game right now.
        Returns the legal moves"""
        psb_moves = self.movement
        lgl_moves = []
        psb_captures = self.captures
        lgl_captures = []
        try:
            # checking if there is something in front of the pawn
            for move in psb_moves:
                if situation[move[0]][move[1]] is None:
                    lgl_moves.append(move)
            # checking if there is something to be capture
            for move in psb_captures:
                if situation[move[0]][move[1]] is not None and situation[move[0]][move[1]].color != self.color:
                    lgl_captures.append(move)
        except IndexError as e:
            print("Ops!", e, "Occurred")
        finally:
            return lgl_moves + lgl_captures

    def move(self, target: list[int], situation: list[list]) -> list[list]:
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        psb_moves = self.legal_moves(situation)
        # checking if the move is possible
        if target not in psb_moves:
            return situation
        # updating attributes
        self._has_moved = True
        return self.update_situation(target, situation)

    @property
    def promotion(self) -> bool:
        """Checks if it is a case for promotion"""
        if self.y == 7 or self.y == 0:
            return True
        return False
