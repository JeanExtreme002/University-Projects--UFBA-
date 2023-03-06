from .button import Button
from .highlighted_widget import HighlightedWidget
from .widget_group import WidgetGroup
from typing import Optional

class PromotionSelection(HighlightedWidget):
    """
    Classe para criar um popup de seleção para promoções.
    """
    def __init__(self, screen, x: int, y: int, size: list[int], images: list[str], widget_group: Optional[WidgetGroup] = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)
        
        self.__images = images
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        margin = self.width * 0.08
        button_size = (self.width - margin * 5) // 4

        self.__background = HighlightedWidget(
            self.screen, self.x, self.y,
            (self.width, self.height),
            fill = 0, opacity = 200
        )

        self.__text = self.screen.create_text(
            str(), x = self.x + self.width / 2, y = self.y + self.height * 0.2,
            color = (255, 255, 255, 255), font_size = int(self.width * 0.034),
            anchor_x = "center", anchor_y = "center"
        )
        
        self.__button_1 = Button(
            self.screen, self.x + margin + (button_size + margin) * 0,
            self.y + self.height - button_size - margin,
            (button_size, button_size),
            (self.__images[0], self.__images[0])
        )
        
        self.__button_2 = Button(
            self.screen, self.x + margin + (button_size + margin) * 1,
            self.y + self.height - button_size - margin,
            (button_size, button_size),
            (self.__images[1], self.__images[1])
        )

        self.__button_3 = Button(
            self.screen, self.x + margin + (button_size + margin) * 2,
            self.y + self.height - button_size - margin,
            (button_size, button_size),
            (self.__images[2], self.__images[2])
        )

        self.__button_4 = Button(
            self.screen, self.x + margin + (button_size + margin) * 3,
            self.y + self.height - button_size - margin,
            (button_size, button_size),
            (self.__images[3], self.__images[3])
        )

    def check(self, *cursor_pos: int) -> tuple[bool, bool, bool, bool]:
        """
        Verifica se o cursor se encontra na posição de um dos botões.
        """
        button_1 = self.__button_1.check(*cursor_pos)
        button_2 = self.__button_2.check(*cursor_pos)
        button_3 = self.__button_3.check(*cursor_pos)
        button_4 = self.__button_4.check(*cursor_pos)
        
        return button_1, button_2, button_3, button_4

    def draw(self):
        """
        Desenha o widget na tela.
        """
        super().draw()

        self.__background.draw()
        self.__text.draw()
        
        self.__button_1.draw()
        self.__button_2.draw()
        self.__button_3.draw()
        self.__button_4.draw()

    def set_message(self, message: str):
        """
        Define uma mensagem para o widget.
        """
        self.__text.text = message
