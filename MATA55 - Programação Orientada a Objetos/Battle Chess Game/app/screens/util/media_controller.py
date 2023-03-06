from .button import Button
from .highlighted_widget import HighlightedWidget
from .widget_group import WidgetGroup
from typing import Optional

class MediaController(HighlightedWidget):
    """
    Classe para criar um popup com uma mensagem na tela.
    """
    def __init__(self, screen, x: int, y: int, width: int, images: list[str], widget_group: Optional[WidgetGroup] = None):
        super().__init__(
            screen, x, y, [width, int(width * 0.08)],
            opacity = 200,
            fill = int(width * 0.08 * 0.2),
            widget_group = widget_group
        )
        
        self.__images = images
        self.__is_playing = True
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        self.__widget_group = WidgetGroup()
        
        margin = self.width * 0.1
        spacing = self.width * 0.1
        
        x = self.x + margin

        self.__previous_button = Button(
            self.screen, x + (self.height + spacing) * 0, self.y, (self.height, self.height),
            images = self.__images[0], widget_group = self.__widget_group
        )
        self.__back_button = Button(
            self.screen, x + (self.height + spacing) * 1, self.y, (self.height, self.height),
            images = self.__images[1], widget_group = self.__widget_group
        )
        self.__play_button = Button(
            self.screen, x + (self.height + spacing) * 2, self.y, (self.height, self.height),
            images = self.__images[2], widget_group = self.__widget_group
        )
        self.__forward_button = Button(
            self.screen, x + (self.height + spacing) * 3, self.y, (self.height, self.height),
            images = self.__images[4], widget_group = self.__widget_group
        )
        self.__next_button = Button(
            self.screen, x + (self.height + spacing) * 4, self.y, (self.height, self.height),
            images = self.__images[5], widget_group = self.__widget_group
        )

    def check(self, x: int, y: int) -> tuple[bool, bool, bool, bool, bool]:
        """
        Verifica se o cursor se encontra na posição de um dos botões.
        """
        previous_button = self.__previous_button.check(x, y)
        back_button = self.__back_button.check(x, y)
        play_button = self.__play_button.check(x, y)
        forward_button = self.__forward_button.check(x, y)
        next_button = self.__next_button.check(x, y)
        
        return previous_button, back_button, play_button, forward_button, next_button
        
    def draw(self):
        """
        Desenha o widget na tela.
        """
        super().draw()
        self.__widget_group.draw()

    def is_playing(self) -> bool:
        """
        Verifica se o botão de reprodução foi ativado.
        """
        return self.__is_playing

    def switch_play_button(self):
        """
        Alterna entre o botão de pause e de reprodução.
        """
        self.__is_playing = not self.__is_playing
        
        image = self.__images[2 + (0 if self.__is_playing else 1)]
        self.__play_button.change_image(image)
