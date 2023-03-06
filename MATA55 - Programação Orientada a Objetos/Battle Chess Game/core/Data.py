from .Bishop import Bishop
from .Knight import Knight
from .Piece import Piece
from .Queen import Queen
from .King import King
from .Pawn import Pawn
from .Rook import Rook
from .Color import Color

from typing import Callable, Optional, Type, Union
import io, os, time


class GameData():
    """
    Classe para salvar e reproduzir partidas.
    """
    
    __PIECE_NAMES = ["pawn", "king", "knight", "queen", "bishop", "rook"]
    
    def __init__(self, directory:str):
        self.__directory = directory
        
        self.__file:Optional[io.TextIOWrapper] = None
        self.__closed = True
        self.__game_id:Optional[str] = None

    @property
    def id(self) -> Optional[str]:
        return self.__game_id

    @property
    def replay_ended(self) -> bool:
        return self.__finished

    def __get_game_id(self) -> str:
        """
        Retorna o ID do jogo.
        """
        return str(os.getpid()) + "i" + str(len([filename for filename in os.listdir(self.__directory) if filename.endswith(".replay")]))

    def __get_piece_id(self, piece: Piece) -> str:
        """
        Retorna o ID da peça, mesmo se não houver uma peça.
        """
        if not piece:
            return chr(97)

        piece_id = (self.__PIECE_NAMES.index(piece.name) + 1) * 2
        piece_id += piece.color.value
        
        return chr(piece_id + 97)

    def __get_piece_by_id(self, piece_id_:str, x:int, y:int) -> Optional[Piece]:
        """
        Retorna a peça através do seu ID.
        """
        piece_id = ord(piece_id_) - 97

        if piece_id == 0:
            return None

        # Verifica se a peça é branca ou preta observando
        # se o ID é par ou ímpar. Após isso, obtém-se o
        # tipo da peça pelo índice, realizando o cálculo
        # reverso do método de obtenção de ID por peça.
        if piece_id % 2 == 0:
            piece_name = self.__PIECE_NAMES[piece_id // 2 - 1]
            color = Color.White
        else:
            piece_name = self.__PIECE_NAMES[(piece_id - 1) // 2 - 1]
            color = Color.Black

        # Obtém o tipo da peça e retorna o seu objeto.
        pt:dict[str, Type[Piece]] = {
            "bishop": Bishop,
            "knight": Knight,
            "rook": Rook,
            "queen": Queen,
            "king": King,
            "pawn": Pawn,
        }
        PieceType = pt[piece_name]

        return PieceType(color, x, y)

    def close(self, winner:Optional[Color]=None):
        """
        Fecha o arquivo. Caso tenha sido aberto em modo escrita,
        o jogo, antes salvo em um arquivo temporário, será salvo
        em um arquivo apropriado, com a cor do vencedor, passada
        como parâmetro, sendo registrada.
        """

        if self.__closed:
            return
        
        if not (self.__file is None):
            self.__file.close()
        
        self.__file = None
        self.__closed = True

        # Renomeia o arquivo temporário.
        if not self.__read_mode and not winner is None:
            new_filename = "{}_{}_{}x{}_{}.replay".format( # NAME_WINNER_NxM_GAMEID.replay
                self.__game_name, winner.value,
                *self.__score, self.__game_id
            ) 
            new_filename = os.path.join(self.__directory, new_filename)
            os.rename(self.__filename, new_filename)

        # Se a partida encerrou sem vencedores, o jogo não é salvo.
        if not self.__read_mode and winner is None:
            os.remove(self.__filename)

    def get_game_list(self) -> list[list]:
        """
        Retorna uma lista com todos os jogos salvos e suas informações gerais.
        """
        games = []

        # Percorre o diretório procurando pelos arquivos de replay.
        for filename in os.listdir(self.__directory):
            if filename.endswith(".replay") and filename.count("_") == 3:

                # Obtém os dados do jogo pelo nome do arquivo.
                data = filename.rstrip(".replay").split("_")
                name = data[0]
                winner = "WHITE" if data[1] == "0" else "BLACK"
                score = data[2].split("x")
                game_id = data[3]

                # Obtém a data e hora da finalização da partida formatadas.
                date = os.path.getctime(os.path.join(self.__directory, filename))
                fmtdate = time.strftime("%d/%m/%y às %H:%M", time.localtime(date))
                
                games.append([name, winner, score[0], score[1], game_id, fmtdate, date])

        # Ordena a lista de jogos pela data de finalização.
        key_sort:Callable[[list], float] = lambda game: game[-1]
        games.sort(key=key_sort, reverse=True)
        return games

    def open(self, game_id:Optional[str]=None, game_name:str="game"):
        """
        Abre um arquivo, para leitura ou escrita. Em caso de leitura,
        deve ser informado o ID do jogo em questão.
        """
        self.__game_id = None
        self.__finished = False
        self.__lines = 0

        # Verifica se o arquivo já foi aberto.
        if self.__file: raise io.UnsupportedOperation("file is already open")

        self.__read_mode = bool(not game_id is None)

        # Se solicitado a abertura do arquivo, o mesmo será procurado pelo ID do jogo.
        if game_id:
            for filename in os.listdir(self.__directory):
                if filename.endswith(".replay") and "_{}".format(game_id) in filename:
                    filename = os.path.join(self.__directory, filename)
                    break
            else:
                raise FileNotFoundError("The game could not be found by ID {}".format(game_id))

        # Se solicitado o modo de escrita, um arquivo temporário será criado para salvar o jogo continuamente.
        else:
            filename = os.path.join(self.__directory, str(os.getpid()) + "{}.temp".format(game_id))
            game_id = self.__get_game_id()

        self.__game_id = game_id
        self.__filename = filename
        self.__game_name = game_name
        self.__closed = False

        # Abre o arquivo para leitura ou escrita.
        self.__file = open(self.__filename, "r" if self.__read_mode else "w")

    def read(self) -> list:
        """
        Retorna uma matriz que é o estado do tabuleiro no momento atual. (somente no modo leitura)
        """
        if self.__file is None:
            raise TypeError("self.__file must be a 'io.TextIOWrapper', not 'NoneType'")

        if not self.__read_mode or self.__closed:
            raise io.UnsupportedOperation("not readable")
        
        board:list[list] = [list() for i in range(8)]

        # Faz a leitura da linha completa.
        string = self.__file.read(8 * 8 + 1).rstrip("\n")

        # Verifica se já chegou no final. Se sim, o último estado do tabuleiro será retornado.
        if not string:
            self.back()
            self.__finished = True
            string = self.__file.read(8 * 8 + 1).rstrip("\n")
        else:
            self.__finished = False

        # Volta o ponteiro do arquivo para a linha lida.
        self.__file.seek(self.__lines)

        # Através dos IDs obtidos, as peças serão inseridas na matriz.
        for index in range(8 * 8):
            x, y = index % 8, index // 8
            board[y].append(self.__get_piece_by_id(string[index], x, y))
        return board

    def back(self):
        """
        Volta para o estado anterior do tabuleiro. (somente no modo leitura)
        """
        if not self.__read_mode or self.__closed: raise io.UnsupportedOperation("not readable")

        # Verifica se já chegou no ínicio do arquivo.
        if self.__lines <= 0: self.__lines = 0
        else: self.__lines -= 8 * 8 + 2

        self.__file.seek(self.__lines)

    def next(self):
        """
        Avança para o próximo estado do tabuleiro. (somente no modo leitura)
        """
        if not self.__read_mode or self.__closed: raise io.UnsupportedOperation("not readable")

        self.__lines += 8 * 8 + 2
        self.__file.seek(self.__lines)
    
    def save(self, board:list[list]):
        """
        Salva um estado do tabuleiro. (somente no modo escrita)
        """
        if self.__file is None:
            raise TypeError("self.__file must be a 'io.TextIOWrapper', not 'NoneType'")

        if self.__read_mode or self.__closed:
            raise io.UnsupportedOperation("not writable")

        self.__score = [0, 0]

        # Percorre a matriz, obtendo e salvando no arquivo o ID de cada peça,
        # além da quantidade atual de peças no mesmo.
        for row in board:
            for piece in row:
                self.__file.write(self.__get_piece_id(piece))
                if piece: self.__score[piece.color.value] += 1
                
        self.__file.write("\n")
        
        

