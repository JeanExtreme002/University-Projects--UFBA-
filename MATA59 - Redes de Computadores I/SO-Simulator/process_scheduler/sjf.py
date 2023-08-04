from typing import List, Optional, Tuple
from process_scheduler.abstract import ProcessScheduler
from process import Process


class SJFProcessScheduler(ProcessScheduler):

    __process_running = None

    @property
    def name(self) -> str:
        return "Shortest Job First (SJF)"

    def remove_process(self, process: Process):
        """
        Remove um processo.
        """
        super().remove_process(process)

        if process == self.__running:
            self.__process_running = None

    def run(self) -> Optional[Tuple[Optional[Process], Optional[List[Process]], bool]]:
        """
        Executa um processo.

        :return: Retorna o processo executado, uma lista com os processos em espera e um indicador de sobrecarga.
        """
        if not self.processes: return

        processes = self.processes
        process = self.__process_running

        # Se não houver processo em execução, ordena os processos pela duração e obtém o mais próximo de finalizar.
        if process is None:
            processes.sort(key = lambda process: process.duration)
            process = processes[0]

        process.run()
        self.__process_running = process

        if process.is_finished():
            self.remove_process(process)

        asleep_processes = list()

        for asleep_process in processes:
            if asleep_process.id != process.id:
                asleep_process.wait()
                asleep_processes.append(asleep_process)

        return process, asleep_processes, False
