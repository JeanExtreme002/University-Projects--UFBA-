__author__ = "Jean Loui Bernard Silva de Jesus"

from tkinter import Frame, Label, StringVar
from tkinter.ttk import Button, Entry

class InputFrame(Frame):
    """
    Classe para criar um frame com todos os widgets
    relacionados ao input do usuário.
    """

    def __init__(self, master = None, operators = {}, input_callback = lambda *args: None, on_button_press = lambda *args: None):
        super().__init__(master)
        self.__build(operators, input_callback, on_button_press)

    def __build(self, operators, input_callback, on_button_press):
        self.__build_input_frame(input_callback, on_button_press)
        self.__build_operator_buttons(operators)

    def __build_input_frame(self, input_callback, on_button_press):
        self.__input = StringVar()
        self.__input.trace("w", lambda *args: input_callback(self.__input))

        frame = Frame(self)
        frame.pack(fill = "x")

        # Cria a Entry, adicionando um evento para calcular a expressão ao apertar "Enter".
        self.__entry = Entry(frame, textvariable = self.__input)
        self.__entry.bind("<Return>", lambda event: on_button_press(self.__input))
        self.__entry.pack(side = "left", padx = (0, 10), fill = "x", expand = True)

        # Cria um botão para calcular a expressão.
        Button(frame, text = "Calcular", command = lambda: on_button_press(self.__input)).pack(side = "left")

    def __build_operator_buttons(self, operators):
        frame = Frame(self)
        frame.pack(pady = 10)

        # Cria um botão para cada operador, para inserir o seu caractere na Entry.
        for label, operator in operators.items():
            command = lambda event = None, operator = operator: self.__insert_operator_to_input(operator)
            Button(frame, text = label, width = 20, command = command, takefocus = 0).pack(side = "left")

            # Adiciona um evento para a Entry, para inserir o operador através do teclado.
            event_key = label.split(":", maxsplit = 1)[0].strip()
            if event_key.isnumeric(): self.__entry.bind("<Key-{}>".format(event_key), command)

    def __insert_operator_to_input(self, operator = ""):
        # Insere o operador na posição do cursor na Entry.
        cursor_position = self.__entry.index("insert")
        self.__entry.insert(cursor_position, operator)
