from .widget import Widget
from .widget_group import WidgetGroup
from typing import Optional

class Scrollbar(Widget):
    """
    Classe para criar botões na tela.
    """
    def __init__(self, screen, x: int, y: int, size: list[int], bar_height: int, widget_group: Optional[WidgetGroup] = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)

        self.__bar_height = bar_height
        
        self.__max_value: float = 0
        self.__value: float = 0
        
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        # Cria o background do scrollbar.
        self.__scrollbar_background = self.screen.create_rectangle(
            self.x, self.y, self.width, self.height, color = (210, 210, 210)
        )

        # Cria o scrollbar.
        self.__scrollbar = self.screen.create_rectangle(
            self.x, self.y, self.width, self.__bar_height, color = (250, 250, 250)
        )

    def __move(self, proportion: float):
        """
        Move a barra de rolagem, dada uma porcentagem.
        """
        if proportion < 0: proportion = 0
        elif proportion > 1: proportion = 1

        y = self.y + (self.height - self.__bar_height) * proportion
        self.__scrollbar.y = self.screen.get_true_y_position(y)
        
        self.__value = self.__max_value * proportion

    def check(self, x: int, y: int, ignore_x: bool = False):
        """
        Verifica se o cursor se encontra na posição do scrollbar.
        """
        in_x = True if ignore_x else self.x <= x <= (self.x + self.width)
        in_y = self.y <= y <= (self.y + self.height)
        
        if in_x and in_y: self.__scrollbar.color = (230, 230, 230)
        else: self.__scrollbar.color = (250, 250, 250)

        return in_x and in_y
        
    def draw(self):
        """
        Desenha o widget na tela.
        """
        self.__scrollbar_background.draw()
        self.__scrollbar.draw()

    def get_max_value(self) -> float:
        """
        Retorna o valor máximo da barra de rolagem.
        """
        return self.__max_value

    def get_value(self) -> float:
        """
        Retorna o valor atual da barra de rolagem.
        """
        return self.__value

    def move(self, diff: float):
        """
        Move a barra de rolagem, dada uma variação.
        """
        proportion = 1 if self.__max_value == 0 else ((self.__value + diff) / self.__max_value)
        self.__move(proportion)

    def move_by_mouse(self, x: int, y: int, ignore_x: bool = False) -> bool:
        """
        Move a barra de rolagem, dada as coordenadas do cursor.
        """
        result = self.check(x, y, ignore_x)
        if not result: return False

        proportion = ((y - self.y) / self.height)
        self.__move(proportion)
        
        return True

    def set_max_value(self, value: float):
        """
        Define um valor máximo para a barra de rolagem.
        """
        self.__max_value = value
