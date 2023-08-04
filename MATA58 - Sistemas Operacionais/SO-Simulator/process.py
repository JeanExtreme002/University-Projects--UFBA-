from typing import Optional


class Process(object):
    """
    Representa um processo no sistema operacional.
    """

    def __init__(self, process_id: int, duration: int, deadline: Optional[int] = None, ignore_deadline_error: bool = False, is_critical: bool = False):
        """
        :param duration: Duração para o processo executar completamente na CPU.
        :param deadline: Tempo em que o processo necessita ser executado completamente.
        :param ignore_deadline_error: Se False, os métodos run() e wait() irão gerar um erro caso o deadline seja expirado.
        :param is_critical: Define se o processo deve terminar ou não ao ter seu deadline expirado.
        """
        self.__id = process_id
        self.__duration = duration
        self.__deadline = deadline
        self.__ignore_deadline_error = ignore_deadline_error
        self.__is_critical = is_critical

        self.__absolute_duration = 0
        self.__is_frozen = False

    def __str__(self):
        return f"<Process: {self.id}>"

    @property
    def id(self) -> int:
        return self.__id

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def deadline(self) -> int:
        return self.__deadline

    @property
    def is_critical(self) -> int:
        return self.__is_critical

    def get_absolute_duration(self) -> int:
        """
        Retorna o tempo total que o processo ficou esperando ou executando.
        """
        return self.__absolute_duration

    def is_finished(self) -> bool:
        """
        Verifica se o processo encerrou completamente.
        """
        return self.__duration <= 0 or (self.has_died() and self.__is_critical)

    def is_frozen(self) -> bool:
        """
        Verifica se o processo está congelado.
        """
        return self.__is_frozen

    def has_died(self) -> bool:
        """
        Verifica se o tempo do deadline foi excedido.
        """
        if self.__deadline is None: return False
        return self.__deadline < 0

    def run(self, time: int = 1):
        """
        Executa o processo.
        :param time: tempo em que o processo permaneceu na CPU.
        
        :raises: TimeoutError se o tempo do deadline for excedido.
        """
        if not self.__is_frozen: self.__duration -= time
        self.wait(time)

    def set_freeze(self, freeze: bool):
        """
        Congela ou descongela o processo.
        """
        self.__is_frozen = freeze

    def wait(self, time: int = 1):
        """
        Informa que o processo deve esperar.
        :param time: tempo em que o processo espera.

        :raises: TimeoutError se o tempo do deadline for excedido.
        """
        self.__absolute_duration += time

        if self.__deadline is None:
            return

        self.__deadline -= time

        if self.has_died() and not self.__ignore_deadline_error:
            raise TimeoutError("The process is over!")
