class MatrixOrderError(Exception):
    pass

class Matrix(object):
    
    def __init__(self, rows, columns):
        self.__matrix = [[0,] * columns for i in range(rows)]
        self.__rows = rows
        self.__columns = columns

    def __str__(self):
        str_matrix = [[str(v) for v in self.__matrix[row]] for row in range(self.__rows)]
        return "\n".join(["|" + ",".join(str_matrix[row]) + "|" for row in range(self.__rows)])

    def __getitem__(self, position: slice):
        return self.__matrix[position.start][position.stop]

    def __setitem__(self, position: slice, value):
        # Verifica se o valor é um número e o insere na posição especificada.
        if not self.__is_number(value): raise TypeError("Value must be a number (int, float or complex)")
        self.__matrix[position.start][position.stop] = value

    def __eq__(self, matrix):
        # Verifica se o argumento é uma matriz.
        if not self.__is_matrix(matrix):
            raise TypeError("Expected a Matrix object")

        # Verifica se a ordem das matrizes é a mesma.
        if self.get_order() != matrix.get_order(): return False

        # Verifica se os valores são iguais.
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self[row: column] != matrix[row: column]: return False
        return True

    def __add__(self, matrix):
        # Verifica se o argumento é uma matriz.
        if not self.__is_matrix(matrix):
            raise TypeError("Expected a Matrix object")

        # Verifica se a ordem é a mesma.
        if not self.get_order() == matrix.get_order():
            raise MatrixOrderError("Matrix must have the same order")
    
        new_matrix = Matrix(*self.get_order())

        # Retorna uma nova matriz com as somas de seus elementos.
        for row in range(self.__rows):
            for column in range(self.__columns):
                new_matrix[row: column] = self[row: column] + matrix[row: column]
        return new_matrix

    def __mul__(self, value):
        # Verifica se o valor é uma matriz. Se sim, verifica se o seu número de linhas é
        # o mesmo do número de colunas do objeto.
        if self.__is_matrix(value):
            if self.__columns == value.get_order()[0]:
                return self.__mul_by_matrix(value)
            else: raise MatrixOrderError("The number of rows must equal the number of columns.")
            
        # Verifica se o valor é um número.    
        elif self.__is_number(value):
            return self.__mul_by_number(value)
            
        else: raise TypeError("Value must be a number (int, float or complex) or a Matrix object")
    
    def __mul_by_number(self, value):
        new_matrix = Matrix(*self.get_order())
        
        # Retorna uma nova matriz com o produto de cada elemento pelo valor recebido.
        for row in range(self.__rows):
            for column in range(self.__columns):
                new_matrix[row: column] = self.__matrix[row][column] * value
        return new_matrix

    def __mul_by_matrix(self, matrix):
        # A ordem da nova matriz é (M linhas da primeira, N columnas da segunda).
        new_matrix_rows, new_matrix_columns = matrix.get_order()
        new_matrix = Matrix(self.__rows, new_matrix_columns)

        # Retorna uma nova matriz com o produto das matrizes, no qual é uma soma
        # das multiplicações zip(A1[row], A2[column]).
        for row in range(self.__rows):
            for column in range(new_matrix_columns):
                for index in range(self.__columns):
                    new_matrix[row: column] += self.__matrix[row][index] * matrix[index: column]
        return new_matrix

    def __check_position(self, row, column):
        if not isinstance(row, int): raise TypeError("Row must be an integer")
        if not isinstance(column, int): raise TypeError("Column must be an integer")
        if row <= 0: raise ValueError("Row must be > 0")
        if column <= 0: raise ValueError("Column must be > 0")

    def __is_matrix(self, value):
        return isinstance(value, Matrix)

    def __is_number(self, value):
        return type(value) in [int, float, complex]

    def add(self, matrix):
        """
        Retorna uma matriz resultante da soma de matrizes.
        """
        return self + matrix

    def multiply(self, value):
        """
        Retorna uma matriz resultante do produto da matriz por um escalar ou por outra matriz.
        """
        return self * value
    
    def get(self, row, column):
        """
        Obtém um elemento na posição (linha >= 1, coluna >= 1).
        """
        self.__check_position(row, column)
        return self[row - 1: column - 1]

    def get_order(self):
        """
        Retorna o número de linhas e colunas que a matriz possui.
        """
        return (self.__rows, self.__columns)

    def set(self, row, column, value):
        """
        Insere um elemento na posição (linha >= 1, coluna >= 1).
        """
        self.__check_position(row, column)
        self[row - 1: column - 1] = value

    def trace(self):
        """
        Retorna o traço da matriz.
        """
        value = 0
        
        for row in range(self.__rows):
            value += self[row: row]
        return value

    def transpose(self):
        """
        Retorna a matriz transposta.
        """
        new_matrix = Matrix(*self.get_order()[::-1])

        for row in range(self.__rows):
            for column in range(self.__columns):
                new_matrix[column: row] = self[row: column]
        return new_matrix
