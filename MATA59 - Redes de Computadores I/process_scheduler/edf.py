from typing import Optional, Tuple, List
from process_scheduler.abstract import ProcessScheduler
from process import Process


class EDFProcessScheduler(ProcessScheduler):

    __process_running = None
    __time_in_cpu = 0
    __context_switching_time = float("inf")

    __queue = []

    @property
    def name(self) -> str:
        return "Earliest Deadline First (EDF)"

    def run(self) -> Optional[Tuple[Optional[Process], Optional[List[Process]], bool]]:
        """
        Executa um processo.

        :return: Retorna o processo executado, uma lista com os processos em espera e um indicador de sobrecarga.
        """
        if len(self.processes) == 0: return

        # Verifica se o processo já ficou pelo tempo máximo que a CPU permite. Se sim,
        # será realizado a troca de processo.
        if (self.__time_in_cpu % self.quantum) == 0:

            # Realiza o chaveamento.
            if self.__context_switching_time < self.context_switching:
                self.__context_switching_time += 1

                for process in self.processes:
                    process.wait()

                return self.__process_running, self.__queue[1:], True

            self.__queue = self.processes.copy()
            self.__queue.sort(key = lambda process: process.deadline - process.duration)

            self.__process_running = self.__queue[0]
            self.__context_switching_time = 0

        # Executa o processo.
        process = self.__process_running
        process.run()

        self.__time_in_cpu += 1

        if process.is_finished():
            self.remove_process(process)
            self.__context_switching_time = float("inf")
            self.__time_in_cpu = 0

        asleep_processes = list()

        for asleep_process in self.processes:
            if asleep_process.id != process.id:
                asleep_process.wait()
                asleep_processes.append(asleep_process)

        return process, asleep_processes, False
