__author__ = "Jean Loui Bernard Silva de Jesus"

from tkinter import Frame, Label

class OutputFrame(Frame):
    """
    Classe para para mostrar o output do
    programa em formato de tabela.
    """

    __table_style = {
        "borderwidth": 1,
        "relief": "solid",
        "font": ("Helvetica", 12)
    }

    __table_header_background = "lightblue"
    __table_item_background = "white"

    def __init__(self, master = None):
        super().__init__(master)
        self.__column_count = 0
        self.__build()

    def __build(self):
        self.config({key: value for key, value in self.__table_style.items() if key != "font"})
        self.set_output(table = [])

    def __build_table(self, table):
        # Percorre a lista criando no frame cada linha da tabela.
        for row in range(len(table)):
            row_bg = self.__table_header_background if row == 0 else self.__table_item_background
            self.__build_table_row(row, table, row_bg)

    def __build_table_column(self, row, column, text, background):
        # Cria um item da tabela em uma dada linha e coluna.
        label = Label(self, self.__table_style, text = text, bg = background)
        label.grid(row = row, ipadx = 5, column = column, sticky = "we")

        # Adiciona um peso para que o widget se expanda e o computa na variável de quantidade de colunas.
        self.columnconfigure(column, weight = 1)
        self.__column_count += 1

    def __build_table_row(self, row, table, background):
        # Percorre e cria cada coluna da linha da tabela.
        for column in range(len(table[0])):
            text = table[row][column]
            self.__build_table_column(row, column, text, background)

    def __clear_frame(self):
        # Remove todos os itens da tabela, resetando a sua configuração.
        for widget in self.winfo_children(): widget.destroy()
        for column in range(self.__column_count): self.columnconfigure(column, weight = 0)
        self.__column_count = 0

    def __create_empty_table(self, rows, columns):
        # Cria uma tabela vazia com uma determinada quantidade de linhas e colunas.
        self.set_output([["",] * columns for row in range(rows)])

    def set_output(self, table = []):
        # Apaga a tabela anterior e cria uma nova, a partir da lista recebida.
        if len(table) > 0 and len(table[0]) > 0:
            self.__clear_frame()
            self.__build_table(table)
        else: self.__create_empty_table(rows = 5, columns = 3)
