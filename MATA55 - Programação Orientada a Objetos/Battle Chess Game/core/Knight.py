from .Piece import Piece
from .Color import Color


class Knight(Piece):
    def __init__(self, color: Color, x: int, y: int):
        super(Knight, self).__init__(color, x, y)

    @property
    def movement(self) -> list[list[int]]:
        """Returns the lists of potential moves in any given position"""
        self._list_moves.clear()
        directions = [(-2, -1), (2, -1), (-2, 1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]
        # checking each direction
        for side in directions:
            x, y = self.x, self.y
            x += side[0]
            y += side[1]
            in_board_boundary = 0 <= x < 8 and 0 <= y < 8
            if in_board_boundary:
                self._list_moves.append([y, x])
        return self._list_moves.copy()

    def legal_moves(self, situation: list[list]) -> list[list[int]]:
        """Restricts the list of movements to only legal moves.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the legal moves"""
        psb_moves = self.movement
        try:
            for move in psb_moves:
                if situation[move[0]][move[1]] is not None and (
                        situation[move[0]][move[1]].color == self.color):
                    psb_moves.remove(move)
        except IndexError as e:
            print("Ops!", e, "Occurred")
        finally:
            return psb_moves

    def move(self, target: list[int], situation: list[list]) -> list[list]:
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        psb_moves = self.legal_moves(situation)
        # checking if the move is possible
        if target not in psb_moves:
            return situation
        new_situation = self.update_situation(target, situation)
        self._has_moved = True
        return new_situation
