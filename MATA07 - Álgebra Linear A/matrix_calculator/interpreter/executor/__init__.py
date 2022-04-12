from ..parser import parse_instruction
from .application_operation import ApplicationOperationExecutor
from .arithmetic_operation import ArithmeticOperationExecutor
from .elementary_operation import ElementaryOperationExecutor
from .matrix_operation import MatrixOperationExecutor

__all__ = ("Executor",)

class Executor(object):
    def __init__(self, core):
        self.__core = core

        self.__application_op_executor = ApplicationOperationExecutor(core)
        self.__arithmetic_op_executor = ArithmeticOperationExecutor(core)
        self.__elementary_op_executor = ElementaryOperationExecutor(core)
        self.__matrix_op_executor = MatrixOperationExecutor(core)
        
    def execute(self, instruction):
        """
        Executa uma instrução.
        """
        instruction = parse_instruction(instruction)
        
        options = {
            "application": self.__application_op_executor,
            "arithmetic": self.__arithmetic_op_executor,
            "elementary": self.__elementary_op_executor,
            "matrix": self.__matrix_op_executor
        }
        return options[instruction["operation"]].execute(instruction)
