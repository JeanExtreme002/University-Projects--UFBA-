class MatrixOrderError(Exception):
    pass

class Matrix(object):
    
    def __init__(self, rows, columns):
        self.__matrix = [[0,] * columns for i in range(rows)]
        self.__rows, self.__columns = rows, columns

    def __str__(self):
        str_matrix = [[str(v) for v in self.__matrix[row]] for row in range(self.__rows)]
        return "\n".join(["|" + ",".join(str_matrix[row]) + "|" for row in range(self.__rows)])

    def __getitem__(self, position: slice):
        # Caso seja obtido um índice (valor inteiro), a linha e coluna do elemento será calculada.
        if isinstance(position, int):
            position = slice(*divmod(position, self.__columns))

        # Retorna o valor na posição (linha, coluna).
        return self.__matrix[position.start][position.stop]

    def __setitem__(self, position: slice, value):
        # Verifica se o valor é um número e o insere na posição especificada.
        if not self.__is_number(value): raise TypeError("Value must be a number (int, float or complex)")
        self.__matrix[position.start][position.stop] = value

    def __iter__(self):
        self.__iteration_index = 0
        return self

    def __next__(self):
        # Obtém a linha e coluna a partir do índice.
        row, column = divmod(self.__iteration_index, self.__columns)

        # Verifica se o número de linha já excedeu.
        if row >= len(self.__matrix): raise StopIteration
        
        self.__iteration_index += 1
        return row, column, self[row: column]

    def __eq__(self, matrix):
        # Verifica se o argumento é uma matriz.
        if not self.__is_matrix(matrix):
            raise TypeError("Expected a Matrix object")

        # Verifica se a ordem das matrizes é a mesma.
        if self.get_order() != matrix.get_order(): return False

        # Verifica se os valores são iguais.
        for row, column, element in self:
            if matrix[row: column] != element: return False
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
        for row, column, element in self:
            new_matrix[row: column] = element + matrix[row: column]
        return new_matrix

    def __mul__(self, value):
        # Verifica se o valor é uma matriz. Se sim, verifica se o seu número de linhas é
        # o mesmo do número de colunas do objeto.
        if self.__is_matrix(value):
            if self.__columns == value.get_order()[0]:
                return self.__mul_by_matrix(value)
            else:
                raise MatrixOrderError("The number of rows must equal the number of columns.")
            
        # Verifica se o valor é um número.    
        elif self.__is_number(value):
            return self.__mul_by_number(value)
            
        else: raise TypeError("Value must be a number (int, float or complex) or a Matrix object")
    
    def __mul_by_number(self, value):
        new_matrix = Matrix(*self.get_order())
        
        # Retorna uma nova matriz com o produto de cada elemento pelo valor recebido.
        for row, column, element in self:
            new_matrix[row: column] = element * value
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

    def __conjugate_transpose(self, conjugate = True, transpose = True):
        new_matrix = Matrix(*self.get_order()[::-1])

        for row, column, element in self:
            # Troca a linha pela coluna e a coluna pela linha, caso seja pedido a matriz transposta.
            if transpose:
                column, row = row, column

            # Insere na posição (linha, coluna) o valor. Caso pedido, será inserido o valor conjugado.
            new_matrix[row: column] = element.conjugate() if conjugate else element
        return new_matrix

    def __get_position(self, position, row = True):
        # Verifica se a posição (linha ou coluna) é um inteiro maior que zero e retorna (posição - 1).
        if not isinstance(position, int):
            raise TypeError("{} must be an integer".format("Row" if row else "Column"))
        if position <= 0:
            raise ValueError("{} must be > 0".format("Row" if row else "Column"))
        return position - 1

    def __is_matrix(self, value):
        return isinstance(value, Matrix)

    def __is_number(self, value):
        return type(value) in [int, float, complex]

    def add(self, matrix):
        """
        Retorna uma matriz resultante da soma de matrizes.
        """
        return self + matrix

    def conjugate(self):
        """
        Retorna a matriz conjugada.
        """
        return self.__conjugate_transpose(transpose = False)

    def conjugate_transpose(self):
        """
        Retorna a matriz transconjugada.
        """
        return self.__conjugate_transpose()
    
    def get(self, row, column):
        """
        Obtém um elemento na posição (linha >= 1, coluna >= 1).
        """
        row, column = self.__get_position(row), self.__get_position(column, row = False)
        return self[row: column]

    def get_column(self, column):
        """
        Obtém toda a coluna da matriz em uma determinada posição.
        """
        column = self.__get_position(column, row = False)
        return [self[row: column] for row in range(self.__rows)]

    def get_order(self):
        """
        Retorna o número de linhas e colunas que a matriz possui.
        """
        return (self.__rows, self.__columns)

    def get_row(self, row):
        """
        Obtém toda a linha da matriz em uma determinada posição.
        """
        row = self.__get_position(row)
        return self.__matrix[row].copy()

    def is_identity(self):
        """
        Verifica se a matriz é uma matriz identidade.
        """
        for row, column, element in self:
            if (row == column and element != 1) or (row != column and element != 0):
                return False
        return True

    def is_square(self):
        """
        Verifica se a matriz é uma matriz square.
        """
        return self.__rows == self.__columns

    def is_symmetric(self):
        """
        Verifica se a matriz é uma matriz simétrica.
        """
        pass

    def multiply(self, value):
        """
        Retorna uma matriz resultante do produto da matriz por um escalar ou por outra matriz.
        """
        return self * value

    def set(self, row, column, value):
        """
        Insere um elemento na posição (linha >= 1, coluna >= 1).
        """
        row, column = self.__get_position(row), self.__get_position(column, row = False)
        self[row: column] = value

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
        return self.__conjugate_transpose(conjugate = False)




