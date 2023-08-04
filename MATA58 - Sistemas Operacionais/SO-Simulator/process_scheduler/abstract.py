from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from process import Process


class ProcessScheduler(ABC):
    def __init__(self, quantum: Optional[int] = None, context_switching: Optional[int] = None):
        self.__process_list = list()
        self.__quantum = quantum
        self.__context_switching = context_switching

    def __len__(self) -> int:
        return len(self.__process_list)
    
    @property
    def name(self) -> str:
        return str()

    @property
    def processes(self) -> List[Process]:
        return self.__process_list.copy()

    @property
    def quantum(self):
        return self.__quantum

    @property
    def context_switching(self):
        return self.__context_switching

    def add_process(self, process: Process):
        """
        Adiciona um processo.
        """
        self.__process_list.append(process)

    def remove_process(self, process: Process):
        """
        Remove um processo.
        """
        self.__process_list.remove(process)

    @abstractmethod
    def run(self) -> Optional[Tuple[Optional[Process], Optional[List[Process]], bool]]:
        """
        Executa um processo.

        :return: Retorna o processo executado, uma lista com os processos em espera e um indicador de sobrecarga.
        """
        pass

