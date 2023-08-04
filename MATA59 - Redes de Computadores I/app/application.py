from tkinter import Button, BooleanVar, Canvas, Checkbutton, Entry, Frame, Label, Listbox, Scrollbar, Tk
from typing import List, Optional, Tuple

from app.real_memory_window import RealMemoryWindow
from app.virtual_memory_window import VirtualMemoryWindow
from memory_paging import MemoryManager
from process import Process
from process_scheduler import ProcessScheduler
from process_scheduler.edf import EDFProcessScheduler

import random


class Application(Tk):
    """
    Classe principal da aplicação.
    """

    def __init__(
        self,
        title: str = "Window",
        real_memory_window_title: str = "Window",
        virtual_memory_window_title: str = "Window",
        size: tuple[int] = (1280, 720)
    ):
        super().__init__()

        self.__title = title
        self.__real_memory_window_title = real_memory_window_title
        self.__virtual_memory_window_title = virtual_memory_window_title

        self.__size = size
        self.__paused = False

        self.__generate_log_file = False
        self.__log_filename = "process_log.txt"

        self.__history_length = 20
        self.__history_border = 1
        self.__history_min_rows = 6

        self.__process_history = []
        self.__process_list = []
        self.__process_count = 0
        
        self.__scheduled_processes: List[List[Process, int, int]] = []  # Lista de [Process, memory, time]

        self.__last_process_list_length = self.__history_min_rows

        self.__old_execution_time_list: List[int] = list()

        self.title(title)
        self.resizable(False, False)
        self.geometry("{}x{}".format(*size))

    def __add_memory(self):
        """
        Adiciona mais memória à um processo existente.
        """
        process_id = self.__process_id_entry.get()
        memory = self.__extra_memory_entry.get()

        self.__process_id_label.config(foreground = "black")
        self.__extra_memory_label.config(foreground = "black")

        if not memory: return self.__extra_memory_label.config(foreground = "red")
        if not process_id: return self.__process_id_label.config(foreground = "red")

        # Verifica se o processo existe e não está morto ou terminou.
        for process in self.__process_list:
            if process.id == int(process_id) and not process.has_died() and not process.is_finished(): break
        else: return self.__process_id_label.config(foreground="red")

        try: self.__memory_manager.alloc_memory(process, int(memory))
        except OverflowError: return self.__extra_memory_label.config(foreground = "red")

        self.__real_memory_window.update_table()
        self.__virtual_memory_window.update_table()

    def __add_process(self, process: Process, memory: int):
        """
        Adiciona uma instância de processo para o simulador.
        """
        process.index = len(self.__process_history)

        try: self.__memory_manager.alloc_memory(process, memory)
        except OverflowError: return self.__memory_label.config(foreground = "red")

        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        process.color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

        self.__process_scheduler.add_process(process)
        self.__process_history.append([None] * self.__history_length)

        self.__process_list.append(process)
        
        self.__real_memory_window.update_table()
        self.__virtual_memory_window.update_table()

    def __add_new_process(self):
        """
        Adiciona um novo processo para o simulador.
        """
        duration = self.__duration_entry.get()
        deadline = self.__deadline_entry.get()
        memory = self.__memory_entry.get()
        schedule = self.__schedule_entry.get()

        if not duration or not duration.replace("0", ""): return self.__duration_label.config(foreground = "red")
        if not memory: return self.__memory_label.config(foreground = "red")
        if not schedule: return self.__schedule_label.config(foreground = "red")
        if deadline and not deadline.replace("0", ""): return

        if not deadline and isinstance(self.__process_scheduler, EDFProcessScheduler):
            return self.__deadline_label.config(foreground = "red")

        self.__duration_label.config(foreground = "black")
        self.__memory_label.config(foreground = "black")
        self.__schedule_label.config(foreground = "black")
        self.__deadline_label.config(foreground="black")

        duration = int(duration)
        deadline = int(deadline) if deadline else None
        memory = int(memory)
        schedule = int(schedule)

        process = Process(
            process_id = self.__process_count,
            duration = duration,
            deadline = deadline,
            ignore_deadline_error = True,
            is_critical = self.__is_critical.get()
        )

        self.__process_count += 1

        if schedule > 0:
            try:
                self.__memory_manager.alloc_memory(process, memory, dry_run = True)
                self.__scheduled_processes.append([process, memory, schedule])
            except OverflowError:
                return self.__memory_label.config(foreground = "red")
        else:
            self.__add_process(process, memory)


    def __append_to_log_file(self, string):
        """
        Adiciona ao arquivo de log uma string em uma linha.
        """
        with open(self.__log_filename, "a+", encoding = "UTF-8") as file:
            file.write(string + "\n")

    def __draw_grid(self, length: int):
        """
        Desenha um grid na tela de histórico.
        """
        length = max(length, self.__history_min_rows)

        process_width, process_height = self.__get_process_size_on_history(length)

        for y in range(length - 1):
            for x in range(self.__history_length - 1):

                self.__canvas.create_rectangle(
                    process_width * x + self.__history_border * x + process_width, 0,
                    process_width * x + self.__history_border * x + process_width + self.__history_border, self.__canvas_height + 10,
                    fill="black"
                )
            self.__canvas.create_rectangle(
                0, process_height * y + self.__history_border * y + process_height,
                self.__canvas_width + 10, process_height * y + self.__history_border * y + process_height + self.__history_border,
                fill="black"
            )

    def __get_process_size_on_history(self, length: int) -> Tuple[int, int]:
        """
        Calcula a largura e altura do processo para a tela de histórico.
        """
        length = max(length, self.__history_min_rows)

        process_width = (self.__canvas_width - self.__history_border * (self.__history_length - 1)) / self.__history_length
        process_height = (self.__canvas_height - self.__history_border * (length - 1)) / length

        return int(process_width), int(process_height)

    def __on_update(self):
        """
        Evento executado periodicamente pela interface gráfica.
        """
        if self.__paused:
            return self.after(self.__on_update_interval, self.__on_update)

        self.__canvas.delete("all")

        # Verifica se algum processo agendado já pode ser adicionado ao simulador.
        added_processes = []
        
        for index in range(len(self.__scheduled_processes)):
            process, memory, time = self.__scheduled_processes[index]
            self.__scheduled_processes[index][-1] -= 1
            
            if time == 0:
                self.__add_process(process, memory)
                added_processes.append(self.__scheduled_processes[index])

        for value in added_processes:
            self.__scheduled_processes.remove(value)

        # Se não houver mais processos para serem mostrados, apenas a grade será desenhada.
        if len(self.__process_history) == 0 and not self.__scheduled_processes:
            self.__draw_grid(self.__last_process_list_length)
            return self.after(self.__on_update_interval, self.__on_update)

        # Verifica os processo que estão congelados ou não.
        if self.__freeze_process_on_page_fault:
            for process in self.__process_list:
                process.set_freeze(self.__memory_manager.has_page_fault(process))

        # Executa o próximo processo.
        result = self.__process_scheduler.run()
        process, asleep_processes, context_switching = (result[0], result[1], result[2]) if result is not None else (None, None, None)

        # Adiciona o chaveamento realizado ao histórico.
        if context_switching:
            self.__process_history[process.index][self.__history_length - 1] = ("switch", "#333")

        # Adiciona o estado do processo ao histórico.
        elif process and (not process.has_died() or not process.is_critical):

            # Caso o processo tenha o seu deadline expirado, a sua cor passará a ser uma variação de vermelho.
            if process.has_died() and not process.color.endswith("0000"):
                r, g, b = (random.randint(180, 255), 0, 0)
                process.color = f"#{r:02x}{g:02x}{b:02x}"

            # Libera a memória utilizada pelo processo.
            if process.is_finished():
                self.__memory_manager.free_memory(process)
                self.__real_memory_window.update_table()
                self.__virtual_memory_window.update_table()

            self.__process_history[process.index][self.__history_length - 1] = (process.id, process.color)

        elif process and process.has_died() and process.is_critical:
            return self.__on_update()

        # Remove processos que já saíram do histórico.
        for process in self.__process_list.copy():
            if process.is_finished() and not any(self.__process_history[process.index]):
                self.__old_execution_time_list.append(process.get_absolute_duration())
                self.__remove_process(process)

        # Atualiza o Listbox com as informações dos processos.
        self.__process_list_box.delete(0, "end")

        for process in sorted(self.__process_list, key = lambda process: process.id, reverse = True):
            if result and process.id == result[0].id: state = f"em execução e restando {process.duration}s para terminar"
            elif process.is_finished(): state = "finalizado"
            else: state = f"em espera e restando {process.duration}s para terminar"

            string = f"Processo ID:{process.id} está {state}. "

            if process.has_died():
                string += "O deadline foi atingido!"

            elif not process.is_finished() and process.deadline is not None:
                string += f"Falta {process.deadline}s do deadline para expirar."

            if self.__generate_log_file: self.__append_to_log_file(string)
            self.__process_list_box.insert(0, string)

        for process, memory, time in self.__scheduled_processes:
            string = f"Processo ID:{process.id} será adicionado à fila de processos em {time}s"
            
            if self.__generate_log_file: self.__append_to_log_file(string)
            self.__process_list_box.insert("end", string)            

        if self.__generate_log_file: self.__append_to_log_file("=" * 80)

        # Calcula a largura e altura correta dos processos.
        process_width, process_height = self.__get_process_size_on_history(len(self.__process_history))
        self.__last_process_list_length = len(self.__process_history)

        # Mostra o histórico de todos os processos, até um dado momento, no canvas.
        for y in range(len(self.__process_history)):
            for x in range(self.__history_length):
                element = self.__process_history[y][x]

                if type(element) is tuple:
                    color = element[1]
                else: continue

                # Calcula o X1 do processo.
                x1 = process_width * x + self.__history_border * x

                # Calcula o Y1 do processo.
                y1 = process_height * y + self.__history_border * y

                # Calcula o X2 do processo (X1 + width).
                x2 = process_width * x + self.__history_border * x + process_width

                if x == self.__history_length - 1:
                    x2 = self.__canvas_width + 10

                # Calcula o Y2 do processo (X2 + height).
                y2 = process_height * y + self.__history_border * y + process_height

                if y == len(self.__process_history) - 1 and y >= self.__history_min_rows - 1:
                    y2 = self.__canvas_height + 10

                # Desenha o processo com o seu ID.
                self.__canvas.create_rectangle(x1, y1, x2, y2, fill = color)
                self.__canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text = element[0])

        self.__draw_grid(self.__last_process_list_length)

        # Move o histórico para a esquerda e atualiza o tempo médio de execução dos processos.
        self.__shift_process_history()
        self.__update_average_execution_time()

        # Repete a execução do método, após um determinado tempo.
        self.after(self.__on_update_interval, self.__on_update)

    def __remove_process(self, process: Process):
        """
        Remove um processo do simulador.
        """
        new_process_list = list()

        for p in self.__process_list:
            if p is not process:
                if p.index > process.index:
                    p.index -= 1
                new_process_list.append(p)

        self.__process_list = new_process_list
        self.__process_history = self.__process_history[:process.index] + self.__process_history[process.index + 1:]

    def __shift_process_history(self):
        """
        Move o histórico dos processos para a esquerda.
        """
        for y in range(len(self.__process_history)):
            for x in range(self.__history_length - 1):
                self.__process_history[y][x] = self.__process_history[y][x + 1]
            self.__process_history[y][self.__history_length - 1] = None

    def __update_average_execution_time(self):
        """
        Atualiza o tempo médio de execução dos processos.
        """
        average_execution_time = sum(self.__old_execution_time_list)
        average_execution_time += sum([process.get_absolute_duration() for process in self.__process_list])

        total = (len(self.__old_execution_time_list) + len(self.__process_list))

        average_execution_time = (average_execution_time / total) if total > 0 else 0.0
        average_execution_time = round(average_execution_time, 2)

        self.__average_execution_time_label.config(text = "Tempo Médio de Execução: " + str(average_execution_time))

    def __use_memory_page(self):
        """
        Utiliza uma página de memória de um processo.
        """
        process_id = self.__use_process_id_entry.get()
        page_address = self.__memory_address_entry.get()

        self.__use_process_id_label.config(foreground = "black")
        self.__memory_address_label.config(foreground = "black")

        if not process_id:
            return self.__use_process_id_label.config(foreground = "red")

        if not page_address:
            return self.__memory_address_label.config(foreground = "red")

        # Verifica se o processo existe.
        for process in self.__process_list:
            if process.id == int(process_id): break
        else: return self.__use_process_id_label.config(foreground="red")

        try: self.__memory_manager.use(process, int(page_address))
        except ValueError: return self.__memory_address_label.config(foreground = "red")

        self.__real_memory_window.update_table()
        self.__virtual_memory_window.update_table()

    def __validate_entry(self, string):
        """
        Valida a entrada do usuário na Entry.
        """
        for char in string:
            if char not in "0123456789": return False
        return True

    def build(self):
        """
        Constrói a parte gráfica da janela.
        """
        self["bg"] = "white"
        button_width = int(self.__size[0] * 0.014)

        self.__main_frame = Frame(self)
        self.__main_frame["bg"] = "white"
        self.__main_frame.pack(padx = 10, pady = 10, expand = True, fill = "x")

        # Widgets para mostrar o histórico.
        self.__canvas_label_frame = Frame(self.__main_frame)
        self.__canvas_label_frame["bg"] = "white"
        self.__canvas_label_frame.pack(padx = 10, expand = True, fill ="x")

        self.__canvas_label = Label(
            self.__canvas_label_frame, text ="Histórico do estado dos processos (por segundo).",
            background = "white"
        )
        self.__canvas_label.pack(side = "left")

        # Cria widget para mostrar o tempo médio de execução dos processo.
        self.__average_execution_time_label = Label(self.__canvas_label_frame, background = "white")
        self.__update_average_execution_time()
        self.__average_execution_time_label.pack(side = "right")

        self.__canvas_width = (
            self.__size[0] * 0.95 - (self.__size[0] * 0.95 % self.__history_length)
            + self.__history_border * (self.__history_length - 1)
        )
        self.__canvas_height = self.__size[1] * 0.5

        self.__canvas = Canvas(
            self.__main_frame, width = self.__canvas_width, height = self.__canvas_height,
            borderwidth = 2, background = "white", relief = "solid"
        )
        self.__draw_grid(self.__last_process_list_length)
        self.__canvas.pack(pady = 10)

        # Widgets para mostrar a lista de processos e seus estados em texto.
        self.__process_list_label_frame = Frame(self.__main_frame)
        self.__process_list_label_frame["bg"] = "white"
        self.__process_list_label_frame.pack(padx = 10, expand = True, fill ="x")

        self.__process_list_label = Label(
            self.__process_list_label_frame, text ="Processos:",
            background = "white"
        )
        self.__process_list_label.pack(side = "left")

        self.__process_list_frame = Frame(self.__main_frame)
        self.__process_list_frame["bg"] = "white"
        self.__process_list_frame.pack(padx = 13, expand = True, fill ="x")

        self.__process_list_box = Listbox(self.__process_list_frame, height = self.__history_min_rows + 2)
        self.__process_list_box.pack(side = "left", expand = True, fill ="x")

        self.__process_list_box_scrollbar = Scrollbar(self.__process_list_frame)
        self.__process_list_box_scrollbar.pack(side = "right", fill = "both")
        self.__process_list_box.config(yscrollcommand= self.__process_list_box_scrollbar.set)

        # Frame para inserir widgets relacionados à entrada do usuário.
        self.__input_frame = Frame(self.__main_frame)
        self.__input_frame["bg"] = "white"
        self.__input_frame.pack(side = "left", expand = True, fill = "x")

        # Widgets para receber as entradas do usuário para adicionar um novo processo.
        self.__add_new_process_frame = Frame(self.__input_frame)
        self.__add_new_process_frame["bg"] = "white"
        self.__add_new_process_frame.pack(padx = 10, pady = 10, expand = True, fill = "x")

        self.__add_new_process_button = Button(
            self.__add_new_process_frame, text = "Adicionar Processo", width = button_width,
            command = self.__add_new_process, background = "lightgreen"
        )
        self.__add_new_process_button.pack(padx = 10, side = "left")

        self.__duration_frame = Frame(self.__add_new_process_frame)
        self.__duration_frame["bg"] = "white"
        self.__duration_frame.pack(side = "left", padx = 10)

        self.__duration_label = Label(self.__duration_frame, text = "Duração: ", background = "white")
        self.__duration_label.pack(side = "left")

        self.__entry_reg = self.register(self.__validate_entry)

        self.__duration_entry = Entry(self.__duration_frame)
        self.__duration_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__duration_entry.pack(side = "left")

        self.__deadline_label = Label(self.__add_new_process_frame, text="Deadline: ", background = "white")
        self.__deadline_label.pack(side="left")

        self.__deadline_entry = Entry(self.__add_new_process_frame)
        self.__deadline_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__deadline_entry.pack(side="left")

        self.__memory_label = Label(self.__add_new_process_frame, text="Memória: ", background = "white")
        self.__memory_label.pack(side="left")

        self.__memory_entry = Entry(self.__add_new_process_frame)
        self.__memory_entry.insert(0, "0")
        self.__memory_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__memory_entry.pack(side="left")

        self.__schedule_label = Label(self.__add_new_process_frame, text="Agendar: ", background = "white")
        self.__schedule_label.pack(side="left")

        self.__schedule_entry = Entry(self.__add_new_process_frame)
        self.__schedule_entry.insert(0, "0")
        self.__schedule_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__schedule_entry.pack(side="left")

        self.__is_critical = BooleanVar()

        self.__critical_checkbutton = Checkbutton(
            self.__add_new_process_frame, text = "Regime Crítico?",
            background = "white", variable = self.__is_critical
        )
        self.__critical_checkbutton.pack(side="left")

        # Widgets para receber as entradas do usuário para adicionar memória à um processo.
        self.__add_memory_frame = Frame(self.__input_frame)
        self.__add_memory_frame["bg"] = "white"
        self.__add_memory_frame.pack(padx = 10, pady = 10, expand = True, fill = "x")

        self.__add_memory_button = Button(
            self.__add_memory_frame, text = "Adicionar Memória", width = button_width,
            command = self.__add_memory, background = "lightblue"
        )
        self.__add_memory_button.pack(padx = 10, side = "left")

        self.__process_id_frame = Frame(self.__add_memory_frame)
        self.__process_id_frame["bg"] = "white"
        self.__process_id_frame.pack(side = "left", padx = 10)

        self.__process_id_label = Label(self.__process_id_frame, text = "ID do Processo: ", background = "white")
        self.__process_id_label.pack(side = "left")

        self.__process_id_entry = Entry(self.__process_id_frame)
        self.__process_id_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__process_id_entry.pack(side = "left")

        self.__extra_memory_frame = Frame(self.__add_memory_frame)
        self.__extra_memory_frame["bg"] = "white"
        self.__extra_memory_frame.pack(side = "left", padx = 10)

        self.__extra_memory_label = Label(self.__extra_memory_frame, text = "Memória Extra: ", background = "white")
        self.__extra_memory_label.pack(side = "left")

        self.__extra_memory_entry = Entry(self.__extra_memory_frame)
        self.__extra_memory_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__extra_memory_entry.pack(side = "left")

        # Widgets para receber as entradas do usuário para usar uma dada página de um processo.
        self.__use_memory_frame = Frame(self.__input_frame)
        self.__use_memory_frame["bg"] = "white"
        self.__use_memory_frame.pack(padx = 10, pady = 10, expand = True, fill = "x")

        self.__use_memory_button = Button(
            self.__use_memory_frame, text = "Usar Página", width = button_width,
            command = self.__use_memory_page, background = "orange"
        )
        self.__use_memory_button.pack(padx = 10, side = "left")

        self.__use_process_id_frame = Frame(self.__use_memory_frame)
        self.__use_process_id_frame["bg"] = "white"
        self.__use_process_id_frame.pack(side = "left", padx = 10)

        self.__use_process_id_label = Label(self.__use_process_id_frame, text = "ID do Processo: ", background = "white")
        self.__use_process_id_label.pack(side = "left")

        self.__use_process_id_entry = Entry(self.__use_process_id_frame)
        self.__use_process_id_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__use_process_id_entry.pack(side = "left")

        self.__use_memory_frame = Frame(self.__use_memory_frame)
        self.__use_memory_frame["bg"] = "white"
        self.__use_memory_frame.pack(side = "left", padx = 10)

        self.__memory_address_label = Label(self.__use_memory_frame, text = "Endereço da Página Virtual: ", background = "white")
        self.__memory_address_label.pack(side = "left")

        self.__memory_address_entry = Entry(self.__use_memory_frame)
        self.__memory_address_entry.config(validate="key", validatecommand=(self.__entry_reg, "%P"))
        self.__memory_address_entry.pack(side = "left")

        # # Cria botão para controlar a execução do simulador.
        self.__control_frame = Frame(self.__main_frame)
        self.__control_frame["bg"] = "white"
        self.__control_frame.pack(side = "left", expand = True, fill = "x")

        self.__control_button = Button(
            self.__control_frame, text = "Pausar Simulação",
            width = button_width, background = "#ff6961",
            command = self.switch_simulation_status
        )
        self.__control_button.pack()

    def switch_simulation_status(self, pause: Optional[bool] = None):
        """
        Pausa a simulação.
        """
        if pause is None: self.__paused = not self.__paused
        else: self.__paused = pause

        self.__control_button.config(background="#87cefa" if self.__paused else "#ff6961")
        self.__control_button.config(text="Continuar Simulação" if self.__paused else "Pausar Simulação")

    def run(
        self,
        process_scheduler: ProcessScheduler,
        memory_manager: MemoryManager,
        interval: int = 1000,
        freeze_process_on_page_fault: bool = False,
        generate_log_file: bool = False
    ):
        """
        Executa a aplicação principal, com sua parte gráfica.
        """
        self.__process_scheduler = process_scheduler
        self.__memory_manager = memory_manager

        self.__on_update_interval = interval
        self.__freeze_process_on_page_fault = freeze_process_on_page_fault
        self.__generate_log_file = generate_log_file

        self.__real_memory_window = RealMemoryWindow(self.__real_memory_window_title)
        self.__real_memory_window.build(memory_manager)

        self.__virtual_memory_window = VirtualMemoryWindow(self.__virtual_memory_window_title)
        self.__virtual_memory_window.build(memory_manager)

        self.after(self.__on_update_interval, self.__on_update)
        self.mainloop()
