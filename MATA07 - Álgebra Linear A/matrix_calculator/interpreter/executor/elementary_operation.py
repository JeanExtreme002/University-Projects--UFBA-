from ..parser import parse_complex_value
from .operation_errors import *

class ElementaryOperationExecutor(object):
    def __init__(self, core):
        self.__core = core
        
    def __check_scalar(self, scalar, mult = True):
        if scalar == 0: raise ZeroScalarError(mult = mult)
           
    def __convert_to_number(self, string):
        return parse_complex_value(string) if "(" in string else float(string)

    def __get_matrix_in_use(self):
        return self.__core.get_matrix_in_use()[0]

    def __parse_instruction_args(self, instruction):
        row1, row2 = instruction["row1"], instruction["row2"]
        scalar, operator = instruction["scalar"], instruction["operator"]
        
        row1, row2 = int(row1), int(row2) if row2 else None
        scalar = self.__convert_to_number(scalar) if scalar else None
        return row1, operator, scalar, row2

    def __add(self, matrix, row1, row2, scalar, sub = False):
        if row1 == row2: raise SameRowError
        if not row2: raise NoSecondaryRowError
        
        if scalar is None: scalar = 1
        matrix.add_row(row1, row2, scalar * (-1 if sub else 1))

    def __interchange(self, matrix, row1, row2, scalar):
        if not row2: raise NoSecondaryRowError
        if scalar: raise IllegalScalarError
        matrix.interchange_rows(row1, row2)

    def __is_equal(self, matrix, row1, row2, scalar):
        if not row2: raise NoSecondaryRowError
        
        if scalar is None: return matrix.get_row(row1) == matrix.get_row(row2)
        return matrix.get_row(row1) == [value * scalar for value in matrix.get_row(row2)]

    def __multiply(self, matrix, row1, row2, scalar, div = False):
        if row2: raise IllegalRowError
        if scalar is None: raise NoScalarError
        matrix.multiply_row(row1, scalar, div = div)
            
    def execute(self, instruction: dict):
        """
        Obtém um dicionário {"row1": ..., "operator": ..., "scalar": ..., "row2": ...}
        e realiza a alteração na linha especificada, na chave "row1", na matriz em uso.
        """
        matrix = self.__get_matrix_in_use()

        # Transforma os valores recebidos para os seus respectivos tipos.
        row1, operator, scalar, row2 = self.__parse_instruction_args(instruction)

        # Verifica se o escalar é zero, pois, não é possível dividir um número por zero
        # e a multiplicação de uma linha por zero não é uma operação elementar.
        self.__check_scalar(scalar, mult = not "/" in operator)

        # Troca a posição de duas linhas.
        if operator == "<>":
            self.__interchange(matrix, row1, row2, scalar)

        # Verifica se as linhas são iguais.
        elif operator == "==":
            result = self.__is_equal(matrix, row1, row2, scalar)
            return "As linhas são iguais." if result else "As linhas são diferentes."
            
        # Soma, ou subtrai, uma linha por outra linha.
        elif operator in "+=-=":
            self.__add(matrix, row1, row2, scalar, sub = "-" in operator)

        # Multiplica, ou divide, uma linha por um escalar. 
        elif operator in "*=/=":
            self.__multiply(matrix, row1, row2, scalar, div = "/" in operator)
