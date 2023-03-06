from .highlighted_widget import HighlightedWidget
from .widget_group import WidgetGroup
from typing import Optional

class Popup(HighlightedWidget):
    """
    Classe para criar um popup com uma mensagem na tela.
    """
    def __init__(self, screen, x: int, y: int, size: list[int], image: str, widget_group: Optional[WidgetGroup] = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)

        self.__texts: list = []
        
        self.__image = image
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        # Cria a imagem de background da caixa de texto.
        self.__loaded_image = self.screen.load_image(self.__image, (self.width, self.height))
        
        self.__background = self.screen.create_sprite(
            self.__loaded_image, x = self.x, y = self.y
        )

    def delete_message(self):
        """
        Apaga a mensagem.
        """
        self.__texts = []

    def draw(self, with_message_only: bool = True) -> bool:
        """
        Desenha o widget na tela, com a possível condição de que haja mensagem.
        """
        if with_message_only and not self.__texts: return False

        super().draw()
        
        self.__background.draw()

        for text in self.__texts:
            text.draw()
            
        return True

    def has_message(self) -> bool:
        """
        Verifica se existe mensagem a ser exibida.
        """
        return len(self.__texts) > 0

    def set_message(self, x: int, y: int, *lines: str, color: tuple[int, int, int, int] = (0, 0, 0, 255), font_size: int = 16, anchor: tuple[str, str] = ("center", "center"), line_spacing: int = 1):
        """
        Define uma mensagem a ser exibida.
        """
        self.delete_message()
        line_index = 0
        
        for line in lines:
            text = self.screen.create_text(
                line, x = int(x), y = int(y + line_spacing * line_index),
                color = color, font_size = int(font_size),
                anchor_x = anchor[0], anchor_y = anchor[1]
            )
            self.__texts.append(text)
            line_index += 1
