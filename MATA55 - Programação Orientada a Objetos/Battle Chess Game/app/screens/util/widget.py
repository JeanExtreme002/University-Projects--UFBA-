from .widget_group import WidgetGroup
from abc import ABC, abstractmethod
from typing import Optional

class Widget(ABC):
    """
    Classe abstrata para criar widgets na tela.
    """
    def __init__(self, screen, x: int, y: int, size: list[int], widget_group: Optional[WidgetGroup] = None):
        self.__screen = screen
        
        self.__position = (x, y)
        self.__size = size

        if widget_group:
            widget_group.add(self)

    @abstractmethod
    def draw(self): pass

    @property
    def screen(self):
        return self.__screen

    @property
    def x(self) -> int:
        return self.__position[0]

    @property
    def y(self) -> int:
        return self.__position[1]

    @property
    def width(self) -> int:
        return self.__size[0]

    @property
    def height(self) -> int:
        return self.__size[1]
