from .screen import Screen
from .util import Button, WidgetGroup
from pyglet.window import mouse, key
from typing import Callable

class HistoryScreen(Screen):
    """
    Classe para criar uma tela de histórico de partidas.
    """
    
    def __init__(self, application):
        super().__init__(application)
        
        self.__replay_function = lambda game_id: None
        self.__game_list = []
        
        self.__index = 0
        self.__build()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        
        self.__batch = self.create_batch()
        self.__text_batch = self.create_batch()
        self.__widget_group = WidgetGroup()

        # Obtém o tamanho e a posição do frame de partida.
        frame_width = self.width * 0.5
        frame_height = frame_width * 0.8
        frame_x = self.width / 2 - frame_width / 2
        frame_y = self.height / 2 - frame_height / 2

        # Obtém o tamanho e a posição da imagem de histórico vazio.
        no_history_width = frame_width * 0.3
        no_history_height = no_history_width * 1.28
        no_history_x = self.width / 2 - no_history_width / 2
        no_history_y = frame_y + frame_height * 0.86 - no_history_height

        # Obtém o tamanho e a posição do botão de play.
        play_button_width = self.width * 0.06
        play_button_height = play_button_width
        play_button_x = frame_x + frame_width * 1.1
        play_button_y = self.height / 2 - play_button_height / 2

        # Obtém o tamanho e a posição dos botões de controle.
        control_button_width = play_button_width
        control_button_height = control_button_width * 1.265
        control_button_x = play_button_x
        back_button_y = play_button_y - control_button_height * 1.5
        next_button_y = play_button_y + play_button_height + control_button_height * 0.5

        # Obtém o tamanho e a posição da imagem do tabuleiro.
        self.__board_size = frame_height * 0.4
        self.__board_x = int(frame_x + frame_width * 0.87 - self.__board_size)
        self.__board_y = int(frame_y + frame_height * 0.85 - self.__board_size)

        # Obtém o tamanho e a posição das peças.
        piece_size = frame_height * 0.1
        piece_x = frame_x + frame_width * 0.13
        piece_y = self.__board_y + self.__board_size - piece_size

        # Obtém a posição do texto de resultado.
        result_x = piece_x + (self.__board_x - piece_x) / 2
        result_y = self.__board_y

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("history", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria o botão de play.
        play_button_filename = application.paths.get_image("history", "buttons", "play.png")
        activated_play_button_filename = application.paths.get_image("history", "buttons", "activated_play.png")
        
        self.__play_button = Button(
            self, play_button_x, play_button_y, (play_button_width, play_button_height),
            (play_button_filename, activated_play_button_filename),
            widget_group = self.__widget_group
        )

        # Cria os botões de controle da lista de histórico.
        back_button_filename = application.paths.get_image("history", "buttons", "back.png")
        activated_back_button_filename = application.paths.get_image("history", "buttons", "activated_back.png")

        next_button_filename = application.paths.get_image("history", "buttons", "next.png")
        activated_next_button_filename = application.paths.get_image("history", "buttons", "activated_next.png")
        
        self.__back_button = Button(
            self, control_button_x, back_button_y, (control_button_width, control_button_height),
            (back_button_filename, activated_back_button_filename),
            widget_group = self.__widget_group
        )
        
        self.__next_button = Button(
            self, control_button_x, next_button_y, (control_button_width, control_button_height),
            (next_button_filename, activated_next_button_filename),
            widget_group = self.__widget_group
        )

        # Cria o frame de partida.
        frame_filename = application.paths.get_image("history", "frame.png")
        frame_image = self.load_image(frame_filename, (frame_width, frame_height))
        self.__frame = self.create_sprite(frame_image, frame_x, frame_y)

        # Cria imagem para informar que o histórico está vazio.
        no_history_filename = application.paths.get_image("history", "empty.png")
        no_history_image = self.load_image(no_history_filename, (no_history_width, no_history_height))
        self.__no_history = self.create_sprite(no_history_image, no_history_x, no_history_y)

        # Cria texto para modo de jogo.
        self.__mode_text = self.create_text(
            str(), x = frame_x + frame_width / 2, y = frame_y + frame_height * 0.25,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.026), font_name = "Comic Sans MS",
            anchor_x = "center", anchor_y = "center", batch = self.__text_batch
        )

        # Cria texto para data de jogo.
        self.__date_text = self.create_text(
            str(), x = frame_x + frame_width / 2, y = self.__board_y * 0.95,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.012), font_name = "Comic Sans MS",
            anchor_x = "center", anchor_y = "bottom", batch = self.__text_batch
        )        

        # Cria texto para o resultado do jogo.
        self.__result_text = self.create_text(
            str(), x = result_x, y = result_y, font_name = "Arial Black",
            color = (100, 71, 50, 255), font_size = int(self.width * 0.024),
            anchor_x = "center", anchor_y = "top", batch = self.__text_batch
        )

        # Cria texto para a quantidade de peças no tabuleiro.
        self.__black_piece_text = self.create_text(
            str(), x = piece_x + piece_size * 1.1, y = piece_y + piece_size * 0.5,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.02),
            anchor_x = "left", anchor_y = "center", batch = self.__text_batch
        )
        
        self.__white_piece_text = self.create_text(
            str(), x = piece_x + piece_size * 1.1, y = piece_y - piece_size * 1.5 + piece_size * 0.5,
            color = (30, 30, 30, 255), font_size = int(self.width * 0.02),
            anchor_x = "left", anchor_y = "center", batch = self.__text_batch
        )

        # Cria as imagens das peças.
        black_piece_filename = application.paths.get_image("history", "black_piece.png")
        black_piece_image = self.load_image(black_piece_filename, (piece_size, piece_size))

        white_piece_filename = application.paths.get_image("history", "white_piece.png")
        white_piece_image = self.load_image(white_piece_filename, (piece_size, piece_size))
        
        self.__black_piece = self.create_sprite(black_piece_image, piece_x, piece_y)
        self.__white_piece = self.create_sprite(white_piece_image, piece_x, piece_y - piece_size * 1.5)

        # Cria a borda para o tabuleiro.
        self.__board_border = self.create_rectangle(
            self.__board_x - 1, self.__board_y - 1,
            self.__board_size + 2, self.__board_size + 2,
            color = (0, 0, 0)
        )
        self.__board = None

    def __change_game(self):
        """
        Troca o jogo em exibição.
        """
        self.__game = None

        # Verifica se a lista está vazia. Se sim, será
        # mostrada a informação de histórico vazio.
        if not self.__game_list:
            return self.__set_empty_history()

        # Obtém as informações do jogo pelo índice atual.
        self.__game = self.__game_list[self.__index]

        # Define a imagem do tabuleiro.
        try: self.__set_board_image()

        # Se não houver imagem, o jogo em questão será indisponibilizado para replay.
        except FileNotFoundError:
            self.__game_list.pop(self.__index)
            return self.__update_index(step = 0)

        # Define o tipo do jogo e a data de quando foi realizado.
        self.__mode_text.text = "JOGO " + self.__game[0]
        self.__date_text.text = self.__game[5]

        # Define a mensagem de resultado do jogo.
        if self.__game[1].upper() == "WHITE": self.__result_text.text = "VITÓRIA"
        else: self.__result_text.text = "DERROTA"

        # Define a quantidade de peças no tabuleiro.
        self.__black_piece_text.text = str(self.__game[2])
        self.__white_piece_text.text = str(self.__game[3])

        # Mostra ao usuário qual o índice em que ele está na lista de histórico de partidas.
        message = "Partida" if len(self.__game_list) == 1 else "Partidas"
        message = "{} de {} {}".format(self.__index + 1, len(self.__game_list), message)
        
        self.get_application().set_message_to_title(message)

    def __set_board_image(self):
        """
        Define a imagem de tabuleiro.
        """
        game_id = self.__game[4]
        
        board_filename = self.get_application().paths.get_replay_image("{}.png".format(game_id))
        board_image = self.load_image(board_filename, (self.__board_size, self.__board_size), save = False)

        if not self.__board: self.__board = self.create_sprite(board_image, self.__board_x, self.__board_y)
        else: self.__board.image = board_image

    def __set_empty_history(self):
        """
        Define o estado de histórico vazio.
        """
        self.__mode_text.text = "Histórico Vazio"
        self.__date_text.text = ""
        
        self.__black_piece_text.text = ""
        self.__white_piece_text.text = ""
        self.__result_text.text = ""
        
        self.__board = None
        self.__game = None

    def __update_index(self, step: int = 1):
        """
        Atualiza o índice atual da lista de partidas.
        """
        if len(self.__game_list) == 0: self.__index = 0
        else: self.__index = (self.__index + step) % len(self.__game_list)
        
        self.__change_game()

    def set_history(self, game_list: list[list[str]]):
        """
        Define os jogos disponíveis para replay.
        """
        self.__game_list = game_list
        self.__index = 0
        self.__change_game()

    def set_replay_function(self, function: Callable):
        """
        Define uma função de replay.
        """
        self.__replay_function = function

    def on_draw_screen(self, by_scheduler: bool = False):
        """
        Evento para desenhar a tela.
        """
        self.__background_image.blit(0, 0)
        self.__frame.draw()
        
        self.__batch.draw()
        self.__text_batch.draw()
        self.__widget_group.draw()

        # Desenha as imagens e textos com as informações da partida.
        if self.__game and self.__board:
            self.__black_piece.draw()
            self.__white_piece.draw()
            
            self.__board_border.draw()
            self.__board.draw()

        # Se não houver jogo, desenha uma imagem de histórico vazio.
        else: self.__no_history.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        super().on_key_press(symbol, modifiers)
        
        # Caso o ESC seja apertado, significa que o usuário deseja sair desta tela.
        if symbol == key.ESCAPE:
            self.get_application().go_back()

        # Troca o jogo em exibição.
        elif symbol == key.DOWN: self.__update_index(step = 1)
        elif symbol == key.UP: self.__update_index(step = -1)

        # Inicia o replay do jogo, utilizando o ID do mesmo.
        elif symbol in [key.ENTER, key.SPACE] and self.__game_list:
            self.__replay_function(self.__game[4])

        return True

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        x, y = super().on_mouse_motion(*args)[0: 2]
        self.__play_button.check(x, y)
        self.__back_button.check(x, y)
        self.__next_button.check(x, y)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse pressionado e liberado.
        """
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return

        if self.__play_button.check(x, y):
            self.on_key_press(key.ENTER, None)
            
        elif self.__back_button.check(x, y):
            self.on_key_press(key.UP, None)
        
        elif self.__next_button.check(x, y):
            self.on_key_press(key.DOWN, None)
