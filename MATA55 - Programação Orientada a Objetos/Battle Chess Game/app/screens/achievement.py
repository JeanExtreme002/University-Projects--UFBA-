from .screen import Screen
from .util import Scrollbar
from pyglet.window import mouse, key

class AchievementScreen(Screen):
    """
    Classe para criar uma tela de histórico de partidas.
    """
    
    def __init__(self, application):
        super().__init__(application)
        self.__build()

        self.__titles = []
        self.__moving = False
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        
        self.__batch = self.create_batch()
        self.__text_batch = self.create_batch()

        # Obtém o tamanho e a posição das conquistas.
        self.__achievement_width = self.width * 0.7
        self.__achievement_height = self.__achievement_width * 0.15
        self.__achievement_x = self.width / 2 - self.__achievement_width / 2
        self.__achievement_vertical_margin = self.height * 0.1

        # Obtém o tamanho e a posição do scrollbar.
        self.__scrollbar_width = self.width * 0.005
        self.__scrollbar_height = self.height - self.__achievement_vertical_margin * 2
        self.__scrollbar_x = self.width * 0.9
        self.__scrollbar_y = self.__achievement_vertical_margin

        self.__start = self.__achievement_vertical_margin
        self.__end = self.__achievement_vertical_margin
        self.__velocity = self.__achievement_height * 0.3
        self.__scrollbar_value = 0
    
        # Cria o plano de fundo.
        background_filename = application.paths.get_image("achievement", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

        # Cria a barra de rolagem.
        self.__scrollbar = Scrollbar(
            self, self.__scrollbar_x, self.__scrollbar_y,
            (self.__scrollbar_width, self.__scrollbar_height),
            bar_height = self.__scrollbar_height * 0.1
        )

        # Carrega a imagem de conquista.
        self.__achievement_filename = application.paths.get_image("achievement", "achievement.png")
        self.__achievement_image = self.load_image(self.__achievement_filename, (self.__achievement_width, self.__achievement_height))
        self.__achievements = []

    def __move_by_mouse(self, x: int, y: int):
        """
        Move a lista através do mouse, utilizando a barra de rolagem.
        """
        moved = self.__scrollbar.move_by_mouse(x, y, ignore_x = self.__moving)
        page_y = self.__scrollbar.get_value() - self.__achievement_vertical_margin
        
        if moved:
            self.__moving = True
            self.__move_list(self.__start + page_y)

    def __move_list(self, velocity: int = 1):
        """
        Move a lista de conquistas verticalmente.
        """
        if velocity > 0 and self.__end + self.__achievement_height <= (self.height - self.__achievement_vertical_margin): return
        if velocity < 0 and self.__start >= self.__achievement_vertical_margin: return
        
        self.__end += velocity * -1
        self.__start += velocity * -1
    
        for achievement in self.__achievements:
            for widget in achievement:
                widget.y += velocity

    def add_achievement(self, title: str, description: str, date: str):
        """
        Adiciona mais uma conquista para a lista.
        """
        if title in self.__titles: return

        self.__end += (self.__achievement_height * 1.4) if self.__titles else 0
        self.__scrollbar_value += (self.__achievement_height * 1.4)
        
        self.__titles.append(title)
        
        background = self.create_sprite(
            self.__achievement_image, x = self.__achievement_x,
            y = self.__end, batch = self.__batch
        )
        
        title = self.create_text(
            title, self.__achievement_x + self.__achievement_width * 0.2,
            self.__end + self.__achievement_height * 0.3,
            anchor_x = "left", anchor_y = "center",
            batch = self.__text_batch,
            font_name = "Comic Sans MS",
            font_size = self.width * 0.017,
            color = (255, 255, 255, 255)
        )  

        description = self.create_text(
            description, self.__achievement_x + self.__achievement_width * 0.2,
            self.__end + self.__achievement_height * 0.7,
            anchor_x = "left", anchor_y = "center",
            batch = self.__text_batch,
            font_size = self.width * 0.012,
            color = (235, 235, 235, 255)
        )

        date = self.create_text(
            date, self.__achievement_x + self.__achievement_width * 0.97,
            self.__end + self.__achievement_height * 0.3,
            anchor_x = "right", anchor_y = "center",
            batch = self.__text_batch,
            font_size = self.width * 0.01,
            color = (245, 245, 245, 255)
        )

        self.__scrollbar.set_max_value(self.__scrollbar_value - self.height * 0.5)
        self.__achievements.append([background, title, description, date])

    def on_draw_screen(self, by_scheduler: bool = False):
        """
        Evento para desenhar a tela.
        """
        self.__background_image.blit(0, 0)
        self.__batch.draw()
        self.__text_batch.draw()
        self.__scrollbar.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        super().on_key_press(symbol, modifiers)
        
        # Caso o ESC seja apertado, significa que o usuário deseja sair desta tela.
        if symbol == key.ESCAPE:
            self.get_application().go_back()
        
        # Caso uma das setas verticais seja apertada, a lista será movida verticalmente.
        elif symbol == key.UP:
            self.__scrollbar.move(-self.__velocity)
            self.__move_list(-self.__velocity)
            
        elif symbol == key.DOWN:
            self.__scrollbar.move(self.__velocity)
            self.__move_list(self.__velocity)

        return True

    def on_mouse_press(self, *args):
        """
        Evento de botão do mouse pressionado.
        """
        x, y, mouse_button = super().on_mouse_press(*args)[0: 3]
        if mouse_button == mouse.LEFT: self.__move_by_mouse(x, y)

    def on_mouse_drag(self, *args):
        """
        Evento de botão do mouse pressionado e movendo.
        """
        x, y, mouse_button = super().on_mouse_drag(*args)[0: 3]
        if mouse_button == mouse.LEFT: self.__move_by_mouse(x, y)

    def on_mouse_motion(self, *args):
        """
        Evento de movimentação do cursor.
        """
        x, y, mouse_button = super().on_mouse_motion(*args)[0: 3]
        self.__scrollbar.check(x, y)

    def on_mouse_release(self, *args):
        """
        Evento de botão do mouse pressionado.
        """
        x, y, mouse_button = super().on_mouse_release(*args)[0: 3]
        if mouse_button == mouse.LEFT: self.__moving = False

    def on_mouse_scroll(self, *args):
        """
        Evento de scroll do mouse.
        """
        x, y, scroll_y = super().on_mouse_scroll(*args)[0: 3]
        self.__scrollbar.move(-self.__velocity * scroll_y)
        self.__move_list(-self.__velocity * scroll_y)
