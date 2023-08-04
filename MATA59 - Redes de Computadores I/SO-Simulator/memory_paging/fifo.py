from typing import List
from memory_paging import MemoryManager
from process import Process


class FIFOMemoryManager(MemoryManager):

    @property
    def name(self) -> str:
        return "First In First Out (FIFO)"

    def alloc_memory(self, process: Process, memory: int, **kwargs) -> List[int]:
        """
        Aloca um espaço na memória para o processo.
        """
        virtual_page_addresses = super().alloc_memory(process, memory, **kwargs)

        for address in virtual_page_addresses:
            self.use(process, address)

        return virtual_page_addresses

    def use(self, process: Process, virtual_page_address: int):
        """
        Utiliza uma página de memória em uma dado endereço.
        """
        if (process.id, virtual_page_address) not in self._virtual_memory_table:
            raise ValueError("Invalid memory address.")

        # Se a página já estiver na RAM, a mesma será utilizada e nada além disso será feito.
        if self._virtual_memory_table[(process.id, virtual_page_address)] is not None:
            return self._use(process, self._virtual_memory_table[(process.id, virtual_page_address)])

        # Verifica se existe espaço livre na memória RAM e define a página para o processo.
        for real_address in range(len(self._real_memory_table)):
            if self._real_memory_table[real_address][0] is None:
                self._virtual_memory_table[(process.id, virtual_page_address)] = real_address
                return self._set_real_page(process, real_address)

        # Sobrescreve a página mais antiga criada.
        sorted_real_memory_table = sorted(self._real_memory_table, key = lambda page: page[2])

        for real_address in range(len(self._real_memory_table)):
            if self._real_memory_table[real_address] == sorted_real_memory_table[0]:

                # Apaga a referência da página de memória virtual que está atualmente na RAM.
                for key, value in self._virtual_memory_table.items():
                    if key[0] == sorted_real_memory_table[0][0].id and value == real_address:
                        self._virtual_memory_table[key] = None
                        break

                # Define a referência para a página de memória virtual utilizada.
                self._virtual_memory_table[(process.id, virtual_page_address)] = real_address
                return self._set_real_page(process, real_address)
