__author__ = "Jean Loui Bernard Silva de Jesus"

from .input import InputFrame
from .output import OutputFrame
from tkinter import Frame, Tk

class ApplicationWindow(Tk):
    """
    Classe para criar a janela da aplicação com os seus widgets.
    """
    
    def __init__(self, title, icon = None):
        super().__init__()
        self.__set_window_config(title, icon)

    def __set_window_config(self, title, icon):
        self.title(title)
        self.iconbitmap(icon)
        self.resizable(False, False)

    def build(self, operators, input_callback, on_button_press):
        self.__main_frame = Frame(self)
        self.__main_frame.pack(padx = 10, pady = 10)

        self.__output_frame = OutputFrame(self.__main_frame)
        self.__output_frame.pack(pady = 10, fill = "x")

        self.__input_frame = InputFrame(self.__main_frame, operators, input_callback, on_button_press)
        self.__input_frame.pack()

    def set_output(self, output):
        self.__output_frame.set_output(output)
