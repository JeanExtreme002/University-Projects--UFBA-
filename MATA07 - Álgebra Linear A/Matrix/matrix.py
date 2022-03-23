class MatrixOrderError(Exception):
    pass

class Matrix(object):
    
    def __init__(self, rows, columns, iterable = []):
        self.__complex_values = 0
        self.__non_zero_values = 0
        
        self.__matrix = [[0,] * columns for i in range(rows)]
        self.__rows, self.__columns = rows, columns
    
        # Adiciona os valores do iterável à matriz, se houverem.
        for index in range(min(rows * columns, len(iterable))):
            self[index] = iterable[index]

    def __str__(self):
        str_matrix = [[str(v) for v in self.__matrix[row]] for row in range(self.__rows)]
        return "\n".join(["|" + ",".join(str_matrix[row]) + "|" for row in range(self.__rows)])

    def __get_position_slice(self, position):
        # Caso seja obtido um índice (valor inteiro), a linha e coluna do elemento serão calculados.
        return slice(*divmod(position, self.__columns)) if isinstance(position, int) else position

    def __getitem__(self, position):
        """
        Param position: Pode ser um índice (inteiro) ou um slice [row: column].
        """
        position = self.__get_position_slice(position)

        # Retorna o valor na posição (linha, coluna).
        return self.__matrix[position.start][position.stop]

    def __setitem__(self, position, value):
        """
        Param position: Deve ser um índice (inteiro) ou um slice [row: column].
        Param value: Deve ser um número (int, float, complex).
        """
        position = self.__get_position_slice(position)

        # Verifica se o tipo dos valores para determinar ao final
        # se existem números complexos na matriz.
        if isinstance(self[position.start: position.stop], complex):
            if not isinstance(value, complex): self.__complex_values -= 1
        else:
            if isinstance(value, complex): self.__complex_values += 1

        # Verifica se o valor é zero para determinar ao final se a matriz é nula.
        if self[position.start: position.stop] == 0:
            if value != 0: self.__non_zero_values += 1
        else:
            if value == 0: self.__non_zero_values -= 1
        
        # Verifica se o valor é um número e o insere na posição especificada.
        if not self.__is_number(value): raise TypeError("Value must be a number (int, float or complex), not '{}'".format(type(value).__name__))
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
            raise TypeError("Expected a Matrix object, not '{}'".format(type(matrix).__name__))

        # Verifica se a ordem das matrizes é a mesma.
        if self.get_order() != matrix.get_order(): return False

        # Verifica se os valores são iguais.
        for row, column, element in self:
            if matrix[row: column] != element: return False
        return True

    def __add__(self, matrix):
        # Verifica se o argumento é uma matriz.
        if not self.__is_matrix(matrix):
            raise TypeError("Expected a Matrix object, not '{}'".format(type(matrix).__name__))

        # Verifica se a ordem é a mesma.
        if not self.get_order() == matrix.get_order():
            raise MatrixOrderError("Matrix must have the same order: {}x{}".format(*self.get_order()))
    
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
            
        else: raise TypeError("Value must be a number (int, float or complex) or a Matrix object, not '{}'".format(type(value).__name__))
    
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

    def __check_symmetry(self, skew = False, conjugate = False):
        # Caso a matriz não seja quadrada, o resultado será falso para qualquer verificação.
        if not self.is_square(): return False

        # Percorre a parte triangular superior da matriz.
        for row in range(self.__rows):
            for column in range(row, self.__columns):
                # Obtém o valor da matriz. Caso pedido, o valor será conjugado.
                value = self[column: row].conjugate() if conjugate else self[column: row]

                # Verifica se o valor na posição (linha, coluna), positivo ou negativo, dependendo
                # do que for pedido, está presente na posição (coluna, linha).
                if self[row: column] != value * (-1 if skew else 1): return False
        return True     

    def __conjugate_transpose(self, conjugate = True, transpose = True):
        new_matrix = Matrix(*self.get_order()[::-1])

        for row, column, element in self:
            # Troca a linha pela coluna e a coluna pela linha, caso seja pedido a matriz transposta.
            if transpose:
                column, row = row, column

            # Insere na posição (linha, coluna) o valor. Caso pedido, será inserido o valor conjugado.
            new_matrix[row: column] = element.conjugate() if conjugate else element
        return new_matrix

    def __is_matrix(self, value):
        return isinstance(value, Matrix)

    def __is_number(self, value):
        return type(value) in [int, float, complex]

    def __verify_position(self, position, row = True):
        # Verifica se a posição (linha ou coluna) é um inteiro maior que zero e retorna (posição - 1).
        if not isinstance(position, int):
            raise TypeError("{} must be an integer, not '{}'".format("Row" if row else "Column", type(position).__name__))
        if position <= 0:
            raise ValueError("{} must be > 0".format("Row" if row else "Column"))
        return position - 1

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
        row, column = self.__verify_position(row), self.__verify_position(column, row = False)
        return self[row: column]

    def get_column(self, column):
        """
        Obtém toda a coluna da matriz em uma determinada posição.
        """
        column = self.__verify_position(column, row = False)
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
        row = self.__verify_position(row)
        return self.__matrix[row].copy()

    def is_hermitian(self):
        """
        Verifica se a matriz é uma matriz hermitiana.
        """
        return self.__check_symmetry(conjugate = True)

    def is_complex(self):
        """
        Verifica se há números complexos na matriz.
        """
        return self.__complex_values > 0

    def is_identity(self):
        """
        Verifica se a matriz é uma matriz identidade.
        """
        for row, column, element in self:
            if (row == column and element != 1) or (row != column and element != 0):
                return False
        return True

    def is_null(self):
        """
        Verifica se a matriz é nula.
        """
        return self.__non_zero_values == 0

    def is_skew_hermitian(self):
        """
        Verifica se a matriz é uma matriz anti-hermitiana.
        """
        return self.__check_symmetry(skew = True, conjugate = True)

    def is_skew_symmetric(self):
        """
        Verifica se a matriz é uma matriz anti-simétrica.
        """
        return self.__check_symmetry(skew = True)

    def is_square(self):
        """
        Verifica se a matriz é uma matriz square.
        """
        return self.__rows == self.__columns

    def is_symmetric(self):
        """
        Verifica se a matriz é uma matriz simétrica.
        """
        return self.__check_symmetry()

    def multiply(self, value):
        """
        Retorna uma matriz resultante do produto da matriz por um escalar ou por outra matriz.
        """
        return self * value

    def set(self, row, column, value):
        """
        Insere um elemento na posição (linha >= 1, coluna >= 1).
        """
        row, column = self.__verify_position(row), self.__verify_position(column, row = False)
        self[row: column] = value

    def trace(self):
        """
        Retorna o traço da matriz.
        """
        if not self.is_square():
            raise MatrixOrderError("Must be a square matrix")
        
        value = 0
        
        for index in range(self.__rows):
            value += self[index: index]
        return value

    def transpose(self):
        """
        Retorna a matriz transposta.
        """
        return self.__conjugate_transpose(conjugate = False)

