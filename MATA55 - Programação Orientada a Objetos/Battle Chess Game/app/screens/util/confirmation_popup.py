from .button import Button
from .popup import Popup
from .widget_group import WidgetGroup
from typing import Optional

class ConfirmationPopup(Popup):
    """
    Classe para criar um popup de confirmação na tela.
    """
    def __init__(self, screen, x: int, y: int, size: list[int], image: str, button_images: list[list], widget_group: Optional[WidgetGroup] = None):
        super().__init__(screen, x, y, size, image, widget_group = widget_group)

        self.__button_images = button_images
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        button_width = self.width * 0.1
        button_height = button_width * 0.75

        # Cria botão de cancelamento.
        self.__cancel_button = Button(
            self.screen, self.x + self.width * 0.27,
            self.y + self.height - button_height - self.width * 0.18,
            (button_width, button_height),
            (self.__button_images[0][0], self.__button_images[0][1])
        )

        # Cria botão de confirmação.
        self.__confirm_button = Button(
            self.screen, self.x + self.width * 0.73 - button_width,
            self.y + self.height - button_height - self.width * 0.18,
            (button_width, button_height),
            (self.__button_images[1][0], self.__button_images[1][1])
        )

    def check(self, x: int, y: int) -> tuple[bool, bool]:
        """
        Verifica se o cursor do mouse se
        encontra na posição dos botões.
        """
        if self.__cancel_button.check(x, y): return True, False
        elif self.__confirm_button.check(x, y): return False, True
        return False, False

    def draw(self, with_message_only:bool = True) -> bool:
        """
        Desenha o widget na tela.
        """
        if not super().draw(with_message_only): return False
        
        self.__cancel_button.draw()
        self.__confirm_button.draw()

        return True
