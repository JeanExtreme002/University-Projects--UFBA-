from .widget import Widget
from .widget_group import WidgetGroup
from typing import Optional

class Slide(Widget):
    """
    Classe para criar slides na tela.
    """
    def __init__(self, screen, x: int, y: int, size: list[int], images: str, widget_group: Optional[WidgetGroup] = None):
        super().__init__(screen, x, y, size, widget_group = widget_group)

        self.__max_opacity = 255
        self.__opacity = 70
        self.__direction = 1
        self.__velocity = 1.2
        self.__index = 0

        # Define um tempo de espera, para quando a opacidade chegar em 100%.
        self.__show_waiting = screen.get_application().get_fps() * 5
        self.__waited = 0

        self.__images = images
        self.__load_images()
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        self.__create_sprite()

    def __create_sprite(self):
        """
        Cria a imagem do widget.
        """
        self.__sprite = self.screen.create_sprite(
            self.__loaded_images[self.__index],
            x = self.x, y = self.y
        )

    def __delete_sprite(self):
        """
        Deleta a imagem.
        """
        self.__sprite.delete()

    def __load_images(self):
        """
        Carrega todas as imagens que aparecerão nos slides.
        """
        self.__loaded_images = []
        
        for filename in self.__images:
            image = self.screen.load_image(filename, (self.width, self.height))
            self.__loaded_images.append(image)

    def draw(self):
        """
        Desenha o widget na tela.
        """
        self.__sprite.draw()

    def set_velocity(self, velocity: int):
        """
        Define uma velocidade de "fade effect".
        """
        if 0 > velocity > self.__max_opacity:
            raise ValueError("Velocity must be a value between 0 and {}".format(self.__max_opacity))
        self.__velocity = velocity

    def next(self):
        """
        Avança para o próximo estado da animação.
        """
        # Após chegar na opacidade máxima, ele mantém a mesma por um certo período de tempo.
        if self.__opacity == self.__max_opacity and self.__waited < self.__show_waiting:
            self.__waited += 1
        else:
            self.__waited = 0
            self.__opacity += self.__velocity * self.__direction

        # A opacidade deve estar entre zero e cem.
        if self.__opacity > self.__max_opacity: self.__opacity = self.__max_opacity
        elif self.__opacity < 0: self.__opacity = 0

        # Verifica se a troca de imagem deve ser realizada.
        if self.__opacity == 0 and self.__direction < 0:
            self.__index = (self.__index + 1) % len(self.__loaded_images)
            self.__direction *= -1
            
            self.__delete_sprite()
            self.__create_sprite()

        # Verifica se já chegou no pico.
        elif self.__opacity == self.__max_opacity and self.__direction > 0:
            self.__direction *= -1

        self.__sprite.opacity = self.__opacity

        
