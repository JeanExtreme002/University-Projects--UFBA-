from typing import List, Optional, Tuple
from process_scheduler.abstract import ProcessScheduler
from process import Process


class FIFOProcessScheduler(ProcessScheduler):

    @property
    def name(self) -> str:
        return "First In First Out (FIFO)"
    
    def run(self) -> Optional[Tuple[Optional[Process], Optional[List[Process]], bool]]:
        """
        Executa um processo.

        :return: Retorna o processo executado, uma lista com os processos em espera e um indicador de sobrecarga.
        """
        if not self.processes: return

        process = self.processes[0]
        process.run()

        if process.is_finished():
            self.remove_process(process)

        asleep_processes = self.processes[1:]

        for asleep_process in asleep_processes:
            asleep_process.wait()

        return process, asleep_processes, False
