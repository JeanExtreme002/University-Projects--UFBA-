from .highlighted_widget import HighlightedWidget
from .widget_group import WidgetGroup
from typing import Optional
import random

class Snow(HighlightedWidget):
    """
    Classe para criar neve na tela.
    """
    def __init__(self, screen, image: str, particles: int = 300, max_size: int = 2, widget_group: Optional[WidgetGroup] = None):
        super().__init__(
            screen, 0, 0, [screen.width, screen.height],
            color = (80, 80, 80), opacity = 150,
            widget_group = widget_group
        )

        self.__image = image
        
        self.__max_particles = particles
        self.__particles: list = []
        self.__velocity = (1, 4)

        angle = 0.4
        
        self.__vertical_proportion = screen.height / (screen.width * angle)
        self.__max_particle_size = max_size

        self.__interval = screen.get_application().get_fps() * 0.05
        self.__frame_counter = 0

        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar o widget.
        """
        self.__loaded_image = self.screen.load_image(self.__image, (self.width, self.height))
        
        self.__sprite = self.screen.create_sprite(
            self.__loaded_image, x = self.x, y = self.y
        )
        self.__sprite.opacity = self.get_opacity()

    def __create_particle(self):
        """
        Cria uma partícula de neve na tela.
        """
        x = random.randint(int(-self.width * 0.3), int(self.width * 0.9))
        y = random.randint(int(-self.height), 0)

        size = random.randint(1, self.__max_particle_size)
        
        particle = self.screen.create_rectangle(x, y, size, size, color = (230, 230, 230))        
        self.__particles.append(particle)

    def __move_particles(self):
        """
        Move todas as partículas criadas.
        """
        for particle in self.__particles:
            particle.x += self.__velocity[0]
            particle.y -= self.__velocity[1] * self.__vertical_proportion

            # Remove a partícula caso ela tenha saído da tela.
            if particle.x > self.width or particle.y < 0:
                self.__particles.remove(particle)

    def clear(self):
        """
        Remove todas as partículas de neve.
        """
        self.__particles = []
            
    def draw(self):
        """
        Desenha o widget na tela.
        """
        super().draw()
        self.__sprite.draw()

        for particle in self.__particles:
            particle.draw()

    def next(self):
        """
        Avança para o próximo estado da animação.
        """
        self.__frame_counter += 1

        # Verifica se está no momento de atualizar a posição dos elementos.
        if self.__frame_counter < self.__interval: return
        self.__frame_counter = 0

        # Cria uma nova partícula caso haja espaço para mais.
        if len(self.__particles) < self.__max_particles:
            self.__create_particle()

        # Move as partículas.
        self.__move_particles()

    def set_opacity(self, value: int):
        """
        Define a opacidade do widget.
        """
        super().set_opacity(value)
        self.__sprite.opacity = value

    def set_particles(self, value: int):
        """
        Define uma quantidade de partículas.
        """
        self.__max_particles = value

    def set_velocity(self, velocity: tuple[int, int]):
        """
        Define a velocidade da neve.
        """
        self.__velocity = velocity
           

        

        

        
