from .util import Achievement, Snow
from abc import ABC, abstractmethod
from pyglet import image
from pyglet import gl
from pyglet import graphics
from pyglet import shapes
from pyglet import sprite
from pyglet import text
from pyglet import window
from typing import Optional, Union

# Configuração para habilitar o redimensionamento de imagens.
gl.glEnable(gl.GL_TEXTURE_2D)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


class Screen(ABC):
    """
    Classe abstrata para criar telas.
    """

    _images: dict = dict()
    _achievement_widget: Optional[Achievement] = None
    _defeat_theme = False
    
    def __init__(self, application):
        self.__application = application
        self.__build()

    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """ 
        application = self.get_application()

        # Cria widget para mostrar animação de neve.
        frost_filename = application.paths.get_image("general", "frost.png")

        Screen._snow_widget = Snow(self, frost_filename)

        # Cria widget para mostrar conquistas.
        achievement_filename = application.paths.get_image("general", "trophy.png")
        
        Screen._achievement_widget = Achievement(
            self, (application.width * 0.4, application.height * 0.13),
            image = achievement_filename, font_size = application.height * 0.15 * 0.2
        )
        
    @property
    def width(self):
        return self.__application.width

    @property
    def height(self):
        return self.__application.height

    @property
    def sound_player(self):
        return self.__application.get_sound_player()

    def create_batch(self, *args, **kwargs) -> graphics.Batch:
        """
        Cria um batch.
        """
        return graphics.Batch(*args, **kwargs)

    def create_rectangle(self, x: int, y: int, width: int, height: int, **kwargs) -> shapes.Rectangle:
        """
        Cria um retângulo, com a posição Y invertida.
        """
        y = self.get_true_y_position(y)
        height *= -1

        shape = shapes.Rectangle(
            x = x, y = y,
            width = width,
            height = height,
            **kwargs
        )
        return shape

    def create_sprite(self, img: image.TextureRegion, x: int, y: int, **kwargs) -> sprite.Sprite:
        """
        Cria uma imagem, com a posição Y invertida.
        """
        y = self.get_true_y_position(y, img.height)
        return sprite.Sprite(img, x = x, y = y, **kwargs)

    def create_text(self, string: str, x: int, y: int, **kwargs) -> text.Label:
        """
        Cria um texto, com a posição Y invertida.
        """
        y = self.get_true_y_position(y)
        return text.Label(string, x = x, y = y, **kwargs)

    def free_memory(self, save_original: bool = True):
        """
        Método para apagar todas as imagens utilizadas pela tela.
        """
        found_image_filenames = []

        # Busca por imagens que não estão sendo utilizadas por outras telas,
        # para que sejam posteriormente removidas do dicionário.
        for filename, resolutions in Screen._images.items():
            if self in resolutions["original"]["users"]:
                resolutions["original"]["users"].remove(self)

            if len(resolutions["original"]["users"]) == 0:
                found_image_filenames.append([filename, list(resolutions.keys())])

        # Percorre a lista de imagens encontradas para remoção, apagando-as do dicionário.
        for filename, resolutions in found_image_filenames:

            # Apaga todo o dicionário referente ao arquivo de imagem,
            # caso o usuário não deseje salvar a imagem original.
            if not save_original:
                Screen._images.pop(filename)
                continue

            # Remove todas as diferentes resoluções de imagem derivadas da imagem original.
            for size in resolutions:
                if size != "original": Screen._images[filename].pop(size)

    def get_application(self):
        """
        Retorna o objeto Application.
        """
        return self.__application

    def get_true_y_position(self, y: int, height: int = 0):
        """
        Calcula a posição Y invertida.
        """
        return self.height - y - height

    def is_defeat_theme(self):
        """
        Verifica se o tema de derrota está definido.
        """
        return Screen._defeat_theme

    def load_image(self, filename: str, size: Union[tuple[int, int], str] = "original", save: bool = True) -> image.TextureRegion:
        """
        Carrega uma imagem.
        """
        # Obtém a imagem original, sem modificações, se ela não tiver sido salva.
        if not filename in Screen._images:
            Screen._images[filename] = dict()
            Screen._images[filename]["original"] = dict()

            # Tenta carregar a imagem.
            try: Screen._images[filename]["original"]["image"] = image.load(filename)

            # Se não for possível, o dicionário criado anteriormente 
            # para ela é apagado e a exceção é relançada.
            except FileNotFoundError as error:
                Screen._images.pop(filename)
                raise error

            # Cria dicionário para registrar as telas que fazem uso da mesma imagem.
            Screen._images[filename]["original"]["users"] = set()
        
        # Caso a imagem na resolução solicitada não tenha sido salva, uma cópia
        # da imagem original será criada, redimensionando a mesma.
        if not size in Screen._images[filename]:
            img = Screen._images[filename]["original"]["image"]
            img = img.get_region(0, 0, img.width, img.height)

            img = img.get_texture()
            img.width = size[0]
            img.height = size[1]
            
            Screen._images[filename][size] = dict()
            Screen._images[filename][size]["image"] = img

        # Obtém a imagem final, que será retornada pelo método.
        final_image = Screen._images[filename][size]["image"] 

        # Remove a imagem do dicionário se o usuário não deseja que a mesma seja salva.
        if not save:
            if len(Screen._images[filename]["original"]["users"]) == 0:
                Screen._images.pop(filename)

        # Registra a tela que está usando a imagem salva.
        else: Screen._images[filename]["original"]["users"].add(self)

        # Retorna a imagem com a resolução deseja.
        return final_image

    def on_close(self):
        """
        Evento para fechar a janela.
        """
        self.__application.close()
        
    def on_draw(self, by_scheduler: bool = False):
        """
        Evento para desenhar a tela.
        """
        if by_scheduler: Screen._achievement_widget.next()
        
        self.on_draw_screen(by_scheduler)

        # Desenha uma nevasca na tela caso solicitado um tema de derrota.
        if Screen._defeat_theme:
            Screen._snow_widget.next()
            Screen._snow_widget.draw()
        
        Screen._achievement_widget.draw()

    @abstractmethod
    def on_draw_screen(self, by_scheduler: bool = False):
        """
        Método chamado pelo evento on_draw para desenhar a tela.
        """
        pass

    def on_key_press(self, symbol, modifiers):
        """
        Evento de tecla pressionada.
        """
        if symbol == window.key.F12: self.print_screen()
        return True

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        """
        Evento de botão do mouse pressionado e movendo.
        """
        return x, self.get_true_y_position(y), button, modifiers

    def on_mouse_motion(self, x, y, *args):
        """
        Evento de movimentação do cursor.
        """
        return x, self.get_true_y_position(y), *args

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Evento de botão do mouse pressionado.
        """
        return x, self.get_true_y_position(y), button, modifiers

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Evento de botão do mouse liberado.
        """
        return x, self.get_true_y_position(y), button, modifiers

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """
        Evento de scroll do mouse.
        """
        return x, self.get_true_y_position(y), scroll_y

    def print_screen(self, region: Optional[tuple[int, int, int, int]] = None, filename: Optional[str] = None):
        """
        Tira um print da tela do jogo e salva em imagem.
        """
        screenshot_id = len(self.__application.paths.get_screenshot_list()) + 1

        # Define um nome de arquivo caso não haja.
        if not filename:
            filename = "screenshot_{}.png".format(screenshot_id)
            filename = self.__application.paths.get_screenshot(filename)

        # Obtém a captura da tela.
        screenshot = image.get_buffer_manager().get_color_buffer()

        # Corta a imagem se for solicitado.
        screenshot.x = int(region[0]) if region else screenshot.x
        screenshot.y = int(region[1]) if region else screenshot.y
        
        screenshot.width = int(region[2]) if region else screenshot.width
        screenshot.height = int(region[3]) if region else screenshot.height

        # Salva a imagem em um arquivo.
        screenshot.save(filename)

        # Conquista de usuário.
        if not region: self.get_application().add_achievement("Congelando o tempo...", "Realizou uma captura de tela.")

    def set_achievement(self, title: str):
        """
        Mostra uma conquista obtida na tela.
        """
        Screen._achievement_widget.set_achievement(title)

    def set_defeat_theme(self, boolean: bool, particles: Optional[int] = None, opacity: Optional[int] = None):
        """
        Define um tema de derrota.
        """
        Screen._defeat_theme = boolean
        
        if particles: Screen._snow_widget.set_particles(particles)
        if opacity: Screen._snow_widget.set_opacity(opacity)
