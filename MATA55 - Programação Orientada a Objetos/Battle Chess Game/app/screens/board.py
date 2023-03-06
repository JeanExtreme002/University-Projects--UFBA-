from .screen import Screen
from .util import ConfirmationPopup, MediaController, Popup, PromotionSelection
from pyglet.window import mouse, key
from typing import Callable, Optional, Union
import random

class BoardScreen(Screen):
    """
    Classe para criar a tela do tabuleiro.
    """
    
    __LOCAL_MODE = 0
    __ONLINE_MODE = 1
    __REPLAY_MODE = 2

    __BORDER_COLOR = (0, 0, 0)
    __LIGHT_COLOR = (255, 248, 220)
    __DARK_COLOR = (100, 71, 50)

    __COORD_TEXT_COLOR = [
        (255, 255, 255, 255),
        (220, 220, 220, 255),
        (220, 0, 0, 255)
    ]

    __DEFEAT_MESSAGES = [
        "Infelizmente, você perdeu...",
        "Você perdeu. Talvez na próxima...",
        "Você foi derrotado! Mais sorte na próxima.",
        "Seu adversário o derrotou!",
        "Você perdeu... Vença-o na próxima!",
        "Foi uma boa partida! Porém, você perdeu.",
        "Você perdeu. Pratique mais!",
        "Seu rei foi eliminado. Você perdeu!"
    ]

    __VICTORY_MESSAGES = [
        "Parabéns. Você venceu a partida!",
        "Foi um ótimo jogo. Parabéns pela vitória!",
        "Ótima jogada! Parabéns pela vitória!",
        "Você venceu! Foi uma ótima partida!",
        "Mais uma para o histórico. Parabéns!",
        "Vitória sensacional. Parabéns!",
        "Que bela jogada! Parabéns pela vitória!"
    ]

    __PROMOTION_PIECES = ["bishop", "knight", "queen", "rook"]
    
    def __init__(self, application):
        super().__init__(application)
        
        self.__moving_by_mouse = False
        self.__moving_by_keyboard = False

        self.__selected_piece = None
        self.__selected_piece_shadow = None
        self.__selected_piece_index = None
        self.__selected_piece_position = None

        self.__selected_target_shadow = None
        
        self.__piece_sprites = [[None,] * 8 for i in range(8)]
        self.__destroyed_piece_sprites = {"white": list(), "black": list()}

        self.__key_input_buffer = [None, None]
        
        self.__board_coord_texts = []
        self.__build()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        
        self.__batch = self.create_batch()
        self.__piece_batch = self.create_batch()
        self.__selected_piece_batch = self.create_batch()

        # Obtém o tamanho do tabuleiro, que deve ser divisível por oito.
        self.__board_size = int(self.height * 0.9)

        while self.__board_size % 8 != 0:
            self.__board_size -= 1
        
        self.__square_size = self.__board_size // 8
        self.__destroyed_piece_size = self.__square_size * 0.5

        # Obtém a posição do tabuleiro.
        self.__board_y = (self.height - self.__board_size) // 2
        self.__board_x = self.__board_y

        # Obtém o tamanho e a posição do placar e seus elementos.
        score_board_area_x = self.__board_size + self.__board_x
        score_board_area_width = (self.width - score_board_area_x)
        
        self.__score_board_height = self.height - (self.__board_y * 2)
        self.__score_board_width = self.__score_board_height * 0.7
        self.__score_board_x = score_board_area_x + score_board_area_width / 2 - self.__score_board_width / 2
        self.__score_board_y = self.__board_y

        # Obtém o tamanho e a posição dos identificadores de jogador.
        player_width = self.__score_board_width * 0.14
        player_height = player_width
        player_y = self.__score_board_y + self.__score_board_height * 0.18

        white_player_x = self.__score_board_x + self.__score_board_width * 0.3 - player_width / 2
        black_player_x = self.__score_board_x + self.__score_board_width * 0.7 - player_width / 2

        # Obtém o tamanho e a posição do popup.
        popup_width = self.width * 0.45
        popup_height = popup_width * 0.7
        popup_x = self.width / 2 - popup_width / 2
        popup_y = self.height / 2 - popup_height / 2

        # Obtém o tamanho e a posição da seleção de promoção.
        promotion_selection_width = self.width * 0.7
        promotion_selection_height = promotion_selection_width * 0.4
        promotion_selection_x = self.width / 2 - promotion_selection_width / 2
        promotion_selection_y = self.height / 2 - promotion_selection_height / 2

        # Obtém o tamanho e a posição do controlador de replay.
        replay_controller_width = self.width * 0.2
        replay_controller_x = self.__score_board_x + self.__score_board_width / 2 - replay_controller_width / 2
        replay_controller_y = self.__score_board_y + self.__score_board_height * 0.915

        # Inicializa as imagens de peças.
        self.__load_piece_images(self.__square_size)
        self.__load_destroyed_piece_images()

        # Cria o plano de fundo.
        background_filename = application.paths.get_image("board", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria a imagem do placar.
        score_board_filename = application.paths.get_image("board", "score_board.png")
        score_board_image = self.load_image(score_board_filename, (self.__score_board_width, self.__score_board_height))

        self.__score_board_sprite = self.create_sprite(
            score_board_image, batch = self.__batch,
            x = self.__score_board_x, y = self.__score_board_y
        )  

        # Cria as imagens dos identificadores de jogador.
        white_player_filename = application.paths.get_image("board", "white.png")
        white_player_image = self.load_image(white_player_filename, (player_width, player_height))

        black_player_filename = application.paths.get_image("board", "black.png")
        black_player_image = self.load_image(black_player_filename, (player_width, player_height))

        self.__white_player_sprite = self.create_sprite(white_player_image, x = white_player_x, y = player_y)
        self.__black_player_sprite = self.create_sprite(black_player_image, x = black_player_x, y = player_y)  

        # Cria a borda do tabuleiro.
        self.__board_border = self.create_rectangle(
            self.__board_x - 2, self.__board_y - 2,
            self.__board_size + 4, self.__board_size + 4,
            batch = self.__batch, color = self.__BORDER_COLOR
        )

        # Cria os quadrados do tabuleiro e as peças.
        self.__square_shapes = []
        self.__piece_buttons = []
        
        for row in range(8):
            for column in range(8):
                x, y = self.__get_piece_image_pos(column, row)

                # Alterna a cor da casa, com base nas coordenadas.
                if (column + row) % 2 == 0:
                    color = self.__LIGHT_COLOR
                else: color = self.__DARK_COLOR

                square = self.create_rectangle(
                    x, y, self.__square_size, self.__square_size,
                    batch = self.__batch, color = color
                )
                self.__square_shapes.append(square)
                
        # Cria um popup para mensagens e um popup de confirmação.
        popup_filename = application.paths.get_image("general", "popup", "popup.png")

        cancel_button_filename = application.paths.get_image("general", "popup", "buttons", "cancel.png")
        activated_cancel_button_filename = application.paths.get_image("general", "popup", "buttons", "activated_cancel.png")
        
        confirm_button_filename = application.paths.get_image("general", "popup", "buttons", "confirm.png")
        activated_confirm_button_filename = application.paths.get_image("general", "popup", "buttons", "activated_confirm.png")

        self.__popup = Popup(
            self, popup_x, popup_y, (popup_width, popup_height), popup_filename
        )

        self.__confirmation_popup = ConfirmationPopup(
            self, popup_x, popup_y,
            (popup_width, popup_height),
            popup_filename, button_images = (
                (cancel_button_filename, activated_cancel_button_filename),
                (confirm_button_filename, activated_confirm_button_filename)
            )
        )

        # Cria widget para selecionar peças para eventuais promoções.
        promotion_images = []

        for piece_name in self.__PROMOTION_PIECES:
            promotion_images.append(application.paths.get_image("board", "pieces", "white_{}.png".format(piece_name)))

        self.__promotion_selection = PromotionSelection(
            self, promotion_selection_x, promotion_selection_y,
            (promotion_selection_width, promotion_selection_height),
            images = promotion_images
        )
        self.__promotion_selection.set_message("Escolha uma peça para promover o peão.")

        # Cria um controlador para um eventual replay.
        previous_button_filename = application.paths.get_image("general", "media_controller", "buttons", "previous.png")
        activated_previous_button_filename = application.paths.get_image("general", "media_controller", "buttons", "activated_previous.png")
        
        back_button_filename = application.paths.get_image("general", "media_controller", "buttons", "back.png")
        activated_back_button_filename = application.paths.get_image("general", "media_controller", "buttons", "activated_back.png")

        pause_button_filename = application.paths.get_image("general", "media_controller", "buttons", "pause.png")
        activated_pause_button_filename = application.paths.get_image("general", "media_controller", "buttons", "activated_pause.png")

        play_button_filename = application.paths.get_image("general", "media_controller", "buttons", "play.png")
        activated_play_button_filename = application.paths.get_image("general", "media_controller", "buttons", "activated_play.png")

        forward_button_filename = application.paths.get_image("general", "media_controller", "buttons", "forward.png")
        activated_forward_button_filename = application.paths.get_image("general", "media_controller", "buttons", "activated_forward.png")

        next_button_filename = application.paths.get_image("general", "media_controller", "buttons", "next.png")
        activated_next_button_filename = application.paths.get_image("general", "media_controller", "buttons", "activated_next.png")

        self.__replay_controller = MediaController(
            self, replay_controller_x, replay_controller_y, replay_controller_width,
            images = (
                (previous_button_filename, activated_previous_button_filename),
                (back_button_filename, activated_back_button_filename),
                (pause_button_filename, activated_pause_button_filename),
                (play_button_filename, activated_play_button_filename),
                (forward_button_filename, activated_forward_button_filename),
                (next_button_filename, activated_next_button_filename)
            )
        )

    def __create_board_coordinates(self):
        """
        Cria as letras e números ao lado do tabuleiro,
        correspondentes às linhas e colunas.
        """ 
        for column in range(8):
            x = self.__board_x + self.__square_size * 0.5 + self.__square_size * column
            y = self.__board_y + self.__board_size + self.height * 0.03

            text = self.__create_board_coord_text(chr(ord("A") + column), x, y)
            self.__board_coord_texts.append(text)

        for row in range(8):
            x = self.__board_x + self.__board_size + self.height * 0.03
            y = self.__board_y + self.__square_size * 0.5 + self.__square_size * row

            text = self.__create_board_coord_text(chr(ord("8") - row), x, y)
            self.__board_coord_texts.append(text)

    def __create_board_coord_text(self, string: str, x: int, y: int):
        """
        Cria o texto de uma coordenada do tabuleiro.
        """
        text = self.create_text(
            string, x, y, batch = self.__piece_batch,
            color = self.__COORD_TEXT_COLOR[0], font_size = self.width * 0.01,
            anchor_x = "center", anchor_y = "center"
        )
        return text

    def __create_destroyed_piece(self, piece):
        """
        Registra a dada peça destruída e cria sua imagem no placar.
        """
        color = "white" if piece.color.value == 0 else "black"
        image = self.__destroyed_piece_images[color][piece.name]

        sprite_list = self.__destroyed_piece_sprites[color]
        index = len(sprite_list)

        spacing_x = self.__destroyed_piece_size * 1.5
        spacing_y = self.__destroyed_piece_size * 1.1

        # Calcula a posição da peça destruída.
        if color == "black":
            x = self.__score_board_x + self.__score_board_width * 0.4 - self.__destroyed_piece_size
            x -= spacing_x if index >= 8 else 0
        else:
            x = self.__score_board_x + self.__score_board_width * 0.6
            x += spacing_x if index >= 8 else 0

        y = self.__score_board_y + self.__score_board_height * 0.3 + spacing_y * (index % 8)

        # Cria a imagem, adicionado-a à lista.
        sprite = self.create_sprite(
            image, batch = self.__piece_batch,
            x = x, y = y
        )
        sprite_list.append(sprite)

    def __create_target_shadow(self, row: int, column: int):
        """
        Cria uma sombra para uma dada casa do tabuleiro,
        identificando o destino da peça selecionada.
        """
        x, y = self.__get_piece_image_pos(column, row)
        
        self.__selected_target_shadow = self.create_rectangle(
            x, y, self.__square_size, self.__square_size,
            batch = self.__selected_piece_batch,
            color = self.__COORD_TEXT_COLOR[2][:3]
        )
        self.__selected_target_shadow.opacity = 50

    def __delete_board_coordinates(self):
        """
        Apaga os textos das coordenadas do tabuleiro.
        """
        for text in self.__board_coord_texts: text.delete()
        self.__board_coord_texts = []

    def __delete_destroyed_pieces(self):
        """
        Apaga o registro das peças destruídas,
        junto com suas imagens criadas.
        """
        for color, sprite_list in self.__destroyed_piece_sprites.items():
            for sprite in sprite_list: sprite.delete()
            self.__destroyed_piece_sprites[color] = []

    def __deselect_coordinates(self):
        """
        Desseleciona as coordenadas do tabuleiro.
        """
        for text in self.__board_coord_texts:
            text.color = self.__COORD_TEXT_COLOR[0]

    def __deselect_piece(self):
        """
        Desseleciona a peça, antes selecionada pelo teclado ou mouse. Caso
        a mesma tenha sido selecionada pelo mouse, ela voltará à posição original.
        """
        self.__moving_by_mouse = False
        self.__moving_by_keyboard = False
        
        self.__key_input_buffer = [None, None]
        self.__deselect_coordinates()

        if self.__selected_piece:
            self.__selected_piece.batch = self.__piece_batch
            self.__selected_piece.x = self.__selected_piece_position[0]
            self.__selected_piece.y = self.__selected_piece_position[1]

        if self.__selected_piece_shadow:
            self.__selected_piece_shadow.delete()

        if self.__selected_target_shadow:
            self.__selected_target_shadow.delete()

        self.__selected_target_shadow = None
            
        self.__selected_piece = None
        self.__selected_piece_shadow = None
        self.__selected_piece_index = None
        self.__selected_piece_position = None

    def __execute_replay_action(self, actions: list[bool]):
        """
        Executa uma funcionalidade do modo replay.
        """

        if actions[0]:
            self.__replay_velocity: float = 0
            
            if self.__replay_controller.is_playing():
                self.__replay_controller.switch_play_button()
            
            self.__replay_to(direction = -1)

        elif actions[1] and self.__replay_velocity > -1:
            self.__replay_velocity -= 0.1
    
        elif actions[2]:
            self.__replay_controller.switch_play_button()

        elif actions[3] and self.__replay_velocity < 1:
            self.__replay_velocity += 0.1

        elif actions[4]:
            self.__replay_velocity = 0
            
            if self.__replay_controller.is_playing():
                self.__replay_controller.switch_play_button()
            
            self.__replay_to(direction = 1)

    def __finish_game(self, color):
        """
        Encerra a partida, reproduzindo um som
        e definindo uma mensagem ao jogador.
        """
        self.__finished = True
        title = "JOGO ENCERRADO"

        # Salva uma imagem do estado final do tabuleiro.
        self.print_screen(
            region = (self.__board_x, self.__board_y, self.__board_size, self.__board_size),
            filename = self.get_application().paths.get_replay_image("{}.png".format(self.__game.id))
        )

        # Indica que houve uma derrota, no modo online.
        self.__online_defeat = self.__mode == self.ONLINE_MODE and color.value != self.__player

        # Conquista de usuário.
        if (self.__mode == self.ONLINE_MODE) and (not isinstance(color, bool)):
            if color.value == self.__player: self.get_application().add_achievement("Vida longa ao rei!", "Ganhou uma partida no modo online.")
            else: self.get_application().add_achievement("Dias frios e sombrios...", "Perdeu uma partida no modo online.")

        # Reproduz um som de vitória ou derrota.
        self.sound_player.stop_sound(all_ = True)
        
        if self.__online_defeat: self.sound_player.play_defeat_sound()
        else: self.sound_player.play_victory_sound()

        # Define uma mensagem para ser mostrado ao jogador.
        if self.__mode == self.ONLINE_MODE:
            message_type = self.__VICTORY_MESSAGES if color.value == self.__player else self.__DEFEAT_MESSAGES
            message = random.choice(message_type)

        elif isinstance(color, bool):
            message = "Empate por afogamento"

        else:
            message = "As peças {} ganharam o jogo!"
            message = message.format("brancas" if color.value == 0 else "pretas")
        
        self.__set_dialog_box_message(self.__popup, title, message)
            
    def __get_coord_on_board(self, x: int, y: int) -> Optional[tuple[int, int]]:
        """
        Retorna a posição da casa do tabuleiro
        em que o cursor se encontra no momento.
        """
        if not self.__is_mouse_on_board(x, y): return None
        
        step = self.__square_size

        # Percorre cada casa do tabuleiro.
        for index_x in range(8):
            for index_y in range(8):
                pos_x, pos_y = self.__get_piece_image_pos(index_x, index_y)

                # Verifica se o cursor está dentro dos limites da casa do tabuleiro em questão.
                if pos_x <= x <= pos_x + step and pos_y <= y <= pos_y + step:
                    return index_y, index_x
        return None

    def __get_piece_image_pos(self, x: int, y: int) -> tuple[int, int]:
        """
        Retorna a posição na tela da imagem de peça, dadas
        as coordenadas da mesma no tabuleiro.
        """
        pos_x = self.__board_x + self.__square_size * x
        pos_y = self.__board_y + self.__square_size * y
        return pos_x, pos_y

    def __is_key_input_buffer_full(self) -> bool:
        """
        Verifica se o buffer de teclas de coordenadas está cheio.
        """
        for key in self.__key_input_buffer:
            if key is None: return False
        return True

    def __is_mouse_on_board(self, x: int, y: int) -> bool:
        """
        Verifica se o cursor está dentro do campo do tabuleiro.
        """
        on_x = self.__board_x <= x <= self.__board_x + self.__board_size
        on_y = self.__board_y <= y <= self.__board_y + self.__board_size
        return on_x and on_y

    def __load_destroyed_piece_images(self):
        """
        Carrega as imagens das peças do jogo,
        salvando-as em um dicionário.
        """
        application = self.get_application()

        piece_names = ["king", "queen", "bishop", "knight", "pawn", "rook"]
        
        self.__destroyed_piece_images = {
            "black": dict(),
            "white": dict()
        }
        size = self.__destroyed_piece_size

        for color in self.__destroyed_piece_images.keys():
            for name in piece_names:
                piece_filename = application.paths.get_image("board", "pieces", "{}_{}.png".format(color, name))
                piece_image = self.load_image(piece_filename, (size, size))
                self.__destroyed_piece_images[color][name] = piece_image

    def __load_piece_images(self, size: int):
        """
        Carrega as imagens das peças do jogo,
        salvando-as em um dicionário.
        """
        application = self.get_application()

        piece_names = ["king", "queen", "bishop", "knight", "pawn", "rook"]
        
        self.__piece_images: dict = {
            "black": dict(),
            "white": dict()
        }

        for color in self.__piece_images.keys():
            for name in piece_names:
                piece_filename = application.paths.get_image("board", "pieces", "{}_{}.png".format(color, name))
                piece_image = self.load_image(piece_filename, (size, size))
                self.__piece_images[color][name] = piece_image

    def __move_piece(self, row: int, column: int, received: bool = False):
        """
        Move a peça selecionada para uma posição XY, se possível.
        """
  
        old_row, old_column = self.__selected_piece_index
        selected_piece = self.__game.get_piece(old_row, old_column)
        dest_piece = self.__game.get_piece(row, column)

        moving_by_keyboard = self.__moving_by_keyboard
        self.__deselect_piece()

        # Caso a coordenada seja igual à coordenada da peça selecionada,
        # o seu movimento será invalidado, reproduzindo um som de soltar a peça. 
        if row == old_row and column == old_column:
            return self.__play_dropping_piece_sound(selected_piece)

        # Impede que uma peça destrua outra peça da mesma cor.
        if dest_piece and dest_piece.color == selected_piece.color:
            return

        # Se a jogada ocorreu com sucesso, o tabuleiro é completamente atualizado.
        if self.__game.play(selected_piece, (row, column)):
            sent = True

            # Conquista de usuário.
            if moving_by_keyboard:
                self.get_application().add_achievement("Jogador raíz é outro nível!", "Realizou um movimento com qualquer peça utilizando o teclado.")

            if self.__first_movement and selected_piece.name == "knight":
                if not self.__mode == self.ONLINE_MODE or not received:
                    self.get_application().add_achievement("Na linha de Frente.", "Utilizou o cavalo como primeiro movimento do jogo.")

            self.__first_movement = False
            
            # Se o modo for online, envia a jogada para o outro jogador.
            if self.__mode == self.ONLINE_MODE and not received:
                sent = self.__movement_sender((old_row, old_column), (row, column))

            # Se havia peça na posição de destino, o som a ser reproduzido
            # será o de ataque, além de que a peça será registrada como
            # destruída. Caso contrário, será de movimento.
            if self.__game.attacked:
                
                # Se a peça atacada for o rei, outro som, de vitória ou derrota, será reproduzido.
                if dest_piece.name != "king": self.sound_player.play_attacking_sound()

                # Conquista de usuário.
                if self.__mode == self.ONLINE_MODE and not received:
                    self.get_application().add_achievement("A primeira de muitas...", "Eliminou uma peça do seu adversário no modo online.")
                    self.__killstreak += 1
                    
                    if self.__killstreak == 5:
                        self.get_application().add_achievement("Sangue nos olhos.", "Eliminou 5 peças em sequência.")
                else:
                    self.__killstreak = 0
                
            elif sent:
                self.sound_player.play_movement_sound()
    
            # Atualiza o tabuleiro na tela.
            self.__update_piece_sprites()
            self.__update_destroyed_piece_sprites()

        # Caso contrário, um som de movimento inválido será reproduzido.
        else: self.sound_player.play_invalid_movement_sound()
        
    def __play_dropping_piece_sound(self, piece):
        """
        Reproduz som de largar peça.
        """
        if piece.name == "bishop": self.sound_player.play_dropping_bishop_sound()
        elif piece.name == "king": self.sound_player.play_dropping_king_sound()
        elif piece.name == "knight": self.sound_player.play_dropping_knight_sound()
        elif piece.name == "pawn": self.sound_player.play_dropping_pawn_sound()
        elif piece.name == "queen": self.sound_player.play_dropping_queen_sound()
        elif piece.name == "rook": self.sound_player.play_dropping_rook_sound()

    def __play_getting_piece_sound(self, piece):
        """
        Reproduz som de selecionar peça.
        """
        if piece.name == "bishop": self.sound_player.play_getting_bishop_sound()
        elif piece.name == "king": self.sound_player.play_getting_king_sound() 
        elif piece.name == "knight": self.sound_player.play_getting_knight_sound()
        elif piece.name == "pawn": self.sound_player.play_getting_pawn_sound()
        elif piece.name == "queen": self.sound_player.play_getting_queen_sound()
        elif piece.name == "rook": self.sound_player.play_getting_rook_sound()

    def __replay_to(self, direction: int = 1):
        """
        Avança ou retrocede o jogo no modo replay.
        """
        try:
            # Altera o estado do tabuleiro.
            if direction >= 0: self.__game.next()
            else: self.__game.back()
                
            # Atualiza as sprites.
            self.__update_piece_sprites()
            self.__update_destroyed_piece_sprites()

        # Caso haja um erro, o mesmo será alertado.
        except: self.__replay_error = True

    def __select_coordinate(self, index: int, axis_y: bool = False, target: bool = False):
        """
        Seleciona uma coordenada do tabuleiro.
        """
        if not self.__board_coord_texts: return
        
        text = self.__board_coord_texts[index + (8 if axis_y else 0)]
        text.color = self.__COORD_TEXT_COLOR[2 if target else 1]

    def __select_piece(self, row: int, column: int, piece_on: bool = False, received: bool = False):
        """
        Seleciona uma peça do tabuleiro.
        """
        piece = self.__game.get_piece(row, column)
        player_color = self.__game.get_player().color

        # Verifica se a seleção é uma peça pertencente ao jogador da rodada.
        if not piece or piece.color != player_color:
            return self.__deselect_piece()

        # Se o modo for online, verifica se é a vez do jogador.
        if self.__mode == self.ONLINE_MODE and not received and piece.color.value != self.__player:
            return self.__deselect_piece()

        if not received: self.__play_getting_piece_sound(piece)
        sprite = self.__piece_sprites[row][column]

        # Troca o batch para que a peça fique na
        # frente de qualquer objeto da tela.
        if piece_on: sprite.batch = self.__selected_piece_batch
        
        self.__selected_piece = sprite
        self.__selected_piece_index = (row, column)
        self.__selected_piece_position = (sprite.x, sprite.y)

    def __select_piece_by_keyboard(self, row: int, column: int):
        """
        Define uma peça a ser selecionada, para que a mesma
        possa ser movida através do teclado.
        """
        if self.__moving_by_mouse: self.__deselect_piece()
        self.__moving_by_keyboard = True

        self.__key_input_buffer = [None, None]

        # Cria uma sombra para identificar a peça selecionada.
        x, y = self.__get_piece_image_pos(column, row)
        
        self.__selected_piece_shadow = self.create_rectangle(
            x, y, self.__square_size, self.__square_size,
            batch = self.__selected_piece_batch, color = (0, 0, 0)
        )
        self.__selected_piece_shadow.opacity = 50

        # Seleciona a peça.
        self.__select_piece(row, column)

    def __select_piece_by_mouse(self, row: int, column: int):
        """
        Define uma peça a ser selecionada, para que a mesma
        possa ser movida livremente com o cursor.
        """
        if self.__moving_by_keyboard: self.__deselect_piece()
        self.__moving_by_mouse = True
        self.__select_piece(row, column, True)
        
    def __set_dialog_box_message(self, widget: Popup, *message: str):
        """
        Define uma mensagem a ser mostrada em
        um widget de caixa de mensagem.
        """
        widget.set_message(
            self.width // 2, self.height // 2,
            *message, font_size = int(self.width * 0.012),
            line_spacing = int(self.width * 0.025)
        )

    def __set_promotion(self, index: int):
        """
        Define uma promoção para o peão.
        """
        self.sound_player.play_promotion_sound()
        
        piece_name = self.__PROMOTION_PIECES[index]
        self.__game.set_promotion(piece_name)
        self.__update_piece_sprites()

    def __update_destroyed_piece_sprites(self):
        """
        Atualiza o campo de peças destruídas.
        """
        self.__delete_destroyed_pieces()

        for piece in self.__game.destroyed_pieces:
            self.__create_destroyed_piece(piece)

    def __update_piece_sprites(self):
        """
        Atualiza o tabuleiro, criando toda as imagens das peças.
        """
        # Troca a opacidade da image, indicando qual o turno do jogador.
        if self.__mode != self.REPLAY_MODE:
            if self.__game.get_player().color.value == 0:
                self.__white_player_sprite.opacity = 255
                self.__black_player_sprite.opacity = 120
            else:
                self.__white_player_sprite.opacity = 120
                self.__black_player_sprite.opacity = 255
        else:
            self.__white_player_sprite.opacity = 255
            self.__black_player_sprite.opacity = 255
            
        for row in range(8):
            for column in range(8):
                
                # Deleta a imagem da peça antiga.
                sprite = self.__piece_sprites[row][column]

                if sprite: sprite.delete()
                self.__piece_sprites[row][column] = None

                # Obtém o objeto de peça do jogo.
                piece = self.__game.get_piece(row, column)
                if not piece: continue

                # Obtém a imagem da peça a ser utilizada.
                color = "white" if piece.color.value == 0 else "black"
                image = self.__piece_images[color][piece.name]

                # Calcula a posição da peça no tabuleiro e cria a imagem.
                x, y = self.__get_piece_image_pos(column, row)

                sprite = self.create_sprite(
                    image, batch = self.__piece_batch,
                    x = x, y = y
                )
                self.__piece_sprites[row][column] = sprite

    def __update_board_by_replay_animation(self):
        """
        Atualiza o tabuleiro no modo replay.
        """
        if not self.__replay_controller.is_playing(): return
        if self.__confirmation_popup.has_message(): return
        
        proportion = 2 - abs(self.__replay_velocity)

        # Verifica se chegou o momento de atualizar, com base no FPS do jogo.
        if self.__replay_frame_counter >= self.get_application().get_fps() * proportion:
            
            if self.__replay_velocity < 0: self.__replay_to(direction = -1)
            else: self.__replay_to(direction = 1)

            # Reproduz um som de movimento ou ataque.
            if not self.__game.replay_on_end:
                if self.__replay_velocity >= 0 and self.__game.attacked:
                    self.sound_player.play_attacking_sound()
                
                elif self.__replay_velocity >= 0:
                    self.sound_player.play_movement_sound()

            # Informa se o replay chegou ao fim, alterando o botão.
            if self.__game.replay_on_begin or self.__game.replay_on_end:
                if self.__replay_controller.is_playing():
                    self.__replay_controller.switch_play_button()
                    self.__replay_velocity = 0
                
            self.__replay_frame_counter = 0

        else: self.__replay_frame_counter += 1
        
    @property
    def LOCAL_MODE(self):
        return self.__LOCAL_MODE

    @property
    def ONLINE_MODE(self):
        return self.__ONLINE_MODE

    @property
    def REPLAY_MODE(self):
        return self.__REPLAY_MODE

    def set_board_coordinates(self, boolean: bool = True):
        """
        Mostra ou esconde as coordenadas do tabuleiro.
        """
        self.__delete_board_coordinates()
        if boolean: self.__create_board_coordinates()

    def set_new_game(self, game, mode: int, sender_func: Optional[Callable] = None, receiver_func: Optional[Callable] = None, is_first_player: Optional[bool] = False):
        """
        Define um novo jogo.
        """
        self.__finished = False
        
        self.__game = game
        self.__mode = mode
        self.__movement_sender = sender_func
        self.__movement_receiver = receiver_func

        self.__promotion_available = False
        
        self.__player = int(not is_first_player) # WHITE = 0; BLACK = 1
        self.__online_defeat = False

        self.__request_interval = self.get_application().get_fps() * 0.2
        self.__request_frame_counter = 0

        self.__replay_velocity = 0
        self.__replay_frame_counter = 0
        self.__replay_error = False

        # Reproduz som de início de jogo.
        self.sound_player.stop_sound(all_ = True)
        
        if self.get_application().is_defeated():
            self.sound_player.play_start_after_defeat_sound()
        else: self.sound_player.play_start_sound()

        # Define a reprodução automática ao iniciar o jogo no modo replay.
        if not self.__replay_controller.is_playing():
            self.__replay_controller.switch_play_button()

        self.__delete_destroyed_pieces()
        self.__update_piece_sprites()

        # Atributos de conquistas.
        self.__killstreak = 0
        self.__first_movement = True

        # Conquista de usuário.
        if self.__mode == self.LOCAL_MODE:
            self.get_application().add_achievement("Cara a cara, mano a mano!", "Iniciou uma partida local.")
            
        if self.__mode == self.ONLINE_MODE:
            self.get_application().add_achievement("Quebrando barreiras.", "Iniciou uma partida online (como host ou client).")

        if self.__mode == self.REPLAY_MODE:
            self.get_application().add_achievement("Voltando no tempo.", "Iniciou o replay de uma partida.")

    def on_close(self):
        """
        Evento para fechar a tela.
        """
        self.on_key_press(key.ESCAPE, None)

    def on_draw_screen(self, by_scheduler: bool = False):
        """
        Evento para desenhar a tela.
        """
        if self.__mode == self.REPLAY_MODE and self.__replay_error:
            return self.get_application().go_back("ERRO AO CARREGAR O REPLAY", "Parece que o arquivo está corrompido.")

        # Obtém o vencedor da partida, caso haja.
        winner = self.__game.get_winner() if self.__mode != self.REPLAY_MODE else None
        stalemated = self.__game.stalemated if self.__mode != self.REPLAY_MODE else False
        
        # Verifica se houve alguma jogada realizada pelo outro jogador.
        if not winner and self.__mode == self.ONLINE_MODE and self.__request_frame_counter == 0:
            movement = self.__movement_receiver()

            if movement:
                if movement[2] == 0:
                    self.__select_piece(*movement[0], received = True)
                    self.__move_piece(*movement[1], received = True)
                else: self.__set_promotion(movement[2] - 1)

        self.__request_frame_counter += 1
        self.__request_frame_counter %= self.__request_interval

        # Toca sempre uma música enquanto o usuário estiver na tela.
        if not self.sound_player.is_playing(any_ = True) and not self.__finished:

            # Verifica se o reprodutor está ativo.
            if not self.sound_player.is_muted()[1] and self.sound_player.get_volume()[1] > 0:
                if self.get_application().is_defeated(): self.sound_player.play_defeat_music()
                else: self.sound_player.play_music()

        # Atualiza o tabuleiro se estiver em modo replay.
        if self.__mode == self.REPLAY_MODE:
            self.__update_board_by_replay_animation()

        # Desenha os objetos na tela.   
        self.__background_image.blit(0, 0)
        self.__batch.draw()
        
        self.__white_player_sprite.draw()
        self.__black_player_sprite.draw()
        
        self.__piece_batch.draw()
        self.__selected_piece_batch.draw()

        if self.__mode == self.REPLAY_MODE:
            self.__replay_controller.draw()

        # Verifica se é necessário selecionar uma peça para promover um peão.
        if self.__mode != self.REPLAY_MODE:
            player_turn = self.__mode == self.LOCAL_MODE or self.__game.get_player().color.value == self.__player

            if self.__game.has_promotion() and player_turn:    
                self.__promotion_selection.draw()
                self.__promotion_available = True
            else: self.__promotion_available = False

        # Verifica se a partida finalizou.
        if not self.__finished and (winner or stalemated):
            self.__finish_game(winner or stalemated)
         
        self.__confirmation_popup.draw()
        self.__popup.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        super().on_key_press(symbol, modifiers)
        
        # Sai da tela do tabuleiro se o mesmo tiver sido finalizado.
        if self.__finished:
            self.__popup.delete_message()
            return self.get_application().go_back(defeat = self.__online_defeat)

        # Qualquer ação será realizada somente se não houver mensagem sendo mostrada na tela.
        if self.__confirmation_popup.has_message(): return

        # Verifica se é necessário realizar alguma promoção antes de qualquer ação.
        if self.__promotion_available: return
        
        piece_selected = self.__moving_by_keyboard or self.__moving_by_mouse

        # Caso o ESC seja apertado, significa que o usuário deseja sair
        # desta tela. Nesse caso, uma mensagem de confirmação deverá aparecer.
        if symbol == key.ESCAPE:
            if not self.__confirmation_popup.has_message():
                self.__deselect_piece()
                self.__set_dialog_box_message(self.__confirmation_popup, "Realmente deseja abandonar o jogo?")

        # Impede jogadas no modo replay.
        if self.__mode == self.REPLAY_MODE: return

        # Verifica se o usuário selecionou uma coluna
        if key.A <= symbol <= key.H and self.__key_input_buffer[1] is None:
            self.__key_input_buffer[1] = symbol - key.A
            self.__select_coordinate(self.__key_input_buffer[1], axis_y = False, target = self.__moving_by_keyboard)

        # Verifica se o usuário selecionou uma linha.
        elif key._1 <= symbol <= key._9 and not self.__key_input_buffer[1] is None and not self.__key_input_buffer[0]:
            self.__key_input_buffer[0] = 7 - (symbol - key._1)
            self.__select_coordinate(self.__key_input_buffer[0], axis_y = True, target = self.__moving_by_keyboard)

            # Se a peça já foi selecionado, o destino da peça será marcado.
            if self.__moving_by_keyboard: self.__create_target_shadow(*self.__key_input_buffer)

        # Se a tecla for ENTER e as coordenadas de destino foram selecionadas,
        # o movimento da peça selecionada será realizado.
        elif symbol in [key.ENTER, key.SPACE] and self.__is_key_input_buffer_full() and self.__moving_by_keyboard:
            self.__move_piece(*self.__key_input_buffer)
            
        # Se não, apaga os registros de teclas anteriores.
        else: self.__deselect_piece()

        # Seleciona uma peça a ser movida caso as coordenadas tenham sido selecionadas.
        if self.__is_key_input_buffer_full() and not self.__moving_by_keyboard:
            self.__select_piece_by_keyboard(*self.__key_input_buffer)
            
        return True

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        x, y = super().on_mouse_motion(*args)[0: 2]
        
        if self.__confirmation_popup.has_message():
            self.__confirmation_popup.check(x, y)

        if self.__mode == self.REPLAY_MODE:
            self.__replay_controller.check(x, y)

        # Atualiza a posição da imagem da peça selecionada.
        if self.__moving_by_mouse and self.__selected_piece:
            piece = self.__selected_piece
            piece.x = x - piece.width // 2
            piece.y = self.get_true_y_position(y - piece.height // 2, piece.height)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse pressionado e liberado.
        """
        # Sai da tela do tabuleiro se o mesmo tiver sido finalizado.
        if self.__finished:
            self.__popup.delete_message()
            return self.get_application().go_back(defeat = self.__online_defeat)

        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return

        # Verifica se é necessário realizar alguma promoção.
        if self.__promotion_available:
            results = self.__promotion_selection.check(x, y)

            # Verifica se o jogador selecionou uma peça para realizar a promoção.
            if any(results):
                index = results.index(True)
                self.__set_promotion(index)

                # Envia a promoção caso o jogo seja online.
                if self.__mode == self.ONLINE_MODE:
                    self.__movement_sender((0, 0), (0, 0), index + 1)

                # Conquista de usuário.
                self.get_application().add_achievement("Soldado promovido.", "Realizou a promoção de um peão em qualquer modo de jogo.")

            # Caso necessária a promoção, não será possível efetuar outra ação.
            return

        # Qualquer ação será realizada somente se não houver mensagem sendo mostrada na tela.
        if self.__confirmation_popup.has_message():
            cancel, confirm = self.__confirmation_popup.check(x, y)

            if not (confirm or cancel): return
            self.__confirmation_popup.delete_message()

            # Sai da tela, caso confirmado.
            if confirm: self.get_application().go_back()

        # Verifica se algum botão do controlador de replay foi pressionado.
        if self.__mode == self.REPLAY_MODE:
            buttons = self.__replay_controller.check(x, y)
            return self.__execute_replay_action(buttons)

        # Obtém a casa do tabuleiro através da posição do cursor.
        coords = self.__get_coord_on_board(x, y)
        if not coords: return

        row, column = coords
    
        # Seleciona uma peça do tabuleiro.
        if not self.__moving_by_mouse:
            self.__select_piece_by_mouse(row, column)

        # Move a peça de uma casa à outra.
        else: self.__move_piece(row, column)
