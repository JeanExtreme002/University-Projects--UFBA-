__author__ = "Jean Loui Bernard Silva de Jesus"

from tkinter import Frame, Menu, StringVar, Label
from tkinter.ttk import Entry, Menubutton

class InputFrame(Frame):
    """
    Classe para criar um frame com todos os widgets
    relacionados ao input do usuário.
    """

    __input_width = 70
    __label_font = ("Helvetica", 12)
    __entry_font = ("Helvetica", 10)

    def __init__(self, master = None, callback = lambda event: None):
        super().__init__(master)
        self.__build(callback)

    def __build(self, callback):
        frame = Frame(self)
        frame.pack(pady = 5, fill = "x")

        Label(frame, text = "Valor a ser convertido: ", font = self.__label_font).pack(side = "left")
        self.__build_menu_button(frame, side = "right")

        Label(frame, text = "Converter para: ", font = self.__label_font).pack(side = "right")
        self.__build_entry(self, callback)

    def __build_entry(self, parent, callback, **pack_kwargs):
        self.__input = StringVar()
        self.__input.trace("w", lambda *args: callback(self.__input))

        self.__entry = Entry(parent, textvariable = self.__input, width = self.__input_width, font = self.__entry_font)
        self.__entry.pack(**pack_kwargs)

    def __build_menu_button(self, parent, **pack_kwargs):
        self.__menu_button = Menubutton(parent)
        self.__menu_button.pack(**pack_kwargs)

        self.__menu = Menu(tearoff = 0)
        self.__menu_button.config(menu = self.__menu)

    def __set_selected_option_label(self, index):
        self.__menu_button.config(text = self.__options[index])

    def __on_select_option(self, index):
        self.__set_selected_option_label(index)
        self.__selection_callback(index)

    def __update_menu_button_config(self):
        # Configura o widget para que ele possua a maior largura necessária, para que seu tamanho
        # não varie ao selecionar opções de diferentes comprimentos de texto, e define por padrão
        # a primeira opção do menu como opção selecionada.
        self.__menu_button.config(width = max([len(text) for text in self.__options]))
        self.__set_selected_option_label(0)

    def get_input_variable(self):
        return self.__input

    def set_menu_options(self, options, callback):
        self.__options = options
        self.__selection_callback = callback

        # Insere as opções no menu, definindo uma função que recebe o índice da opção selecionada.
        for option in range(len(options)):
            command = lambda index = option: self.__on_select_option(index)
            self.__menu.add_command(label = options[option], command = command)

        # Atualiza as configurações do widget para que o mesmo se adeque ao novo menu.
        self.__update_menu_button_config()
