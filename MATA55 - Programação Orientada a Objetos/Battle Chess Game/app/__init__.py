from core import ChessGame

from .conn import Connection
from .data import achievements, paths, settings
from .screens import AchievementScreen, BoardScreen, HistoryScreen, HomeScreen, SettingsScreen, StartupScreen
from .sound import SoundPlayer
from pyglet import app
from pyglet import canvas
from pyglet import clock
from pyglet import image
from pyglet import window
from typing import Optional, Union
import os, time

class Application(window.Window):
    """
    Classe principal do aplicativo.
    """
    
    __FRAMES_PER_SECOND = 60
    
    __snow_config = {
        "current_particles": 200.0,
        "min_particles": 50,
        "max_particles": 200,
        "current_opacity": 150.0,
        "min_opacity": 30,
        "max_opacity": 150,
    }

    __decreasing_snowing = False
    
    def __init__(self, title: str, chess_game: ChessGame, winter_theme = False):
        super().__init__(
            caption = title,
            width = settings.size[0],
            height = settings.size[1],
            resizable = False
        )
        self.__center_window()

        self.__title = title

        if winter_theme:
            settings.defeated = True
        
        icon_filename = paths.get_image("icon.png")
        icon_image = image.load(icon_filename)
        self.set_icon(icon_image)
        
        self.paths = paths

        self.__address = settings.address
        self.__connection: Optional[Connection] = None

        self.__chess_game = chess_game
        self.__initialize()

    def __center_window(self):
        """
        Centraliza a janela da aplicação.
        """
        user_screen = canvas.Display().get_screens()[0]
        
        x = int(user_screen.width / 2 - self.width / 2)
        y = int(user_screen.height / 2 - self.height / 2)
        
        self.set_location(x, y)

    def __check_achivements(self):
        """
        Verifica se o usuário pode liberar determinadas
        conquistas obtidas ao iniciar o jogo.
        """
        self.add_achievement("Uma nova jornada começa...", "Iniciou o jogo pela primeira vez.")

        localtime = time.localtime()
        
        if localtime.tm_mday == 20 and localtime.tm_mon == 7:
            self.add_achievement("É dia de xadrez!!", "Iniciou o jogo no dia internacional do xadrez.") 

    def __decrease_snowing_animation(self, first_exec: bool = True):
        """
        Diminui gradualmente as partículas de neve.
        """
        if first_exec: self.__decreasing_snowing = True
        if not self.__decreasing_snowing: return
        
        changed = False

        # Diminui a quantidade de partículas.
        if self.__snow_config["current_particles"] > self.__snow_config["min_particles"]:
            interval = self.__snow_config["max_particles"] - self.__snow_config["min_particles"]
            self.__snow_config["current_particles"] -= interval * 0.005
            changed = True

        # Diminui a opacidade.
        if self.__snow_config["current_opacity"] > self.__snow_config["min_opacity"]:
            interval = self.__snow_config["max_opacity"] - self.__snow_config["min_opacity"]
            self.__snow_config["current_opacity"] -= interval * 0.005
            changed = True

        # Define as novas configurações.
        if not changed: return
        
        self.__home_screen.set_defeat_theme(
            settings.defeated,
            self.__snow_config["current_particles"],
            self.__snow_config["current_opacity"]
        )
        clock.schedule_once(lambda interval: self.__decrease_snowing_animation(False), 0.1)
        
    def __destroy_screens(self):
        """
        Destrói as telas criadas, liberando o espaço em memória.
        """
        self.__home_screen.free_memory()
        self.__board_screen.free_memory()
        self.__settings_screen.free_memory()
        self.__history_screen.free_memory()
        self.__achievement_screen.free_memory()

    def __initialize(self):
        """
        Inicializa a aplicação.
        """
        self.__initializing = True
        
        # Mostra uma tela de inicialização, enquanto o aplicativo inicializa.
        self.__current_screen = StartupScreen(self)
        clock.schedule_interval(self.on_draw, 1 / self.get_fps())

        # Inicializa o reprodutor de sons.
        self.__sound_player = SoundPlayer(settings.volume, settings.muted)

        # Inicializa as telas do jogo.
        clock.schedule_once(lambda interval: self.__initialize_screens(), 1 / self.get_fps() * 5)

    def __initialize_screens(self):
        """
        Inicializa todas as telas do jogo.
        """
        self.__home_screen = HomeScreen(self)
        self.__home_screen.set_play_function(self.__start_game)
        self.__home_screen.set_settings_function(self.__show_settings_screen)
        self.__home_screen.set_history_function(self.__show_history_screen)
        self.__home_screen.set_achievement_function(self.__show_achievement_screen)
        
        self.__home_screen.set_defeat_theme(
            settings.defeated,
            self.__snow_config["max_particles"],
            self.__snow_config["max_opacity"]
        )
        
        self.__board_screen = BoardScreen(self)
        self.__board_screen.set_board_coordinates(True)

        self.__history_screen = HistoryScreen(self)
        self.__history_screen.set_replay_function(self.__start_replay)
        
        self.__settings_screen = SettingsScreen(self)
        self.__achievement_screen = AchievementScreen(self)

        if self.__initializing:
            self.__current_screen.free_memory()
            self.__initializing = False

        self.__current_screen = self.__home_screen
        self.__check_achivements()

    def __finish_online_match_by_error(self) -> bool:
        """
        Encerra a partida online informando que houve um erro.
        """
        self.go_back()
        self.__current_screen.set_popup_message("Conexão perdida.")

        return False

    def __get_movement(self) -> Union[tuple[tuple, tuple, int], bool]:
        """
        Retorna a jogada realizada pelo outro jogador, se houver.
        """
        if self.__connection.is_connected():
            return self.__connection.recv()

        return self.__finish_online_match_by_error()

    def __send_movement(self, origin: list[int], dest: list[int], promotion: int = 0) -> bool:
        """
        Envia a jogada realizada para o outro jogador.
        """
        if self.__connection.is_connected():
            self.__connection.send(origin, dest, promotion = promotion)
            return True

        return self.__finish_online_match_by_error()
            
    def __show_achievement_screen(self):
        """
        Alterna para a tela de conquistas.
        """
        achievement_count = 0
        
        for achievement_info in achievements.get_achievements():
            self.__achievement_screen.add_achievement(*achievement_info)
            achievement_count += 1

        message = "Conquista" if achievement_count == 1 else "Conquistas"
        self.set_message_to_title("{} {}".format(achievement_count, message))
            
        self.__current_screen = self.__achievement_screen

    def __show_history_screen(self):
        """
        Alterna para a tela de histórico de partidas.
        """
        self.__history_screen.set_history(self.__chess_game.get_history())
        self.__current_screen = self.__history_screen

    def __show_settings_screen(self):
        """
        Alterna para a tela de configurações.
        """
        self.__current_screen = self.__settings_screen
        self.set_message_to_title("Configurações")

    def __start_connection(self, host_mode: bool) -> bool:
        """
        Inicia uma conexão com outro jogador.
        """
        self.__connection = Connection(settings.address, host_mode)
        self.__connection.connect(timeout_in_seconds = 0.3, attempts = 10)
        
        return self.__connection.is_connected()
        
    def __start_game(self, selection: int):
        """
        Inicia o jogo, dada uma seleção (local ou online).
        """
        self.__chess_game.new_game("LOCAL" if selection == 1 else "ONLINE")
        
        # Inicia o jogo localmente.
        if selection == 1: return self.__start_local_game()

        # Inicia o jogo online.
        self.__current_screen.set_popup_message("Procurando por um jogador na rede...", "Por favor, aguarde.")
        clock.schedule_once(lambda interval: self.__start_online_game(selection), 1 / self.get_fps() * 3)

    def __start_local_game(self):
        """
        Inicia o jogo no modo local.
        """
        self.__home_screen.set_defeat_theme(self.is_defeated())
        self.__decrease_snowing_animation()

        self.__sound_player.stop_sound(all_ = True)
        
        self.__board_screen.set_new_game(self.__chess_game, self.__board_screen.LOCAL_MODE)
        self.__current_screen = self.__board_screen
        self.set_message_to_title("Jogo Local")

    def __start_online_game(self, selection: int):
        """
        Inicia o jogo no modo online.
        """
        # Tentar estabelecer uma conexão.
        if not self.__start_connection(selection == 2):
            return self.__current_screen.set_popup_message("Infelizmente, não foi possível conectar.", "Por favor, verique a sua conexão.")

        self.__current_screen.set_popup_message(None)
        self.__sound_player.stop_sound(all_ = True)
        
        self.__home_screen.set_defeat_theme(self.is_defeated())
        self.__decrease_snowing_animation()

        # Inicia o jogo online.
        self.__board_screen.set_new_game(
            self.__chess_game, self.__board_screen.ONLINE_MODE,
            self.__send_movement, self.__get_movement, selection == 2
        )
        self.__current_screen = self.__board_screen
        self.set_message_to_title("Jogo Online")

    def __start_replay(self, game_id: str):
        """
        Inicia o jogo no modo replay.
        """       
        try: self.__chess_game.start_replay(game_id)
        except: return self.go_back("ERRO AO CARREGAR O REPLAY", "Parece que o arquivo está corrompido.")

        self.__sound_player.stop_sound(all_ = True)
        
        self.__board_screen.set_new_game(self.__chess_game, self.__board_screen.REPLAY_MODE)
        self.__current_screen = self.__board_screen
        self.set_message_to_title("Replay da Partida \"#{}\"".format(game_id))

    def add_achievement(self, title: str, description: str):
        """
        Adiciona uma nova conquista de usuário.
        """
        if achievements.add_achievement(title, description):
            self.__current_screen.set_achievement(title)
  
    def get_fps(self) -> float:
        """
        Retorna a taxa de frames por segundo do aplicativo.
        """
        return self.__FRAMES_PER_SECOND

    def get_ip_address(self) -> tuple[str, int]:
        """
        Retorna o endereço IP do usuário.
        """
        return self.__address[0], self.__address[1]

    def get_sound_player(self) -> SoundPlayer:
        """
        Retorna o reprodutor de som.
        """
        return self.__sound_player

    def go_back(self, *error_message: str, **kwargs):
        """
        Volta uma tela para trás.
        """
        self.set_caption(self.__title)

        # Interrompe a reprodução de qualquer som ativo da partida finalizada.
        if self.__current_screen is self.__board_screen:
            self.__sound_player.stop_sound(all_ = True)

        # Define um tema de derrota, caso o jogador tenha perdido.
        if self.__current_screen is self.__board_screen:
            settings.defeated = kwargs.get("defeat", self.is_defeated())

        self.__decreasing_snowing = False
        
        self.__home_screen.set_defeat_theme(
            self.is_defeated(),
            self.__snow_config["max_particles"],
            self.__snow_config["max_opacity"],
        )
        self.__snow_config["current_particles"] = self.__snow_config["max_particles"]
        self.__snow_config["current_opacity"] = self.__snow_config["max_opacity"]

        # Encerra a conexão com o outro jogador, caso exista.
        if self.__connection:
            self.__connection.close()
            self.__connection = None

        # Encerra qualquer jogo aberto.
        self.__chess_game.close()

        # Retorna para a tela de menu, mostrando uma mensagem de erro, caso haja.
        if error_message: self.__home_screen.set_popup_message(*error_message)
        self.__current_screen = self.__home_screen

    def is_defeated(self) -> bool:
        """
        Verifica se o jogador foi derrotado.
        """
        return settings.defeated
    
    def on_close(self):
        """
        Evento para fechar a janela.
        """
        self.__current_screen.on_close()

    def on_draw(self, interval: Union[float, None] = None):
        """
        Evento para desenhar a tela.
        """
        self.clear()
        self.__current_screen.on_draw(not interval is None)

    def on_key_press(self, *args):
        """
        Evento de tecla pressionada.
        """
        self.__current_screen.on_key_press(*args)

    def on_mouse_drag(self, *args):
        """
        Evento de botão do mouse pressionado.
        """
        self.__current_screen.on_mouse_drag(*args)

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        self.__current_screen.on_mouse_motion(*args)

    def on_mouse_press(self, *args):
        """
        Evento de botão do mouse pressionado e movendo.
        """
        self.__current_screen.on_mouse_press(*args)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse liberado.
        """
        self.__current_screen.on_mouse_release(*args)

    def on_mouse_scroll(self, *args):
        """
        Evento de scroll do mouse.
        """
        self.__current_screen.on_mouse_scroll(*args)

    def resize(self, width: int, height: int):
        """
        Altera o tamanho da tela do aplicativo.
        """
        if width == self.width and height == self.height: return
        
        self.width = width
        self.height = height
        
        self.__center_window()
        self.__destroy_screens()
        self.__initialize_screens()

    def run(self):
        """
        Inicia a execução do aplicativo.
        """
        app.run()    

    def save_settings(self):
        """
        Salva todas as configurações atuais do aplicativo serão salvas.
        """
        settings.address = self.__address
        settings.size = [self.width, self.height]
        settings.volume = self.__sound_player.get_volume()
        settings.muted = self.__sound_player.is_muted()

    def set_ip_address(self, address: str, port: int):
        """
        Define um endereço IP para o usuário.
        """
        self.__address[0] = address
        self.__address[1] = int(port)

    def set_message_to_title(self, message: str):
        """
        Define uma mensagem ao lado do título do jogo.
        """
        self.set_caption(self.__title + " - " + message)
