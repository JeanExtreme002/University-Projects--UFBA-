from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from process import Process

import time


class MemoryManager(ABC):
    def __init__(self, ram_memory_size: int, page_size: int, page_per_process: Optional[int] = None):
        self.__ram_memory_size = ram_memory_size
        self.__page_size = page_size
        self.__page_per_process = page_per_process

        self.__ram_memory_pages = ram_memory_size // page_size

        self._real_memory_table: List[Tuple[Optional[Process], Any, datetime, datetime]] = [  # Lista de (Processo, Valor, Tempo de Criação, Tempo do Último uso)
            (None, None, datetime.now(), datetime.now()) for i in range(self.__ram_memory_pages)
        ]
        self._virtual_memory_table: Dict[Tuple[int, int], Optional[int]] = dict()  # {(<ID Processo>, VMEM_ADDRESS) : RMEM_ADDRESS}        
        self.__incremented_virtual_page_address = 0

    @property
    def name(self) -> str:
        return ""

    @property
    def ram_memory_pages(self) -> int:
        return self.__ram_memory_pages

    @property
    def ram_memory_size(self) -> int:
        return self.__ram_memory_size

    @property
    def page_size(self) -> int:
        return self.__page_size

    @property
    def page_per_process(self) -> int:
        return self.__page_per_process

    def _set_real_page(self, process: Optional[Process], real_memory_address: int):
        """
        Define um processo à uma página de memória real em uma dado endereço.
        """
        self._real_memory_table[real_memory_address] = (process, None, datetime.now(), datetime.now())
        self._use(process, real_memory_address)

        time.sleep(0.01)  # Garante que todas as páginas possuirão um tempo de criação diferente.

    def _use(self, process: Process, real_memory_address: int, new_value: Optional[Any] = None) -> Any:
        """
        Utiliza uma página de memória em uma dado endereço, retornando
        o seu valor atual e escrevendo algo no espaço.
        """
        registered_process, value, created_at, last_used_at = self._real_memory_table[real_memory_address]

        if process.id != registered_process.id:
            raise ValueError("Illegal access for this memory page.")

        if new_value is not None: self._real_memory_table[real_memory_address] = (process, new_value, created_at, datetime.now())
        else: self._real_memory_table[real_memory_address] = (process, value, created_at, datetime.now())

        return value

    def alloc_memory(self, process: Process, memory: int, *, dry_run: bool = False) -> List[int]:
        """
        Aloca um espaço na memória para o processo.

        :param dry_run: Apenas verifica se seria possível alocar mais memória para o processo.
        """        
        memory_addresses = []

        total_used = memory + sum([self.page_size for pid, vmem_addr in self._virtual_memory_table if pid == process.id])

        # Idealmente a verificação abaixo não deveria existir. Só existe porque um processo não roda se alguma página não estiver na RAM.
        if total_used > self.page_per_process * self.page_size or total_used > self.__ram_memory_pages * self.page_size:
            raise OverflowError("Max amount of memory page exceeded.")
        
        if dry_run:
            return list()

        while memory > 0:
            virtual_address = self.__incremented_virtual_page_address
            self.__incremented_virtual_page_address += 1

            self._virtual_memory_table[(process.id, virtual_address)] = None
            memory_addresses.append(virtual_address)

            memory -= self.page_size
        return memory_addresses

    def free_memory(self, process: Process):
        """
        Libera a memória utiliza por um processo.
        """
        keys = list()
        
        for key, value in self._virtual_memory_table.items():
            if key[0] == process.id and value is not None:
                self._real_memory_table[value] = (process, None, datetime.now(), datetime.now())
                keys.append(key)

        for key in keys:
            self._virtual_memory_table.pop(key)
            
    def get_virtual_memory_table(self) -> List[Tuple[id, id, Optional[int], Optional[str]]]:
        """
        Retorna uma lista contendo tuplas no formato (Process ID, Virtual Memory ID, Real Memory ID, Último Uso).
        """
        table: List[Tuple[id, id, Optional[int], Optional[str]]] = list()

        for key, value in self._virtual_memory_table.items():
            last_used_at = None
            
            if value is not None:
                last_used_at = self._real_memory_table[value][-1]
                last_used_at = last_used_at.strftime("%d/%m/%Y %H:%M:%S")
            table.append((key[0], key[1], value, last_used_at))
            
        return table

    def has_page_fault(self, process: Process):
        """
        Verifica se um dado processo possui páginas que não estão na memória principal.
        """
        for key, value in self._virtual_memory_table.items():
            if key[0] == process.id and value is None:
                return True
        return False

    @abstractmethod
    def use(self, process: Process, memory_page_address: int):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        pass
