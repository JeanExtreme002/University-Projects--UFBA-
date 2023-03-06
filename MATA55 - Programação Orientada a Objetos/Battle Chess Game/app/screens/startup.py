from .screen import Screen

class StartupScreen(Screen):
    """
    Classe para criar uma tela de inicialização.
    """
    
    def __init__(self, application):
        super().__init__(application)
        self.__build()
        
    def __build(self):
        """
        Cria todas as imagens e objetos gráficos
        necessários para desenhar a tela.
        """
        application = self.get_application()
        
        # Cria o plano de fundo.
        background_filename = application.paths.get_image("startup", "background.png")
        self.__background_image = self.load_image(background_filename, (self.width, self.height))

    def on_draw_screen(self, by_scheduler: bool = False):
        """
        Evento para desenhar a tela.
        """
        self.__background_image.blit(0, 0)
