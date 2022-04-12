from .errors import *

class Matrix(object):
    
    def __init__(self, rows, columns, iterable = []):
        # Verifica se o número de linhas ou colunas é menor que zero.
        if rows <= 0 or columns <= 0:
            raise MatrixOrderError("Matrix order must be at least '1x1'")

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

    def __repr__(self):
        matrix_type = "Complex" if self.is_complex() else "Real"
        return "<{} Matrix : {},{}>".format(matrix_type, self.__rows, self.__columns)
    
    def __len__(self):
        return len(self.__matrix)

    def __contains__(self, value):
        for row in self.__matrix:
            if value in row: return True
        return False

    def __get_row_and_column(self, position):
        # Caso seja obtido um índice (valor inteiro), a linha e coluna do elemento serão calculados.
        position = slice(*divmod(position, self.__columns)) if isinstance(position, int) else position
        return position.start, position.stop

    def __getitem__(self, position):
        """
        Param position: Deve ser um índice (inteiro) ou um slice [row: column]. (OBS: As posições aqui devem começar de 0)
        """
        row, column = self.__get_row_and_column(position)
        return self.__matrix[row][column]

    def __setitem__(self, position, value):
        """
        Param position: Deve ser um índice (inteiro) ou um slice [row: column]. (OBS: As posições aqui devem começar de 0)
        Param value: Deve ser um número (int, float, complex).
        """
        row, column = self.__get_row_and_column(position)
        old_value = self[row: column]
        
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
        self.__matrix[row][column] = int(value) if not isinstance(value, complex) and int(value) == value else value

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

    def __pow__(self, exponent):
        if not isinstance(exponent, int): TypeError("Exponent must be an integer, not '{}'".format(type(value).__name__))
        if not self.is_square(): raise MatrixOrderError("Must be a square matrix")

        # Se o expoente for zero, será retornado uma matriz identidade.
        if exponent == 0:
            rows, columns = self.get_order()
            identity_matrix = Matrix(*self.get_order())

            for i in range(rows):
                identity_matrix[i: i] = 1
            return identity_matrix

        # Se o expoente for menor que zero, a matriz a ser trabalhada será a inversa.
        if exponent < 0:
            matrix = self.get_matrix_inverse()
            exponent *= -1
        else: matrix = self

        # Obtém uma nova matriz, na qual será multiplicada pela base.
        new_matrix = Matrix(*matrix.get_order(), matrix.to_list())
        
        # Multiplica a matriz por ela mesma (N - 1) vezes.
        for i in range(exponent - 1):
            new_matrix *= matrix

        return new_matrix

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

    def __truediv__(self, value):
        return self.__mul__(value, div = True)

    def __mul__(self, value, *, div = False):
        # Verifica se o valor é uma matriz. Se sim, verifica se o seu número de linhas é
        # o mesmo do número de colunas do objeto.
        if not div and self.__is_matrix(value):
            if self.__columns == value.get_order()[0]:
                return self.__mul_by_matrix(value)
            else:
                raise MatrixOrderError("The number of rows must equal the number of columns.")
            
        # Verifica se o valor é um número e o multiplica, ou divide.    
        elif self.__is_number(value):
            return self.__mul_by_number(value, div = div)

        # Se a operação de divisão foi solicitada, e o valor não é um número, então não é possível dividir.
        elif div: raise TypeError("Value must be a number (int, float or complex), not '{}'".format(type(value).__name__))

        # Gera um erro se o valor não for um número ou matriz.
        else: raise TypeError("Value must be a number (int, float or complex) or a Matrix object, not '{}'".format(type(value).__name__))
    
    def __mul_by_number(self, value, *, div = False):
        new_matrix = Matrix(*self.get_order())
        
        # Retorna uma nova matriz com o produto de cada elemento pelo valor recebido.
        for row, column, element in self:
            if div: new_matrix[row: column] = element / value
            else: new_matrix[row: column] = element * value
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

    def add(self, matrix, *, sub = False):
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
        Retorna o elemento em uma dada posição (linha, coluna).
        """
        row, column = self.__verify_position(row), self.__verify_position(column, row = False)
        return self[row: column]

    def get_adjugate_matrix(self):
        """
        Retorna a matriz adjunta.
        """
        return self.get_cofactor_matrix().transpose()

    def get_cofactor(self, row, column):
        """
        Retorna o cofator de uma dada posição (linha, coluna) da matriz.
        """
        if self.__rows == 1 and self.__columns == 1: return 1
        
        determinant = self.get_matrix_minor(row, column).get_determinant()
        return (determinant * -1) if (row + column) % 2 != 0 else determinant

    def get_cofactor_matrix(self):
        """
        Retorna a matriz cofatora.
        """
        new_matrix = Matrix(*self.get_order())
        
        for row in range(self.__rows):
            for column in range(self.__columns):
                new_matrix[row: column] = self.get_cofactor(row + 1, column + 1)
        return new_matrix

    def get_column(self, column):
        """
        Retorna toda a coluna da matriz em uma determinada posição (coluna).
        """
        column = self.__verify_position(column, row = False)
        return [self[row: column] for row in range(self.__rows)]

    def get_determinant(self):
        """
        Retorna o determinante da matriz.
        """
        if not self.is_square():
            raise MatrixOrderError("Matrix must be a square matrix")

        # O determinante de uma matriz de ordem 0 é 1.
        if self.__rows == 0: return 1

        # O determinante de uma matriz de ordem 1 é o próprio valor.
        if self.__rows == 1:
            return self[0] if self[0] != 0 else 0

        # Caso a matriz seja de ordem 2, basta utilizar a fórmula (AD - BC)
        if self.__rows == 2:
            determinant = self[0] * self[3] - self[1] * self[2]
            return determinant if determinant != 0 else 0

        determinant = 0

        # Calcula o determinante multiplicando os elementos da primeira
        # linha pelos seus cofatores e os somando.
        for column in range(self.__columns):
            determinant += self[0: column] * self.get_cofactor(1, column + 1)
            
        return determinant if determinant != 0 else 0

    def get_matrix_minor(self, row, column):
        """
        Retorna o menor complementar da matriz, removendo a linha e coluna especificada.
        """

        # A menor matriz possível para realizar essa operação é a de ordem 2x2.
        if self.__rows < 2 or self.__columns < 2:
            raise MatrixOrderError("'{}x{}' matrix does not have a minor".format(*self.get_order()))
        
        row, column = self.__verify_position(row), self.__verify_position(column, row = False)
        new_matrix = Matrix(self.__rows - 1, self.__columns - 1)

        index = 0

        # Percorre todos os elementos da matriz e adiciona à nova matriz
        # somente os que não pertencem à linha e coluna especificada.
        for value_row, value_column, value in self:
            
            if value_row != row and value_column != column:
                new_matrix[index] = value
                index += 1
                
        return new_matrix

    def get_matrix_inverse(self):
        """
        Retorna a matriz inversa.
        """
        determinant = self.get_determinant()

        # Retorna a matriz se o determinante for diferente de zero.
        if determinant == 0: raise NonInvertibleMatrixError("Matrix is not invertible because its determinant is zero")
        return self.get_adjugate_matrix() / determinant

    def get_order(self):
        """
        Retorna o número de linhas e colunas que a matriz possui.
        """
        return (self.__rows, self.__columns)

    def get_row(self, row):
        """
        Retorna toda a linha da matriz em uma determinada posição (linha).
        """
        row = self.__verify_position(row)
        return self.__matrix[row].copy()

    def get_trace(self):
        """
        Retorna o traço da matriz.
        """
        if not self.is_square():
            raise MatrixOrderError("Must be a square matrix")
        
        value = 0
        
        for index in range(self.__rows):
            value += self[index: index]
        return value

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

    def is_normal(self):
        """
        Verifica se a matriz é uma matriz normal.
        """
        if not self.is_square(): return False
        
        ct_matrix = self.conjugate_transpose()
        return ct_matrix * self == self * ct_matrix

    def is_null(self):
        """
        Verifica se a matriz é uma matriz nula.
        """
        return self.__non_zero_values == 0

    def is_orthogonal(self):
        """
        Verifica se a matriz é uma matriz ortogonal.
        """
        if not self.is_square(): return False
        
        t_matrix = self.transpose()
        result = t_matrix * self
        
        return (result == self * t_matrix) and result.is_identity()

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

    def multiply(self, value, *, div = False):
        """
        Retorna uma matriz resultante do produto da matriz por um escalar ou por outra matriz,
        ou da divisão (div = True) da matriz por um escalar.
        """
        return (self / value) if div else (self * value)

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
        Insere um elemento em uma dada posição (linha, coluna).
        """
        row, column = self.__verify_position(row), self.__verify_position(column, row = False)
        self[row: column] = value

    def set_column(self, column, iterable):
        """
        Define uma coluna em uma determinada posição (coluna) da matriz.
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
        Define uma linha em uma determinada posição (linha) da matriz.
        """
        row = self.__verify_position(row)

        # Verifica se o objeto iterável é formado apenas por números.
        number_array, value_index, value_type = self.__is_number_array(iterable)
        if not number_array: raise TypeError("Iterable must contain only numbers. Got '{}' at index {}".format(value_type.__name__, value_index))

        # Insere os valores do iterável em cada coluna, na linha especificada, da matriz.
        for column in range(self.__columns):
            self[row: column] = iterable[column]

    def to_list(self):
        """
        Retorna uma lista com todos os valores da matriz.
        """
        return [value for row in self.__matrix for value in row]

    def transpose(self):
        """
        Retorna a matriz transposta.
        """
        return self.__conjugate_transpose(conjugate = False)
