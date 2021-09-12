__author__ = "Jean Loui Bernard Silva de Jesus"

from .input import InputFrame
from .logo import LogoFrame
from .output import OutputFrame
from tkinter import Frame, Tk

class ApplicationWindow(Tk):
    """
    Classe para criar a janela da aplicação com os seus widgets.
    """

    def __init__(self, title, icon = None):
        super().__init__()
        self.__input_callback = lambda *args: None
        self.__set_window_config(title, icon)

    def build(self, conversion_options, input_callback, selection_callback, logo_image = None):
        self.__main_frame = Frame(self)
        self.__main_frame.pack(padx = 10, pady = 10)

        self.__logo_frame = LogoFrame(self.__main_frame, logo_image)
        self.__logo_frame.pack()

        self.__input_frame = InputFrame(self.__main_frame, input_callback)
        self.__input_frame.set_menu_options(conversion_options, selection_callback)
        self.__input_frame.pack(pady = 20)

        self.__output_frame = OutputFrame(self.__main_frame)
        self.__output_frame.pack()

    def __set_window_config(self, title, icon):
        self.title(title)
        self.iconbitmap(icon)
        self.resizable(False, False)

    def get_input_variable(self):
        return self.__input_frame.get_input_variable()

    def set_output(self, output):
        self.__output_frame.set_output(output)
