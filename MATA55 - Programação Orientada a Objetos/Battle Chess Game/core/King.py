from .Piece import Piece
from .Rook import Rook
from .Color import Color
from .Pieces_type import Piece_type


class King(Piece):
    def __init__(self, color: Color, x: int, y: int):
        super(King, self).__init__(color, x, y)
        self.is_checked = False
        self.is_mated = False
        self.__id = Piece_type.KING.value + color.value

    @property
    def movement(self) -> list[list[int]]:
        """Returns the lists of potential moves in any given position"""
        self._list_moves.clear()
        for square in range(self.x - 1, self.x + 2):
            if 0 <= square <= 7:
                if 0 <= self.y < 7:
                    self._list_moves.append([self.y + 1, square])
                if square != self.x:
                    self._list_moves.append([self.y, square])
                if 0 < self.y <= 7:
                    self._list_moves.append([self.y - 1, square])
        return self._list_moves.copy()

    def _free_spaces(self, situation: list[list], rook: Rook) -> bool:
        """Private auxiliary method to check if the squares between the king and rook are free"""
        free = True
        if rook.x == 7:
            for square in range(self.x + 1, rook.x):
                if situation[self.y][square] is not None:
                    free = False
                    break
        elif rook.x == 0:
            for square in range(rook.x + 1, self.x):
                if situation[self.y][square] is not None:
                    free = False
                    break
        return free

    def castle(self, situation: list[list], rook: Rook) -> bool:
        """Checks if castle is possible"""
        if rook.color != self.color:
            return False
            
        if not self.has_moved and not rook.has_moved and not self.is_checked:
            return self._free_spaces(situation, rook)

        return False

    def legal_moves(self, situation: list[list]) -> list[list[int]]:
        """Restricts the list of movements to only legal moves.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the legal moves"""
        psb_moves = self.movement
        lgl_moves = []
        k_rook, q_rook = None, None
        if not self.has_moved:
            k_rook = situation[self.y][0]
            q_rook = situation[self.y][7]
        try:
            # checking if king side castle is possible
            if isinstance(k_rook, Rook) and self.castle(situation, k_rook):
                lgl_moves.append([self.y, self.x - 2])
            # checking if queen side castle is possible
            if isinstance(q_rook, Rook) and self.castle(situation, q_rook):
                lgl_moves.append([self.y, self.x + 2])
            # checking if the square is defended
            for move in psb_moves:
                if situation[move[0]][move[1]] is None or situation[move[0]][move[1]].color != self.color:
                    lgl_moves.append(move)
        except IndexError as e:
            print("Ops!", e, "Occurred")
        finally:
            return lgl_moves

    def move(self, target: list[int], situation: list[list]) -> list[list]:
        """Executes the move of the piece.
        Receives the target square and the situation of the board,
        a matrix with all the instances in the game right now.
        Returns the new updated situation if the move was possible"""
        psb_moves = self.legal_moves(situation)
        # checking if the move is possible
        if target not in psb_moves:
            return situation
        # checking if the desired move is to castle
        if target[1] == self.x + 2 or target[1] == self.x - 2:
            # finding the rook
            rook_pos = 7 if target[1] == self.x + 2 else 0
            rook = situation[self.y][rook_pos]
            # moving the rook
            rook_target = 4 if rook_pos == 7 else 2
            aux_situation = rook.update_situation([self.y, rook_target], situation)

            new_situation = self.update_situation(target, aux_situation)
        else:
            new_situation = self.update_situation(target, situation)
        self._has_moved = True
        return new_situation
