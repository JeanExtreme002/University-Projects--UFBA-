from typing import Optional, Tuple, List
from process_scheduler.abstract import ProcessScheduler
from process import Process


class RoundRobinProcessScheduler(ProcessScheduler):

    __process_running = None
    __time_in_cpu = 0
    __context_switching_time = float("inf")

    __queue = []

    @property
    def name(self) -> str:
        return "Round Robin (RR)"

    def add_process(self, process: Process):
        """
        Adiciona um processo.
        """
        super().add_process(process)
        self.__queue.append(process)

    def remove_process(self, process: Process):
        """
        Remove um processo.
        """
        super().remove_process(process)
        self.__queue.remove(process)

    def run(self) -> Optional[Tuple[Optional[Process], Optional[List[Process]], bool]]:
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

            self.__queue = self.__queue[1:] + [self.__queue[0]]
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
