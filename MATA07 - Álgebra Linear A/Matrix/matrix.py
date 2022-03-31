class MatrixOrderError(Exception):
    pass

class Matrix(object):
    
    def __init__(self, rows, columns, iterable = []):
        # Verifica se o número de linhas ou colunas é menor que zero.
        if rows < 0 or columns < 0:
            raise MatrixOrderError("Matrix order must be at least '0x0'")

        # Inicializa os atributos privados do objeto.
        self.__complex_values = 0
        self.__non_zero_values = 0
    
        # Cria uma lista para armazenar os elementos da matriz.
        self.__matrix = [[0,] * columns for i in range(rows)]
        self.__rows, self.__columns = rows, columns
    
        # Adiciona os valores do iterável à matriz, se houverem.
        for index in range(min(rows * columns, len(iterable))):
            self[index] = iterable[index]

    def __str__(self):
        # Obtém o comprimento da maior string de elemento da matriz.
        largest_string_length = 0

        for row, column, element in self:
            element_string_length = len(str(element))
            
            if element_string_length > largest_string_length:
                largest_string_length = element_string_length

        element_format = "{:>" + str(largest_string_length) + "}"
        string = ""

        # Constrói a string a ser retornada, tratando linha por linha.
        for row in range(self.__rows):
            string += "|"
            
            for column in range(self.__columns):
                element = self[row: column]

                # Remove os parênteses do número complexo e troca a letra "J" por "I".
                if isinstance(element, complex):
                    element = str(element).replace("(", "").replace(")", "").replace("j", "i")

                # Adiciona o elemento à linha da string.
                string += element_format.format(element) + (" " if column != (self.__columns - 1) else "")

            # Finaliza a linha da string.
            string += "|" + ("\n" if row != (self.__rows - 1) else "")
        return string
    
    def __len__(self):
        return len(self.__matrix)

    def __get_position_slice(self, position):
        # Caso seja obtido um índice (valor inteiro), a linha e coluna do elemento serão calculados.
        return slice(*divmod(position, self.__columns)) if isinstance(position, int) else position

    def __getitem__(self, position):
        """
        Param position: Deve ser um índice (inteiro) ou um slice [row: column]. (OBS: As posições aqui devem começar de 0)
        """
        position = self.__get_position_slice(position)

        # Retorna o valor na posição (linha, coluna).
        return self.__matrix[position.start][position.stop]

    def __setitem__(self, position, value):
        """
        Param position: Deve ser um índice (inteiro) ou um slice [row: column]. (OBS: As posições aqui devem começar de 0)
        Param value: Deve ser um número (int, float, complex).
        """
        position = self.__get_position_slice(position)
        old_value = self[position.start: position.stop]
        
        # Verifica se o tipo dos valores para determinar ao final
        # se existem números complexos na matriz.
        if isinstance(old_value, complex):
            if not isinstance(value, complex): self.__complex_values -= 1
        else:
            if isinstance(value, complex): self.__complex_values += 1

        # Verifica se o valor é zero para determinar ao final se a matriz é nula.
        if old_value == 0:
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
        """
        Retorna uma tupla no formato (linha, coluna, valor).
        """
        # Obtém a linha e coluna a partir do índice.
        row, column = divmod(self.__iteration_index, self.__columns)

        # Verifica se o número de linha já excedeu.
        if row >= len(self): raise StopIteration
        
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

    def __add__(self, matrix, *, sub = False):
        # Verifica se o argumento é uma matriz.
        if not self.__is_matrix(matrix):
            raise TypeError("Expected a Matrix object, not '{}'".format(type(matrix).__name__))

        # Verifica se a ordem é a mesma.
        if not self.get_order() == matrix.get_order():
            raise MatrixOrderError("Matrix must have the same order: {}x{}".format(*self.get_order()))
    
        new_matrix = Matrix(*self.get_order())

        # Retorna uma nova matriz com as somas de seus elementos.
        for row, column, element in self:
            new_matrix[row: column] = element + matrix[row: column] * (-1 if sub else 1)
        return new_matrix

    def __sub__(self, matrix):
        return self.__add__(matrix, sub = True)

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
                    new_matrix[row: column] += self[row: index] * matrix[index: column]
        return new_matrix

    def __check_diagonal(self, value = 1):
        # Um dos requisitos para a função retornar True é a matriz ser quadrada.
        if not self.is_square(): return False
        
        for row, column, element in self:
            if (row == column and element != value) or (row != column and element != 0):
                return False
        return True
    
    def __check_symmetry(self, skew = False, conjugate = False):
        # Um dos requisitos para a função retornar True é a matriz ser quadrada.
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

    def __check_triangular(self, lower = False):
        # Um dos requisitos para a função retornar True é a matriz ser quadrada.
        if not self.is_square(): return False
        
        for row, column, element in self:
            if ((row < column) if lower else (row > column)) and element != 0:
                return False
        return True

    def __conjugate_transpose(self, conjugate = True, transpose = True):
        new_matrix = Matrix(*self.get_order()[::-1])

        for row, column, element in self:
            # Troca a linha pela coluna e a coluna pela linha, caso seja pedido a matriz transposta.
            if transpose: column, row = row, column

            # Insere na posição (linha, coluna) o valor. Caso pedido, será inserido o valor conjugado.
            new_matrix[row: column] = element.conjugate() if conjugate else element
        return new_matrix

    def __is_matrix(self, value):
        return isinstance(value, Matrix)

    def __is_number(self, value):
        return type(value) in [int, float, complex]

    def __is_number_array(self, iterable):
        # Percorre o iterável, verificando se ele possui apenas elementos numéricos.
        for index in range(len(iterable)):
            value = iterable[index]
            if not self.__is_number(value): return False, index, type(value)
        return True, None, None

    def __verify_position(self, position, row = True):
        # Verifica se a posição (linha ou coluna) é um inteiro maior que zero.
        if not isinstance(position, int):
            raise TypeError("{} must be an integer, not '{}'".format("Row" if row else "Column", type(position).__name__))
        if position <= 0:
            raise IndexError("{} must be > 0".format("Row" if row else "Column"))

        # Verifica se a posição (linha ou coluna) é maior que o tamanho da matriz.
        if row and position > self.__rows:
            raise IndexError("Matrix has just {} rows".format(self.__rows))
        elif not row and position > self.__columns:
            raise IndexError("Matrix has just {} columns".format(self.__columns))

        # Retorna a posição em forma de índice comum (indo de zero à N). 
        return position - 1

    def add(self, matrix, *, sub = True):
        """
        Retorna uma matriz resultante da soma, ou subtração (sub = True), de matrizes.
        """
        return (self - matrix) if sub else (self + matrix)

    def add_row(self, row1, row2, scalar = 1, *, div = False):
        """
        Soma todos os elementos de uma linha por outra multiplicada por um escalar (default: scalar = 1).
        """
        row1 = self.__verify_position(row1)
        row2 = self.__verify_position(row2)

        # Verifica se o escalar é um número.
        if not self.__is_number(scalar):
            raise TypeError("Value must be a number (int, float or complex), not '{}'".format(type(scalar).__name__))

        # Percorre a linha somando os seus elementos pelo elemento da outra na linha, na coluna correspondente. 
        for column in range(self.__columns):
           if div: self[row1: column] += self[row2: column] / scalar
           else: self[row1: column] += self[row2: column] * scalar
      
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

    def interchange_rows(self, row1, row2):
        """
        Troca duas linhas de posição na matrix.
        """
        row1 = self.__verify_position(row1)
        row2 = self.__verify_position(row2)

        # Percorre as linhas trocando o valor de suas colunas.
        for column in range(self.__columns):
            row1_value, row2_value = self[row1: column], self[row2: column]
            self[row1: column] = row2_value
            self[row2: column] = row1_value

    def is_column(self):
        """
        Verifica se a matriz é uma matriz coluna.
        """
        return self.__columns == 1

    def is_complex(self):
        """
        Verifica se há números complexos na matriz.
        """
        return self.__complex_values > 0

    def is_diagonal(self):
        """
        Verifica se a matriz é uma matriz diagonal.
        """
        for row, column, element in self:
            if row != column and element != 0:
                return False
        return True

    def is_hermitian(self):
        """
        Verifica se a matriz é uma matriz hermitiana.
        """
        return self.__check_symmetry(conjugate = True)

    def is_identity(self):
        """
        Verifica se a matriz é uma matriz identidade.
        """
        return self.__check_diagonal(value = 1)

    def is_lower_triangular(self):
        """
        Verifica se a matriz é uma matriz triangular inferior.
        """
        return self.__check_triangular(lower = True)

    def is_null(self):
        """
        Verifica se a matriz é uma matriz nula.
        """
        return self.__non_zero_values == 0

    def is_row(self):
        """
        Verifica se a matriz é uma matriz linha.
        """
        return self.__rows == 1

    def is_scalar(self):
        """
        Verifica se a matriz é uma matriz escalar.
        """
        return self.__check_diagonal(value = self[0])
        
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
        Verifica se a matriz é uma matriz quadrada.
        """
        return self.__rows == self.__columns

    def is_symmetric(self):
        """
        Verifica se a matriz é uma matriz simétrica.
        """
        return self.__check_symmetry()

    def is_upper_triangular(self):
        """
        Verifica se a matriz é uma matriz triangular superior.
        """
        return self.__check_triangular(lower = False)

    def multiply(self, value):
        """
        Retorna uma matriz resultante do produto da matriz por um escalar ou por outra matriz.
        """
        return self * value

    def multiply_row(self, row, value, *, div = False):
        """
        Multiplica, ou divide (div = True), todos os elementos de uma linha por um valor.
        """
        row = self.__verify_position(row)

        # Percorre a linha multiplicando os seus elementos pelo escalar. 
        for column in range(self.__columns):
            if div: self[row: column] = self[row: column] / value
            else: self[row: column] = self[row: column] * value

    def set(self, row, column, value):
        """
        Insere um elemento na posição (linha >= 1, coluna >= 1).
        """
        row, column = self.__verify_position(row), self.__verify_position(column, row = False)
        self[row: column] = value

    def set_column(self, column, iterable):
        """
        Define uma coluna em uma determinada posição da matriz.
        """
        column = self.__verify_position(column, row = False)

        # Verifica se o objeto iterável é formado apenas por números.
        number_array, value_index, value_type = self.__is_number_array(iterable)
        if not number_array: raise TypeError("Iterable must contain only numbers. Got '{}' at index {}".format(value_type.__name__, value_index))

        # Insere os valores do iterável em cada linha, na coluna especificada, da matriz.
        for row in range(self.__rows):
            self[row: column] = iterable[row]

    def set_row(self, row, iterable):
        """
        Define uma linha em uma determinada posição da matriz.
        """
        row = self.__verify_position(row)

        # Verifica se o objeto iterável é formado apenas por números.
        number_array, value_index, value_type = self.__is_number_array(iterable)
        if not number_array: raise TypeError("Iterable must contain only numbers. Got '{}' at index {}".format(value_type.__name__, value_index))

        # Insere os valores do iterável em cada coluna, na linha especificada, da matriz.
        for column in range(self.__columns):
            self[row: column] = iterable[column]

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
