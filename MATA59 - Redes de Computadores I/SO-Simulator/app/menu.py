from tkinter import BooleanVar, Button, Checkbutton, Frame, Label, Menu, Tk
from tkinter.ttk import Entry, Menubutton

from memory_paging import MemoryManager
from memory_paging.fifo import FIFOMemoryManager
from memory_paging.lru import LRUMemoryManager

from process_scheduler import ProcessScheduler
from process_scheduler.edf import EDFProcessScheduler
from process_scheduler.fifo import FIFOProcessScheduler
from process_scheduler.round_robin import RoundRobinProcessScheduler
from process_scheduler.sjf import SJFProcessScheduler

import json
import os


class MenuWindow(Tk):
    """
    Classe para criar uma tela inicial de menu.
    """

    __NOT_REQUIRED_MESSAGE = "(not required)"
    __CONFIG_FILENAME = "config.cfg"

    def __init__(self, title: str = "Window", size: tuple[int] = (350, 550)):
        super().__init__()
        self.__size = size

        # Configurações relacionadas ao escalonador de processos.
        self.__cpu_algorithm = FIFOProcessScheduler
        self.__context_switching = None
        self.__quantum = None

        # Configurações relacionadas à paginação.
        self.__paging_algorithm = FIFOMemoryManager
        self.__ram_memory_size = 200 * 1000
        self.__memory_page_size = 4 * 1000
        self.__page_per_process = 10

        self.__update_interval = 1000
        self.__closed = True

        self.title(title)
        self.resizable(False, False)
        self.geometry("{}x{}".format(*size))

    @property
    def closed(self):
        return self.__closed

    def __finish_config(self):
        """
        Encerra a janela de menu, salvando as configurações feitas.
        """
        self.__quantum = self.__entry_2.get()
        self.__context_switching = self.__entry_3.get()

        self.__ram_memory_size = self.__entry_4.get()
        self.__memory_page_size = self.__entry_5.get()
        self.__page_per_process = self.__entry_6.get()
        self.__update_interval = self.__entry_7.get()

        # Deve haver um quantum e um chaveamento para os algoritmos RR e EDF.
        if self.__cpu_algorithm in [RoundRobinProcessScheduler, EDFProcessScheduler]:
            self.__label_2["fg"] = "black"
            self.__label_3["fg"] = "black"

            if len(self.__quantum) == 0 or not self.__quantum.replace("0", ""):
                self.__label_2["fg"] = "red"
                return

            if len(self.__context_switching) == 0 or not self.__context_switching.replace("0", ""):
                self.__label_3["fg"] = "red"
                return

            self.__quantum = int(self.__quantum)
            self.__context_switching = int(self.__context_switching)
        else:
            self.__quantum = None
            self.__context_switching = None

        self.__label_5["fg"] = "black"
        self.__label_6["fg"] = "black"
        self.__label_7["fg"] = "black"

        # Verifica se o usuário definiu as configurações nas entries corretamente.
        if not self.__ram_memory_size or not self.__ram_memory_size.replace("0", ""):
            self.__label_5["fg"] = "red"
            return

        if not self.__memory_page_size or not self.__memory_page_size.replace("0", ""):
            self.__label_6["fg"] = "red"
            return

        if not self.__page_per_process or not self.__page_per_process.replace("0", ""):
            self.__label_7["fg"] = "red"
            return

        if not self.__update_interval or not self.__update_interval.replace("0", ""):
            self.__label_8["fg"] = "red"
            return

        self.__ram_memory_size = int(self.__ram_memory_size)
        self.__memory_page_size = int(self.__memory_page_size)
        self.__page_per_process = int(self.__page_per_process)
        self.__update_interval = int(self.__update_interval)

        self.__closed = False

        # Salva as configurações, caso desejado.
        if self.__save_config.get():
            with open(self.__CONFIG_FILENAME, "w") as file:
                file.write(json.dumps({
                    "cpu_algorithm": self.get_process_scheduler().name,
                    "quantum": self.__entry_2.get(),
                    "context_switching": self.__entry_3.get(),
                    "paging_algorithm": self.get_memory_manager().name,
                    "ram_size": self.__entry_4.get(),
                    "page_size": self.__entry_5.get(),
                    "page_per_process": self.__entry_6.get(),
                    "freeze_process": self.__freeze_process.get(),
                    "generate_log_file": self.__generate_log_file.get(),
                    "save_config": self.__save_config.get(),
                    "update_interval": self.__entry_7.get()
                }, indent = " " * 4))

        self.destroy()

    def __load_config_from_file(self):
        """
        Carrega as configurações do arquivo de configurações, caso exista.
        """
        if not os.path.exists(self.__CONFIG_FILENAME): return

        with open(self.__CONFIG_FILENAME, encoding = "UTF-8") as file:
            data = json.loads(file.read())

        cpu_algorithms = [
            FIFOProcessScheduler,
            SJFProcessScheduler,
            RoundRobinProcessScheduler,
            EDFProcessScheduler
        ]
        cpu_algorithms_dict = {algorithm(0, 0).name: algorithm for algorithm in cpu_algorithms}
        cpu_algorithm = cpu_algorithms_dict.get(data.get("cpu_algorithm"), FIFOProcessScheduler)

        self.__entry_2.delete(0, "end")
        self.__entry_3.delete(0, "end")

        self.__set_cpu_algorithm(cpu_algorithms.index(cpu_algorithm))

        self.__entry_2.insert(0, str(data.get("quantum", "")))
        self.__entry_3.insert(0, str(data.get("context_switching", "")))

        paging_algorithms = [
            FIFOProcessScheduler,
            LRUMemoryManager
        ]
        paging_algorithms_dict = {algorithm(1, 1).name: algorithm for algorithm in paging_algorithms}
        paging_algorithm = paging_algorithms_dict.get(data.get("paging_algorithm"), FIFOMemoryManager)

        self.__entry_4.delete(0, "end")
        self.__entry_5.delete(0, "end")
        self.__entry_6.delete(0, "end")

        self.__set_memory_algorithm(paging_algorithms.index(paging_algorithm))

        self.__entry_4.delete(0, "end")
        self.__entry_4.insert(0, str(data.get("ram_size", "")))
        self.__entry_5.delete(0, "end")
        self.__entry_5.insert(0, str(data.get("page_size", "")))
        self.__entry_6.delete(0, "end")
        self.__entry_6.insert(0, str(data.get("page_per_process", "")))

        self.__entry_7.delete(0, "end")
        self.__entry_7.insert(0, str(data.get("update_interval", self.__update_interval)))

        self.__freeze_process_checkbutton.deselect()
        self.__generate_log_file_checkbutton.deselect()
        self.__save_config_checkbutton.deselect()

        if data.get("freeze_process", False) is True: self.__freeze_process_checkbutton.select()
        if data.get("generate_log_file", True) is True: self.__generate_log_file_checkbutton.select()
        if data.get("save_config", False) is True: self.__save_config_checkbutton.select()

    def __set_cpu_algorithm(self, index: int):
        """
        Define o algorimo (classe) que será utilizado para escalonamento de processos.
        """
        last_algorithm = self.__cpu_algorithm

        self.__cpu_algorithm = [
            FIFOProcessScheduler,
            SJFProcessScheduler,
            RoundRobinProcessScheduler,
            EDFProcessScheduler
        ][index]

        if index in [0, 1]:
            self.__entry_2.delete(0, "end")
            self.__entry_3.delete(0, "end")

            self.__entry_2.insert(0, self.__NOT_REQUIRED_MESSAGE)
            self.__entry_3.insert(0, self.__NOT_REQUIRED_MESSAGE)

        elif last_algorithm in [FIFOProcessScheduler, SJFProcessScheduler]:
            self.__entry_2.delete(0, "end")
            self.__entry_3.delete(0, "end")

        self.__label_2["fg"] = "black"
        self.__label_3["fg"] = "black"

        self.__menu_button_1.config(text = ["FIFO", "SJF", "RR", "EDF"][index])

    def __set_memory_algorithm(self, index: int):
        """
        Define o algorimo (classe) que será utilizado para paginação.
        """
        self.__paging_algorithm = [
            FIFOMemoryManager, LRUMemoryManager
        ][index]

        self.__menu_button_2.config(text = ["FIFO", "LRU"][index])

    def __validate_memory_scheduler_entry(self, string):
        """
        Valida a entrada do usuário nas Entrys relacionadas à memória.
        """
        for char in string:
            if char not in "0123456789": return False
        return True

    def __validate_process_scheduler_entry(self, string):
        """
        Valida a entrada do usuário nas Entrys relacionadas à CPU.
        """

        if self.__cpu_algorithm not in [RoundRobinProcessScheduler, EDFProcessScheduler]:
            if string == self.__NOT_REQUIRED_MESSAGE:
                return True
            if self.__NOT_REQUIRED_MESSAGE in string:
                return False

            self.__entry_2.delete(0, "end")
            self.__entry_3.delete(0, "end")

            self.__entry_2.insert(0, self.__NOT_REQUIRED_MESSAGE)
            self.__entry_3.insert(0, self.__NOT_REQUIRED_MESSAGE)
            return False

        for char in string:
            if char not in "0123456789": return False
        return True

    def build(self):
        """
        Constrói a parte gráfica da janela.
        """
        self["bg"] = "white"

        self.__main_frame = Frame(self)
        self.__main_frame["bg"] = "white"
        self.__main_frame.pack(pady = 20, padx = 20, expand = True, fill = "x")

        # Widgets para selecionar o algoritmo para escalonar os processos
        self.__frame_1 = Frame(self.__main_frame)
        self.__frame_1["bg"] = "white"
        self.__frame_1.pack(expand = True, fill = "x")

        self.__label_1 = Label(self.__frame_1, text = "Selecione o algoritmo de escalonamento:", bg = "white")
        self.__label_1.pack(side = "left")

        self.__menu_button_1 = Menubutton(self.__frame_1)
        self.__menu_button_1.pack(side = "left", expand = True, fill = "x")

        self.__menu_1 = Menu(tearoff = 0, bg = "white")

        self.__menu_1.add_command(label = "FIFO", command = lambda: self.__set_cpu_algorithm(0))
        self.__menu_1.add_command(label = "SJF", command = lambda: self.__set_cpu_algorithm(1))
        self.__menu_1.add_command(label = "RR", command = lambda: self.__set_cpu_algorithm(2))
        self.__menu_1.add_command(label = "EDF", command = lambda: self.__set_cpu_algorithm(3))

        self.__menu_button_1.config(menu = self.__menu_1, text = "FIFO")

        self.__entry_reg_1 = self.register(self.__validate_process_scheduler_entry)

        # Widgets para selecionar o quantum da CPU.
        self.__frame_2 = Frame(self.__main_frame)
        self.__frame_2["bg"] = "white"
        self.__frame_2.pack(pady = 10, expand = True, fill = "x")

        self.__label_2 = Label(self.__frame_2, text = "Quantum do processador (n > 0):", bg = "white")
        self.__label_2.pack(side = "left")

        self.__entry_2 = Entry(self.__frame_2, width = 4)
        self.__entry_2.config(validate="key", validatecommand=(self.__entry_reg_1, "%P"))
        self.__entry_2.insert(0, self.__NOT_REQUIRED_MESSAGE)
        self.__entry_2.pack(side = "left", expand = True, fill = "x")

        # Widgets para selecionar o chaveamento da CPU.
        self.__frame_3 = Frame(self.__main_frame)
        self.__frame_3["bg"] = "white"
        self.__frame_3.pack(expand = True, fill = "x")

        self.__label_3 = Label(self.__frame_3, text = "Tempo da sobrecarga (n > 0):", bg = "white")
        self.__label_3.pack(side = "left")

        self.__entry_3 = Entry(self.__frame_3, width = 4)
        self.__entry_3.config(validate="key", validatecommand=(self.__entry_reg_1, "%P"))
        self.__entry_3.insert(0, self.__NOT_REQUIRED_MESSAGE)
        self.__entry_3.pack(side = "left", expand = True, fill = "x")

        # Label para separar as configurações de processos (CPU) e memória.
        self.__separator = Label(self.__main_frame, background = "white")
        self.__separator.pack(pady = 10)

        # Widgets para selecionar o algoritmo para paginação.
        self.__frame_4 = Frame(self.__main_frame)
        self.__frame_4["bg"] = "white"
        self.__frame_4.pack(expand = True, fill = "x")

        self.__label_4 = Label(self.__frame_4, text = "Selecione o algoritmo de paginação:", bg = "white")
        self.__label_4.pack(side = "left")

        self.__menu_button_2 = Menubutton(self.__frame_4)
        self.__menu_button_2.pack(side = "left", expand = True, fill = "x")

        self.__menu_2 = Menu(tearoff = 0, bg = "white")
        self.__menu_2.add_command(label = "FIFO", command = lambda: self.__set_memory_algorithm(0))
        self.__menu_2.add_command(label = "LRU", command = lambda: self.__set_memory_algorithm(1))
        self.__menu_button_2.config(menu = self.__menu_2, text = "FIFO")

        self.__entry_reg_2 = self.register(self.__validate_memory_scheduler_entry)

        # Widgets para selecionar o tamanho da memória RAM.
        self.__frame_5 = Frame(self.__main_frame)
        self.__frame_5["bg"] = "white"
        self.__frame_5.pack(pady = 10, expand = True, fill = "x")

        self.__label_5 = Label(self.__frame_5, text = "Tamanho da Memória RAM (n > 0):", bg = "white")
        self.__label_5.pack(side = "left")

        self.__entry_4 = Entry(self.__frame_5, width = 4)
        self.__entry_4.config(validate = "key", validatecommand = (self.__entry_reg_2, "%P"))
        self.__entry_4.insert(0, str(self.__ram_memory_size))
        self.__entry_4.pack(side = "left", expand = True, fill = "x")

        # Widgets para selecionar o tamanho das páginas de memória.
        self.__frame_6 = Frame(self.__main_frame)
        self.__frame_6["bg"] = "white"
        self.__frame_6.pack(expand = True, fill = "x")

        self.__label_6 = Label(self.__frame_6, text = "Tamanho das páginas de memória (n > 0):", bg = "white")
        self.__label_6.pack(side = "left")

        self.__entry_5 = Entry(self.__frame_6, width = 4)
        self.__entry_5.config(validate = "key", validatecommand = (self.__entry_reg_2, "%P"))
        self.__entry_5.insert(0, str(self.__memory_page_size))
        self.__entry_5.pack(side = "left", expand = True, fill = "x")

        # Widgets para selecionar a quantidade de páginas por processo.
        self.__frame_7 = Frame(self.__main_frame)
        self.__frame_7["bg"] = "white"
        self.__frame_7.pack(pady = 10, expand = True, fill = "x")

        self.__label_7 = Label(self.__frame_7, text = "Quantidade de páginas por processo (n > 0):", bg = "white")
        self.__label_7.pack(side = "left")

        self.__entry_6 = Entry(self.__frame_7, width = 4)
        self.__entry_6.config(validate = "key", validatecommand = (self.__entry_reg_2, "%P"))
        self.__entry_6.insert(0, str(self.__page_per_process))
        self.__entry_6.pack(side = "left", expand = True, fill = "x")

        # Widgets para configuração de congelar um processo ou não quando uma de suas páginas não está na RAM.
        self.__frame_8 = Frame(self.__main_frame)
        self.__frame_8["bg"] = "white"
        self.__frame_8.pack(expand = True, fill = "x")
        self.__freeze_process = BooleanVar()

        self.__freeze_process_checkbutton = Checkbutton(
            self.__frame_8, text = "Congelar processo quando houver PageFault?",
            background = "white", variable = self.__freeze_process
        )
        self.__freeze_process_checkbutton.pack(side = "left")

        # Label para separar as configurações de memória das configurações gráficas.
        self.__separator_2 = Label(self.__main_frame, background = "white")
        self.__separator_2.pack()

        # Widgets para configurar a taxa de atualização do simulador.
        self.__frame_9 = Frame(self.__main_frame)
        self.__frame_9["bg"] = "white"
        self.__frame_9.pack(pady = 10, expand = True, fill = "x")

        self.__label_8 = Label(self.__frame_9, text = "Taxa de Atualização (ms > 0):", bg = "white")
        self.__label_8.pack(side = "left")

        self.__entry_7 = Entry(self.__frame_9, width = 4)
        self.__entry_7.config(validate = "key", validatecommand = (self.__entry_reg_2, "%P"))
        self.__entry_7.insert(0, str(self.__update_interval))
        self.__entry_7.pack(side = "left", expand = True, fill = "x")

        # Label para separar as configurações gráficas das configurações de geração de arquivo.
        self.__separator_3 = Label(self.__main_frame, background = "white")
        self.__separator_3.pack()

        # Widgets para configuração de geração de arquivo de log ou não.
        self.__frame_10 = Frame(self.__main_frame)
        self.__frame_10["bg"] = "white"
        self.__frame_10.pack(expand = True, fill = "x")

        self.__generate_log_file = BooleanVar()

        self.__generate_log_file_checkbutton = Checkbutton(
            self.__frame_10, text = "Gerar arquivo de log?",
            background = "white", variable = self.__generate_log_file
        )
        self.__generate_log_file_checkbutton.select()
        self.__generate_log_file_checkbutton.pack(side = "left")

        # Widgets para configuração de salvar as configurações ou não.
        self.__frame_11 = Frame(self.__main_frame)
        self.__frame_11["bg"] = "white"
        self.__frame_11.pack(expand = True, fill = "x")

        self.__save_config = BooleanVar()

        self.__save_config_checkbutton = Checkbutton(
            self.__frame_11, text = "Salvar configurações?",
            background = "white", variable = self.__save_config
        )
        self.__save_config_checkbutton.pack(side = "left")

        # Botão para sair do menu de configuração.
        self.__button = Button(
            self.__main_frame, text = "Iniciar", command = self.__finish_config,
            font = ("Arial", int(self.__size[0] * 0.06))
        )
        self.__button.pack(pady = 10, expand = True, fill = "x")

        # Carrega as informações do arquivo de configurações.
        self.__load_config_from_file()

    def get_freeze_process_config(self) -> bool:
        """
        Retorna um booleano indicando se o processo deve congelar ou não quando uma de suas páginas não estiverem na RAM.
        """
        return self.__freeze_process.get()

    def get_log_config(self) -> bool:
        """
        Retorna um booleano indicando se o arquivo de log deve ser gerado ou não.
        """
        return self.__generate_log_file.get()

    def get_memory_manager(self) -> MemoryManager:
        """
        Retorna o gerenciador de memória, com base nas configurações inseridas pelo usuário.
        """
        return self.__paging_algorithm(self.__ram_memory_size, self.__memory_page_size, self.__page_per_process)

    def get_process_scheduler(self) -> ProcessScheduler:
        """
        Retorna o escalonador, com base nas configurações inseridas pelo usuário.
        """
        return self.__cpu_algorithm(self.__quantum, self.__context_switching)

    def get_update_interval(self) -> int:
        """
        Retorna a taxa de atualização.
        """
        return self.__update_interval

    def run(self):
        """
        Executa a janela de menu.
        """
        self.mainloop()
