class CommandNotExistsError(Exception):
    def __init__(self, command):
        self.__command = command
        
    def __str__(self):
        return "O comando \"{}\" não existe.".format(self.__command)

class DivisionByMatrixError(Exception):
    def __str__(self):
        return "Não é possível dividir por uma matriz."

class ElementPositionError(Exception):
    def __init__(self, position):
        self.__position = position

    def __str__(self):
        return "A posição E{},{} não existe.".format(*self.__position)

class ExpressionSyntaxError(Exception):
    def __str__(self):
        return "A sintaxe dessa expressão está incorreta."

class IllegalExponentError(Exception):
    def __str__(self):
        return "O expoente deve ser um número inteiro."

class IllegalRowError(Exception):
    def __str__(self):
        return "Não é possível realizar essa operação com uma linha."

class IllegalScalarError(Exception):
    def __str__(self):
        return "Não é possível realizar essa operação com um escalar."

class InstructionSyntaxError(Exception):
    def __str__(self):
        return "A sintaxe dessa instrução está incorreta."

class MatrixOrderError(Exception):
    def __init__(self, order = None, add_operation = False, mult_operation = False):
        self.__add_operation = add_operation
        self.__mult_operation = mult_operation
        self.__order = order
        
    def __str__(self):
        if self.__add_operation: return "Para essa operação, as matrizes devem possuir a mesma ordem."
        elif self.__mult_operation: return "O número de colunas da matriz à esquerda deve ser o número de linhas da matriz à direita."
        return "Não é possível realizar essa operação em uma matriz \"{}x{}\".".format(*self.__order)

class NonInvertibleMatrixError(Exception):
    def __str__(self):
        return "Essa matriz não é inversível."

class NoMatricesError(Exception):
    def __init__(self, amount):
        self.__amount = amount
        
    def __str__(self):
        return "Para realizar essa operação, é necessário {} matrizes.".format(self.__amount)

class NoMatrixError(Exception):
    def __init__(self, left = False, right = False):
        self.__left, self.__right = left, right

    def __str__(self):
        if self.__left: direction = " à esquerda do operador"
        elif self.__right: direction = " à direita do operador"
        else: direction = ""
        
        return "Informe uma matriz{} para realizar essa operação.".format(direction)

class NoScalarError(Exception):
    def __str__(self):
        return "Informe o escalar para realizar essa operação."

class NoSecondRowError(Exception):
    def __str__(self):
        return "Informe a posição da segunda linha para realizar essa operação."

class PowByMatrixError(Exception):
    def __str__(self):
        return "Não é possível utilizar uma matriz como expoente."

class SameRowError(Exception):
    def __str__(self):
        return "Essa operação não é válida se as linhas forem as mesmas."

class ZeroScalarDivisionError(Exception):
    def __str__(self):
        return "Não é possível dividir por zero!"

class ZeroScalarError(Exception):
    def __init__(self, mult = True):
        self.__mult = mult

    def __str__(self):
        if self.__mult: return "Multiplicação por zero não é uma operação válida."
        else: return "Não é possível dividir um número por zero!"
