from .Player import Player
from .Piece import Piece
from .Board import Board
from .Color import Color
from .Data import GameData
from copy import deepcopy
from typing import Optional, Union

class FinishedGameError(Exception):
    """
    Exceção relacionada ào fato do jogo ter encerrado.
    """
    pass

class NoPromotionError(Exception):
    """
    Exceção relacionada com eventos quanto não há promoção.
    """
    pass

class GameModeError(Exception):
    """
    Exceção para tentativas de operações em um modo de jogo inválido.
    """
    pass

class ChessGame:
    """
    Classe principal do jogo.
    """
    
    def __init__(self, replay_path:str):
        # Cria um objeto para salvar e reproduzir replays de jogos.
        self.__game_data = GameData(replay_path)

        # Cria dois jogadores.
        self.__white_player = Player(Color.White)
        self.__black_player = Player(Color.Black)
        
        self.__all_legal_moves:dict[tuple, list[list]] = {}
        
        self.__replaying = False

        self.__destroyed_pieces:list[Optional[Piece]] = []
        self.__attacked = False
        self.__stalemated = False

    @property
    def white_player(self) -> Player:
        if self.__replaying:
            raise GameModeError("Você não pode usar esse atributo no modo replay")
        return self.__white_player

    @property
    def black_player(self) -> Player:
        if self.__replaying:
            raise GameModeError("Você não pode usar esse atributo no modo replay")
        return self.__black_player

    @property
    def board(self) -> Board:
        return self.__board

    @property
    def id(self) -> Optional[str]:
        return self.__game_data.id

    @property
    def attacked(self) -> bool:
        return self.__attacked

    @property
    def destroyed_pieces(self) -> list:
        return [piece for piece in self.__destroyed_pieces if piece]

    @property
    def replay_on_begin(self) -> bool:
        return self.__replay_steps == 0

    @property
    def replay_on_end(self) -> bool:
        return self.__game_data.replay_ended
    
    @property
    def all_legal_moves(self) -> dict[tuple, list[list[int]]]:
        return self.__all_legal_moves
    
    @property
    def stalemated(self) -> bool:
        return self.__stalemated

    def close(self):
        """
        Encerra o jogo.
        """
        self.__replaying = False
        self.__attacked = False

        self.__destroyed_pieces = []

        self.__game_data.close()

    def __get_difference_between_piece_lists(self, list_1: list[Piece], list_2: list[Piece]) -> Piece:
        """
        Método para o sistema de replay, para obter a diferença
        entre duas listas de peças.
        """
        list_1.sort(key = lambda piece: piece.name)
        list_2.sort(key = lambda piece: piece.name)

        for index in range(len(list_2)):
            if not type(list_1[index]) is type(list_2[index]): return list_1[index]
        return list_1[-1]

    def __update_destroyed_pieces(self, new_board: list[list]):
        """
        Método para o sistema de replay, para atualizar a lista
        de peças destruídas, dado um nome tabuleiro.
        """
        white = []
        black = []

        new_white = []
        new_black = []

        # Obtém todas as peças brancas e pretas do tabuleiro atual separadas em listas.
        for piece in [piece for row in self.__board.pecas for piece in row]:
            if not piece: continue
            
            if piece.color == Color.Black: black.append(piece)
            else: white.append(piece)

        # Obtém todas as peças brancas e pretas do novo tabuleiro separadas em listas.
        for piece in [piece for row in new_board for piece in row]:
            if not piece: continue
            
            if piece.color == Color.Black: new_black.append(piece)
            else: new_white.append(piece)

        # Verifica se há uma diferença no tamanho entre os tabuleiros. Se houver,
        # significa que uma peça foi eliminada. Nesse caso, é realizado a busca
        # de qual peça foi eliminada, para que a mesma possa ser registrada na lista.
        if len(white) != len(new_white):
            self.__attacked = True
            piece = self.__get_difference_between_piece_lists(white, new_white)
            self.__destroyed_pieces.append(piece)
            
        elif len(black) != len(new_black):
            self.__attacked = True
            piece = self.__get_difference_between_piece_lists(black, new_black)
            self.__destroyed_pieces.append(piece)

        # Se não houver peças eliminadas, será adicionado None à lista, indicando
        # que não houve eliminações naquele momento do replay.
        else:
            self.__destroyed_pieces.append(None)
            self.__attacked = False
        
    def back(self):
        """
        Volta para o estado anterior do tabuleiro. (somente no modo replay)
        """
        if not self.__replaying:
            raise GameModeError("Você deve iniciar o modo replay para usar esse método")

        # Remove a última peça da lista de peças destruídas.
        self.__destroyed_pieces = self.__destroyed_pieces[:-1]
        self.__attacked = False

        # Verifica se já chegou no início.
        if self.replay_on_begin: return

        if self.__replay_steps > 0: self.__replay_steps -= 1

        # Retrocede e atualiza o tabuleiro atual.
        self.__game_data.back()
        self.__board.pecas = self.__game_data.read()

    def next(self):
        """
        Avança para o próximo estado do tabuleiro. (somente no modo replay)
        """
        if not self.__replaying:
            raise GameModeError("Você deve iniciar o modo replay para usar esse método")

        # Avança e obtém o novo estado do tabuleiro.
        self.__game_data.next()
        new_board = self.__game_data.read()

        # Verifica se já chegou no fim.
        if self.replay_on_end: return
        self.__replay_steps += 1

        # Atualiza a lista de peças destruídas e o tabuleiro atual.
        self.__update_destroyed_pieces(new_board)
        self.__board.pecas = new_board

    def start_replay(self, game_id:str):
        """
        Inicia o modo replay de um determinado jogo pelo seu ID.
        """
        self.close()
        self.__replaying = True
        self.__board = Board()

        self.__replay_steps = 0
        self.__game_data.open(game_id)
        self.__board.pecas = self.__game_data.read()

    def new_game(self, name:str="Game"):
        """
        Inicia um novo jogo.
        """
        self.close()

        # Define como primeiro jogador o que possui as peças brancas.
        self.__current_player = self.__white_player
        self.__white_player.played = True
        self.__winner:Optional[Color] = None

        # Cria um novo tabuleiro.
        self.__board = Board()
        self.__check = False
        self.__stalemated = False

        # Salva o estado inicial do tabuleiro.
        self.__game_data.open(game_name = name)
        self.__game_data.save(self.__board.pecas)

        # Define o rei de cada jogador.
        self.__white_player.king = self.__board.pecas[0][3]
        self.__black_player.king = self.__board.pecas[7][3] 

        self.__all_legal_moves_update()

    def get_history(self) -> list[list]:
        """
        Retorna uma lista com o histórico dos jogos realizados.
        """
        return self.__game_data.get_game_list()

    def __change_player(self):
        """
        Troca o jogador que realizará a próxima jogada.
        """
        self.__white_player.played = not self.__white_player.played
        self.__black_player.played = not self.__black_player.played

        self.__current_player =  self.__white_player or self.__black_player

    def __gen_defense_board(self, player:Player, board:Optional[list[list]]=None) -> list[list]:
        if board is None:
            board = self.__board.pecas

        new_defense_board = [[False for _ in range(8)] for _ in range(8)]

        for x in range(8):
            for y in range(8):
                peca = self.get_piece(x, y, board)
                if (peca is None) or peca.color != player.color:
                    continue

                for m in peca.legal_moves(board):
                    new_defense_board[m[0]][m[1]] = True

        return new_defense_board

    def __defense_update(self):
        for p in (self.__white_player, self.__black_player):
            p.defense = self.__gen_defense_board(p)

    def __all_legal_moves_update(self):
        play_color = self.__current_player.color
        new_clm = {}

        for x in range(8):
            for y in range(8):
                peca = self.get_piece(x, y)
                if peca == None or peca.color != play_color:
                    continue

                lm = peca.legal_moves(self.__board.pecas)
                for mov in lm:
                    if self.__simule_check_out(peca.coords, mov):
                        new_clm[peca.coords] = new_clm.get(peca.coords, []) + [mov]

        self.__all_legal_moves = new_clm

    def __check_verify(self):
        adv_player = self.__white_player if self.__current_player == self.__black_player else self.__black_player
        king_pos = self.__current_player.king.coords

        if adv_player.defense[king_pos[1]][king_pos[0]]:
            self.__check = True

            if not self.__all_legal_moves:
                self.__winner = adv_player.color
        else:
            self.__check = False

    def __simule_check_out(self, from_:Union[tuple, list], to:Union[tuple, list]) -> bool:
        if self.__current_player.king is None:
            raise TypeError("self.__current_player.king must be a 'core.King.King', not 'NoneType'")

        adv_player = self.__white_player if self.__current_player == self.__black_player else self.__black_player

        xi, yi = from_
        yf, xf = to
        kx, ky = self.__current_player.king.coords
        if (xi, yi) == (kx, ky):
            kx, ky = xf, yf

        board = deepcopy(self.__board.pecas)
        piece = board[yi][xi]
        piece.move(to, board)
        defended = self.__gen_defense_board(adv_player, board)

        return not defended[ky][kx]

    def has_promotion(self) -> bool:
        """
        Verifica se existe promoção de algum peão no tabuleiro. (não disponível no modo replay)
        """
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")
        return bool(self.__board.check_promotion()) and not self.get_winner()

    def set_promotion(self, piece_name:str):
        """
        Define um tipo de peça para promover o peão. (não disponível no modo replay)
        """
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")

        # Verifica se existem promoções.
        if not self.has_promotion():
            NoPromotionError("Não há promoções disponíveis no momento")

        # Define a promoção e salva o tabuleiro com a troca da peça.
        self.__board.set_promotion(piece_name)
        self.__game_data.save(self.__board.pecas)

        # Libera o próximo jogador para jogar.
        self.__change_player()

        # Atualiza os movimentos legais
        self.__defense_update()
        self.__all_legal_moves_update()
        self.__check_verify()
    
    def get_player(self) -> Player:
        """
        Retorna o jogador do turno atual. (não disponível no modo replay)
        """
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")

        return self.__current_player

    def get_piece(self, x: int, y: int, board:Optional[list[list[Optional[Piece]]]]=None) -> Optional[Piece]:
        """
        Retorna a peça em uma dada posição XY (coluna, linha) do tabuleiro, de 0 à 7.
        """
        if board is None:
            board = self.__board.pecas

        try:
            return board[x][y]

        except KeyError:
            return None

    def get_winner(self) -> Optional[Color]:
        """
        Retorna o vencedor do jogo se houver. (não disponível no modo replay)
        """
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")

        return self.__winner

    def is_check(self) -> bool:
        """
        Verifica se o rei está em cheque.
        """
        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")
        return self.__check

    def play(self, piece:Piece, to:Union[tuple[int, int], list[int]]) -> bool:
        """
        Realiza uma jogada, dado uma peça e uma posição de
        destino XY (coluna, linha) no tabuleiro.
        """

        if self.__stalemated:
            raise FinishedGameError("A partida já encerrou, pois está empatada")

        if self.__replaying:
            raise GameModeError("Você não pode usar esse método no modo replay")

        if not isinstance(to, list):
            to = list(to)

        # Verifica se o jogo já acabou.
        if self.__winner:
            raise FinishedGameError("A partida já encerrou")

        # Verifica se há promoções. Se sim, o próximo jogador só poderá jogar
        # se o jogador anterior resolver essa pendência.
        if self.has_promotion():
            raise NoPromotionError("Promova o peão antes de jogar")

        # Verifica se o movimento solicitado é válido, com base nas regras da peça.
        if not (to in self.__all_legal_moves.get(piece.coords, [])):
            return False

        self.__check = False

        # Obtém o alvo.
        target_piece = self.__board.pecas[to[0]][to[1]]

        # Se o alvo for uma peça, ela será adicionada à lista de peças destruídas.
        if target_piece:
            self.__attacked = True
            self.__destroyed_pieces.append(target_piece)

            # Se a peça destruída foi o rei, o jogador será declarado vencedor.
            if target_piece.name == "king":
                self.__winner = piece.color
            
        else:
            self.__attacked = False

        # Realiza o movimento da peça e salva o novo estado do tabuleiro.
        self.__board.pecas = piece.move(list(to), self.__board.pecas)
        self.__game_data.save(self.__board.pecas)

        # Se não houver promoções, o turno do jogador será alterado e os movimentos legais atualizados
        if not self.has_promotion():
            self.__change_player()
            self.__defense_update()
            self.__all_legal_moves_update()
            self.__check_verify()

        # Se houver vencedor, o arquivo de replay será fechado, informando quem foi o vencedor.
        if self.__winner:
            self.__game_data.close(self.__winner)

        if (not self.__check) and (not self.__all_legal_moves):
            self.__stalemated = True

        return True
