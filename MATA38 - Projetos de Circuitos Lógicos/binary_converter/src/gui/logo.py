__author__ = "Jean Loui Bernard Silva de Jesus"

from tkinter import Frame, Label, PhotoImage

class LogoFrame(Frame):
    """
    Classe para criar um frame com a logo do programa.
    """

    def __init__(self, master = None, image_fn = None):
        super().__init__(master)
        self.__build(image_fn)

    def __build(self, image_fn):
        self.__photo_image = PhotoImage(file = image_fn)
        Label(self, image = self.__photo_image).pack()
