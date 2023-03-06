from .Bishop import Bishop
from .Knight import Knight
from .Piece import Piece
from .Queen import Queen
from .King import King
from .Pawn import Pawn
from .Rook import Rook
from .Color import Color
from enum import Enum
from typing import Optional, Type

class Board():
    """
    Classe para criar e gerenciar o tabuleiro do jogo.
    """
    def __init__(self):
        self.pecas = [[None] * 8 for i in range(8)]

        # Adiciona ao tabuleiro os peões.
        for i in range(8):
            self.add_piece(Pawn(Color.White, i, 1))   

        for i in range(8):
            self.add_piece(Pawn(Color.Black, i, 6))

        # Cria as torres.
        wr0 = Rook(Color.White, 0, 0)
        wr1 = Rook(Color.White, 7, 0)
        br0 = Rook(Color.Black, 0, 7)
        br1 = Rook(Color.Black, 7, 7)

        # Cria os cavalos.
        wn0 = Knight(Color.White, 1, 0)
        wn1 = Knight(Color.White, 6, 0)
        bn0 = Knight(Color.Black, 1, 7)
        bn1 = Knight(Color.Black, 6, 7)

        # Cria os bispos.
        wb0 = Bishop(Color.White, 2, 0)
        wb1 = Bishop(Color.White, 5, 0)
        bb0 = Bishop(Color.Black, 2, 7)
        bb1 = Bishop(Color.Black, 5, 7)

        # Cria os reis.
        wk = King(Color.White, 3, 0)
        bk = King(Color.Black, 3, 7)

        # Cria as rainhas.
        wq = Queen(Color.White, 4, 0)
        bq = Queen(Color.Black, 4, 7)

        # Adiciona as peças criadas acima ao tabuleiro.
        for p in (wr0, wr1, br0, br1, wn0, wn1, bn0, bn1, wb0, wb1, bb0, bb1, bq, wq, bk, wk):
            self.add_piece(p)

    def add_piece(self, piece:Piece):
        """
        Insere uma peça no tabuleiro, através de suas próprias coordenadas.
        """
        self.pecas[piece.y][piece.x] = piece

    def check_promotion(self) -> Optional[Piece]:
        """
        Percorre as extremidades do tabuleiro, verificando
        se há promoções. Se sim, a peça será retornada.
        """
        for i in range(0, 8, 7):
            for j in range(8):
                piece = self.pecas[i][j]

                # Se houver promoção, a peça é retornada.
                if piece and piece.name == "pawn" and piece.promotion:
                    return piece

        return None

    def set_promotion(self, piece_name:str):
        """
        Promove um peão, dado um novo tipo de peça
        em que o mesmo será transformado.
        """
        cp:dict[str, Type[Piece]] = {"bishop": Bishop, "knight": Knight, "rook": Rook, "queen": Queen}
        ChosenPiece = cp.get(piece_name)
        
        if not ChosenPiece:
            raise ValueError("peça inválida para promoção")
        
        piece = self.check_promotion()
        if not (piece is None):
            self.pecas[piece.y][piece.x] = ChosenPiece(piece.color, piece.x, piece.y)
