from .widget import Widget
from .widget_group import WidgetGroup
from typing import Optional

class Button(Widget):
    """
    Classe para criar botões na tela.
    """
    def __init__(self, screen, x: int, y: int, size: list[int], images: list[str], widget_group: Optional[WidgetGroup] = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)
        
        self.__activated = False
        self.__previous_status = False
        self.__images = images

        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        self.__sprite = None
        self.change_image(self.__images)
        
    def __load_images(self):
        """
        Carrega as imagens do botão.
        """
        image_1 = self.screen.load_image(self.__images[0], (self.width, self.height))
        image_2 = self.screen.load_image(self.__images[1], (self.width, self.height))
        
        self.__loaded_images = [image_1, image_2]

    def __create_sprite(self):
        """
        Cria a imagem do botão.
        """
        self.__sprite = self.screen.create_sprite(
            self.__loaded_images[int(self.__activated)],
            x = self.x, y = self.y
        )

    def __delete_sprite(self):
        """
        Deleta a imagem do botão.
        """
        if self.__sprite is not None: self.__sprite.delete()

    def change_image(self, images: list[str]):
        """
        Troca as imagens do botão.
        """
        self.__images = images
        self.__load_images()
        self.__delete_sprite()
        self.__create_sprite()

    def check(self, *cursor_pos: int) -> bool:
        """
        Verifica se o cursor se encontra na posição do botão.
        """
        in_x = self.x <= cursor_pos[0] <= (self.x + self.width)
        in_y = self.y <= cursor_pos[1] <= (self.y + self.height)
        
        self.__activated = (in_x and in_y)

        # Se sim, a imagem do botão será alterada para a imagem de botão ativo.
        if self.__previous_status != self.__activated:
            self.__previous_status = self.__activated
            self.__delete_sprite()
            self.__create_sprite()

        return self.__activated

    def draw(self):
        """
        Desenha o widget na tela.
        """
        self.__sprite.draw()
