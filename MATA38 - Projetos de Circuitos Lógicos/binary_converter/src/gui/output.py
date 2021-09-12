__author__ = "Jean Loui Bernard Silva de Jesus"

from tkinter import Frame, Label, Text

class OutputFrame(Frame):
    """
    Classe para criar um frame com todos os widgets
    relacionados ao output do programa.
    """

    __output_width = 70
    __label_font = ("Helvetica", 12)
    __text_font = ("Helvetica", 10)

    def __init__(self, master = None):
        super().__init__(master)
        self.__build()

    def __build(self):
        Label(self, text = "O valor convertido aparecerá abaixo:", font = self.__label_font).pack(anchor = "w")
        self.__text = Text(self, width = self.__output_width, height = 5, font = self.__text_font)
        self.__text.pack()

    def set_output(self, text):
        self.__text.delete(0.0, "end")
        self.__text.insert(0.0, text)
