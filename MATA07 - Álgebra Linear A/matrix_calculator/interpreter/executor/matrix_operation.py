from ..parser import parse_complex_value
from .operation_errors import *

class MatrixOperationExecutor(object):

    def __init__(self, core):
        self.__core = core

    def __convert_to_number(self, string):
        return parse_complex_value(string) if "(" in string else float(string)

    def __get_matrix(self, matrix_name):
        return self.__core.get_matrix(matrix_name)

    def __set_matrix(self, matrix_name, matrix):
        self.__core.set_matrix(matrix_name, matrix)

    def __get_minor_params(self, operator):
        return [int(value) for value in operator[1:].replace("(","").replace(")", "").split(",")]

    def __add(self, variable, x, y, sub = False):
        # É necessário duas matrizes para essa operação.
        if not x.isalpha() or not y.isalpha():
            raise NoMatricesError(2)

        matrix_x = self.__get_matrix(x)
        matrix_y = self.__get_matrix(y)

        # As matrizes devem ter a mesma ordem.
        if not matrix_x.get_order() == matrix_y.get_order():
            raise MatrixOrderError(add_operation = True)

        self.__set_matrix(variable, (matrix_x - matrix_y) if sub else (matrix_x + matrix_y))
    
    def __adjugate(self, variable, x, y):
        if y: raise InstructionSyntaxError
        matrix = self.__get_matrix(x)

        # Essa operação só pode ser realizada com matrizes quadradas.
        if not matrix.is_square(): raise MatrixOrderError(matrix.get_order())
        self.__set_matrix(variable, matrix.get_adjugate_matrix())

    def __cofactor(self, variable, x, y):
        if y: raise InstructionSyntaxError
        matrix = self.__get_matrix(x)

        # Essa operação só pode ser realizada com matrizes quadradas.
        if not matrix.is_square(): raise MatrixOrderError(matrix.get_order())
        self.__set_matrix(variable, matrix.get_cofactor_matrix())
        
    def __conjugate(self, variable, x, y):    
        if y: raise InstructionSyntaxError
        self.__set_matrix(variable, self.__get_matrix(x).conjugate())

    def __inverse(self, variable, x, y):
        if y: raise InstructionSyntaxError
        try: self.__set_matrix(variable, self.__get_matrix(x).get_matrix_inverse())
        except: raise NonInvertibleMatrixError

    def __minor(self, variable, x, y, operator):
        if y: raise InstructionSyntaxError
        matrix = self.__get_matrix(x)
        
        # Essa operação só pode ser realizada com matrizes de ordem maior ou igual a 2x2.
        if min(matrix.get_order()) < 2:
            raise MatrixOrderError(matrix.get_order())
        
        row, column = self.__get_minor_params(operator)
        self.__set_matrix(variable, matrix.get_matrix_minor(row, column))

    def __mult(self, variable, x, y, div = False):
        if not x.isalpha(): raise NoMatrixError(left = True)
        matrix_x = self.__get_matrix(x)
        
        if y.isalpha(): y = self.__get_matrix(y)
        else: y = self.__convert_to_number(y)

        # Não é possível dividir uma matriz por outra ou multiplicar duas matrizes de número de colunas e linhas diferentes.
        if not type(y) in [int, float, complex]:
            if div: raise DivisionByMatrixError
            if matrix_x.get_order()[1] != y.get_order()[0]: raise MatrixOrderError(mult_operation = True)

        # Não é possível dividir por um escalar zero.
        elif div and y == 0: raise ZeroScalarDivisionError

        self.__set_matrix(variable, (matrix_x / y) if div else (matrix_x * y))
        
    def __transpose(self, variable, x, y):
        if y: raise InstructionSyntaxError
        self.__set_matrix(variable, self.__get_matrix(x).transpose())
    
    def execute(self, instruction: dict):
        """
        Obtém um dicionário {"var": ..., "x": ..., "operator": ..., "y": ...}
        e retorna o resultado do cálculo da expressão.
        """
        operator = instruction["operator"]
        variable = instruction["var"]
        matrix_x = instruction["x"]
        matrix_y = instruction["y"]
        
        # Obtém a matriz conjugada.
        if operator in ["c", "ct", "tc"]:
            self.__conjugate(variable, matrix_x, matrix_y)

        # Obtém a matriz transposta.
        if operator in ["t", "ct", "tc"]:
            self.__transpose(variable, matrix_x, matrix_y)
            
        # Obtém a matriz adjunta ou cofatora.
        if operator == "adj":
            self.__adjugate(variable, matrix_x, matrix_y)

        elif operator == "cof":
            self.__cofactor(variable, matrix_x, matrix_y)

        # Obtém a inversa da matriz.
        elif operator == "inv":
            self.__inverse(variable, matrix_x, matrix_y)

        # Obtém o menor complementar da matriz.
        elif operator.startswith("m"):
            self.__minor(variable, matrix_x, matrix_y, operator)

        # Soma ou subtrai as matrizes.
        elif operator in "+-":
            self.__add(variable, matrix_x, matrix_y, "-" == operator)

        # Multiplica ou divide a matriz.
        elif operator in "*/":
            self.__mult(variable, matrix_x, matrix_y, "/" == operator)
