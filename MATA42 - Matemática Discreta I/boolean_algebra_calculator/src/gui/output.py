__author__ = "Jean Loui Bernard Silva de Jesus"

from tkinter import Canvas, Frame, Label, Scrollbar

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
        # Cria um Canvas para inserir o Frame da tabela. Dessa forma, é possível utilizar o Scrollbar na tabela.
        self.__canvas = Canvas(self)
        self.__canvas.pack(side = "left", fill = "both", expand = True)

        # Cria o frame da tabela e o insere no Canvas.
        self.__table_frame = Frame(self.__canvas)
        self.__table_frame.config({key: value for key, value in self.__table_style.items() if key != "font"})
        self.__table_id = self.__canvas.create_window((0, 0), window = self.__table_frame, anchor = "nw")

        # Cria uma Scrollbar vertical, para rolar o Canvas e, consequentemente, a tabela.
        vertical_scroll_bar = Scrollbar(self, orient = "vertical", command = self.__canvas.yview)
        vertical_scroll_bar.pack(side = "right", fill = "y")
        self.__canvas.configure(yscrollcommand = vertical_scroll_bar.set)

        # Configura evento para redimensionar o Frame da tabela e reconfigurar
        # o Scrollbar, quando o Canvas for redimensionado, e cria uma tabela padrão, vazia.
        self.__canvas.bind("<Configure>", self.__on_canvas_configure)
        self.__table_frame.bind("<Configure>", lambda event: self.__update_scroll_region())
        self.set_output(table = [])

    def __build_table(self, table):
        # Percorre a lista criando no frame cada linha da tabela.
        for row in range(len(table)):
            row_bg = self.__table_header_background if row == 0 else self.__table_item_background
            self.__build_table_row(row, table, row_bg)

    def __build_table_column(self, row, column, text, background):
        # Cria um item da tabela em uma dada linha e coluna.
        label = Label(self.__table_frame, self.__table_style, text = text, bg = background)
        label.grid(row = row, ipadx = 5, column = column, sticky = "we")

        # Adiciona um peso para que o widget se expanda e o computa na variável de quantidade de colunas.
        self.__table_frame.columnconfigure(column, weight = 1)
        self.__column_count += 1

    def __build_table_row(self, row, table, background):
        # Percorre e cria cada coluna da linha da tabela.
        for column in range(len(table[0])):
            text = table[row][column]
            self.__build_table_column(row, column, text, background)

    def __clear_frame(self):
        # Remove todos os itens da tabela, resetando a sua configuração.
        for widget in self.__table_frame.winfo_children(): widget.destroy()
        for column in range(self.__column_count): self.__table_frame.columnconfigure(column, weight = 0)
        self.__column_count = 0

    def __create_empty_table(self, rows, columns):
        # Cria uma tabela vazia com uma determinada quantidade de linhas e colunas.
        self.set_output([["",] * columns for row in range(rows)])

    def __on_canvas_configure(self, event = None):
        self.__update_table_size()
        self.__update_scroll_region()

    def __update_scroll_region(self):
        # Reconfigura a região do Canvas em que o Scrollbar pode atuar.
        self.__canvas.configure(scrollregion = self.__canvas.bbox("all"))

    def __update_table_size(self):
        # Redimensiona o Frame da tabela com base no tamanho do Canvas.
        self.__canvas.itemconfig(self.__table_id, width = self.__canvas.winfo_width() - 2)

    def set_output(self, table = []):
        # Apaga a tabela anterior e cria uma nova, a partir da lista recebida.
        if len(table) > 0 and len(table[0]) > 0:
            self.__clear_frame()
            self.__build_table(table)
        else: self.__create_empty_table(rows = 5, columns = 3)
