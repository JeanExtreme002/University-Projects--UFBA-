from .screen import Screen
from .util import Button, ConfirmationPopup, Popup, Slide, WidgetGroup
from pyglet.window import mouse, key
from typing import Callable
import webbrowser

class HomeScreen(Screen):
    """
    Classe para criar uma tela de menu principal.
    """
    
    def __init__(self, application):
        super().__init__(application)
        
        self.__message = None
        self.__key_buffer = []
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        self.__batch = self.create_batch()
        self.__widget_group = WidgetGroup()

        # Obtém tamanho e posição da imagem background.
        background_x, background_y = self.width * 0.3, 0
        background_width = self.width - background_x
        background_height = self.height

        # Obtém o tamanho da barra lateral.
        sidebar_width = background_x - 2
        sidebar_height = self.height

        # Obtém tamanho e posição da logo.
        logo_width = sidebar_width * 0.70
        logo_height = logo_width * 0.77
        
        logo_x = sidebar_width * 0.5 - logo_width * 0.5
        logo_y = self.height * 0.02

        # Obtém o tamanho e posição dos botões maiores, que serão dispostos verticalmente.
        large_button_width = sidebar_width * 0.60
        large_button_height = large_button_width * 0.39
        large_button_spacing = large_button_height * 0.2
        
        large_button_x = sidebar_width * 0.5 - large_button_width * 0.5
        first_large_button_y = self.height * 0.35

        # Obtém o tamanho e posição dos botões menores, que serão dispostos horizontalmente.
        small_button_width = (large_button_width * 0.8) / 3
        small_button_height = small_button_width * 0.75
        small_button_spacing = large_button_width * 0.1

        first_small_button_x = large_button_x
        small_button_y = sidebar_height * 0.9 - small_button_height

        # Obtém o tamanho e a posição do popup.
        popup_width = self.width * 0.45
        popup_height = popup_width * 0.7
        popup_x = self.width / 2 - popup_width / 2
        popup_y = self.height / 2 - popup_height / 2

        # Carrega e cria a imagem da barra lateral.
        sidebar_filename = application.paths.get_image("home", "sidebar.png")
        self.__sidebar_image = self.load_image(sidebar_filename, (sidebar_width, sidebar_height))
    
        # Carrega e cria a imagem de logo.
        logo_filename = application.paths.get_image("home", "logo.png")
        logo_image = self.load_image(logo_filename, (logo_width, logo_height))
        self.__logo_sprite = self.create_sprite(logo_image, batch = self.__batch, x = logo_x, y = logo_y)

        # Carrega a imagem dos botões de jogar.
        play_button_1_filename = application.paths.get_image("home", "buttons", "play_local.png")
        activated_play_button_1_filename = application.paths.get_image("home", "buttons", "activated_play_local.png")
        
        play_button_2_filename = application.paths.get_image("home", "buttons", "play_as_host.png")
        activated_play_button_2_filename = application.paths.get_image("home", "buttons", "activated_play_as_host.png")
        
        play_button_3_filename = application.paths.get_image("home", "buttons", "play_as_client.png")
        activated_play_button_3_filename = application.paths.get_image("home", "buttons", "activated_play_as_client.png")

        # Carrega a imagem dos botões de histórico, conquistas e configurações.
        history_button_filename = application.paths.get_image("home", "buttons", "history.png")
        activated_history_button_filename = application.paths.get_image("home", "buttons", "activated_history.png")

        achievement_button_filename = application.paths.get_image("home", "buttons", "achievement.png")
        activated_achievement_button_filename = application.paths.get_image("home", "buttons", "activated_achievement.png")

        settings_button_filename = application.paths.get_image("home", "buttons", "settings.png")
        activated_settings_button_filename = application.paths.get_image("home", "buttons", "activated_settings.png")

        # Cria os botões de jogar.
        self.__play_button_1 = Button(
            self, large_button_x, first_large_button_y + (large_button_height + large_button_spacing) * 0,
            (large_button_width, large_button_height), (play_button_1_filename, activated_play_button_1_filename),
            widget_group = self.__widget_group
        )

        self.__play_button_2 = Button(
            self, large_button_x, first_large_button_y + (large_button_height + large_button_spacing) * 1,
            (large_button_width, large_button_height), (play_button_2_filename, activated_play_button_2_filename),
            widget_group = self.__widget_group
        )

        self.__play_button_3 = Button(
            self, large_button_x, first_large_button_y + (large_button_height + large_button_spacing) * 2,
            (large_button_width, large_button_height), (play_button_3_filename, activated_play_button_3_filename),
            widget_group = self.__widget_group
        )

        # Cria os botões de histórico, conquistas e configurações.
        self.__history_button = Button(
            self, first_small_button_x + (small_button_width + small_button_spacing) * 0,
            small_button_y, (small_button_width, small_button_height),
            (history_button_filename, activated_history_button_filename),
            widget_group = self.__widget_group
        )

        self.__achievement_button = Button(
            self, first_small_button_x + (small_button_width + small_button_spacing) * 1,
            small_button_y, (small_button_width, small_button_height),
            (achievement_button_filename, activated_achievement_button_filename),
            widget_group = self.__widget_group
        )

        self.__settings_button = Button(
            self, first_small_button_x + (small_button_width + small_button_spacing) * 2,
            small_button_y, (small_button_width, small_button_height),
            (settings_button_filename, activated_settings_button_filename),
            widget_group = self.__widget_group
        )

        # Carrega a imagem de background.
        background_filenames = application.paths.get_image_list("home", "background", shuffle = True)
        
        self.__background = Slide(
            self, background_x, background_y,
            (background_width, background_height),
            background_filenames,
            widget_group = self.__widget_group
        )

        # Cria um popup para mensagens e um popup de confirmação.
        popup_filename = application.paths.get_image("general", "popup", "popup.png")

        cancel_button_filename = application.paths.get_image("general", "popup", "buttons", "cancel.png")
        activated_cancel_button_filename = application.paths.get_image("general", "popup", "buttons", "activated_cancel.png")
        
        confirm_button_filename = application.paths.get_image("general", "popup", "buttons", "confirm.png")
        activated_confirm_button_filename = application.paths.get_image("general", "popup", "buttons", "activated_confirm.png")

        self.__popup = Popup(
            self, popup_x, popup_y, (popup_width, popup_height),
            popup_filename, widget_group = self.__widget_group
        )

        self.__confirmation_popup = ConfirmationPopup(
            self, popup_x, popup_y, (popup_width, popup_height), popup_filename,
            button_images = (
                (cancel_button_filename, activated_cancel_button_filename),
                (confirm_button_filename, activated_confirm_button_filename)
            ),
            widget_group = self.__widget_group
        )

    def __check_buttons(self, x: int, y: int):
        """
        Retorna os botões no qual o cursor se encontra.
        """
        play_1 = self.__play_button_1.check(x, y)
        play_2 = self.__play_button_2.check(x, y)
        play_3 = self.__play_button_3.check(x, y)
        
        history = self.__history_button.check(x, y)
        achievement = self.__achievement_button.check(x, y)
        settings = self.__settings_button.check(x, y)
        
        return play_1, play_2, play_3, history, achievement, settings

    def __run_easter_egg(self):
        """
        Executa a ação de easter egg.
        """
        url = "https://www.youtube.com/watch?v=bTS9XaoQ6mg"
        webbrowser.open(url)
        
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

    def set_popup_message(self, *message: str):
        """
        Define uma mensagem a ser mostrada na tela.
        """
        if not message[0]: return self.__popup.delete_message()
        self.__set_dialog_box_message(self.__popup, *message)

    def set_achievement_function(self, func: Callable):
        """
        Define uma função para o botão de conquistas.
        """
        self.__achievement_function = func

    def set_history_function(self, func: Callable):
        """
        Define uma função para o botão de histórico de partidas.
        """
        self.__history_function = func

    def set_play_function(self, func: Callable):
        """
        Define uma função para o botão de jogar.
        """
        self.__play_function = func

    def set_settings_function(self, func: Callable):
        """
        Define uma função para o botão de configurações.
        """
        self.__settings_function = func

    def on_draw_screen(self, by_scheduler: bool = False):
        """
        Evento para desenhar a tela.
        """
        # Realiza a animação de slide somente se a tela foi atualizada
        # pelo agendador. Dessa forma, é possível manter uma velocidade
        # constante, através do FPS da tela, definido no agendador.
        if by_scheduler: self.__background.next()

        # Toca sempre uma música enquanto o usuário estiver na tela.
        if not self.sound_player.is_playing(any_ = True):
            if self.get_application().is_defeated(): self.sound_player.play_defeat_music()
            else: self.sound_player.play_music()
        
        self.__sidebar_image.blit(0, 0)
        
        self.__batch.draw()
        self.__widget_group.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        super().on_key_press(symbol, modifiers)
        
        # Caso o ESC seja apertado, significa que o usuário deseja sair desta tela.
        if symbol == key.ESCAPE:
            self.__key_buffer = []
            
            message = self.__popup.has_message()
            confirmation = self.__confirmation_popup.has_message()

            # Mostra uma mensagem de confirmação.
            if not (message or confirmation):
                self.__set_dialog_box_message(self.__confirmation_popup, "Você realmente deseja sair?")
            if message:
                self.__popup.delete_message()

        # Conquista de usuário.
        self.__key_buffer += chr(symbol) if symbol <= 512 else "#"
        string = "".join(self.__key_buffer).upper()
        
        if not string in "XADREZ" and not string in "CHESS":
            self.__key_buffer = self.__key_buffer[-1:]

        if string in ["XADREZ", "CHESS"]:
            self.get_application().add_achievement("LMAO", "Descobriu a EASTER EGG no menu do jogo!")
            self.__run_easter_egg()
                
        return True

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        x, y = super().on_mouse_motion(*args)[0: 2]
        self.__check_buttons(x, y)

        if self.__confirmation_popup.has_message():
            self.__confirmation_popup.check(x, y)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse pressionado e liberado.
        """
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button != mouse.LEFT: return
            
        play_button_1, play_button_2, play_button_3, history, achievement, settings = self.__check_buttons(x, y)

        # Qualquer ação será realizada somente se não houver mensagens sendo mostrada na tela.
        if self.__popup.has_message():
            return self.__popup.delete_message()

        if self.__confirmation_popup.has_message():
            cancel, confirm = self.__confirmation_popup.check(x, y)

            if confirm: self.get_application().close()
            elif cancel: self.__confirmation_popup.delete_message()
            return

        # Verifica se algum botão de jogar foi apertado.
        if play_button_1: self.__play_function(1)
        elif play_button_2: self.__play_function(2)
        elif play_button_3: self.__play_function(3)
        elif settings: self.__settings_function()
        elif history: self.__history_function()
        elif achievement: self.__achievement_function() 
