#include <stdexcept>

template <typename ElementType> class Matrix {
    private:
        ElementType *array;
        int order[2];
        int length;

        /**
        Método para calcular o índice do array através da posição (linha, coluna)
        */
        int getArrayIndex(int row, int column) {
            return row * order[1] + column;
        }

        /**
        Método para verificar se uma dada posição é válida.
        */
        void validatePosition(int row, int column) {
            if (row < 0) {
                throw std::invalid_argument("matrix row must be a natural number");
            }
            if (column < 0) {
                throw std::invalid_argument("matrix column must be a natural number");
            }
            if (row >= order[0]) {
                throw std::out_of_range("matrix row out of range");
            }
            if (column >= order[1]) {
                throw std::out_of_range("matrix column out of range");
            }
        }

        /**
        Método para verificar se a matriz é igual à outra.
        */
        bool equals(Matrix &matrix) {

            // Verifica se a ordem das matrizes é a mesma.
            if (matrix.order[0] != order[0] || matrix.order[1] != order[1]) {
                return false;
            }

            // Percorre os elementos, verificando se são diferentes.
            for (int index = 0; index < length; index++) {
                if (matrix.array[index] != array[index]) {
                    return false;
                }
            }
            return true;
        }

    public:
        Matrix(int rows, int columns) {

            // Verifica se a quantidade de linhas e colunas é maior que zero.
            if (rows <= 0 || columns <= 0) {
                throw std::invalid_argument("matrix order must be at least '1x1'");
            }

            // Aloca memória para os elementos.
            length = rows * columns;
            array = new ElementType[length];

            order[0] = rows;
            order[1] = columns;

        }

        ~Matrix() {
            delete[] array;
        }

        ElementType &operator [](int index) {
            return array[index];
        }

        /**
        Método para verificar se a matriz é igual à outra, 
        utilizando o operador de comparação.
        */
        bool operator ==(Matrix &matrix) {
            return equals(matrix);
        }

        /**
        Método para verificar se a matriz é diferente de outra, 
        utilizando o operador de comparação.
        */
        bool operator !=(Matrix &matrix) {
            return !equals(matrix);
        }

        /**
        Método para verificar se a matriz possui um dado elemento.
        */
        bool contains(ElementType element) {
            for (int index = 0; index < length; index++) {
                if (array[index] == element) {
                    return true;
                }
            }
            return false;
        }

        /**
        Método para retornar o tamanho da matriz.
        */
        int getLength() {
            return length;
        }

        /**
        Método para retornar a quantidade de linhas da matriz.
        */
        int getRows() {
            return order[0];
        }

        /**
        Método para retornar a quantidade de colunas da matriz.
        */
        int getColumns() {
            return order[1];
        }

        /**
        Método para contar quantos elementos X existem na matriz.
        */
        int count(ElementType element) {
            int elementCount = 0;

            for (int index = 0; index < length; index++) {
                if (array[index] == element) {
                    elementCount += 1;
                }
            }
            return elementCount; 
        }

        /**
        Método para definir um elemento, em uma dada posição.
        */
        void set(int row, int column, ElementType element) {
            validatePosition(row, column);
            array[getArrayIndex(row, column)] = element;
        }

        /**
        Método para retornar um elemento, em uma dada posição.
        */
        ElementType get(int row, int column) {
            validatePosition(row, column);
            return array[getArrayIndex(row, column)];
        }

        /**
        Método para retornar uma cópia da matriz, copiando todos os seus elementos.
        */
        Matrix<ElementType> &copy() {
            Matrix<ElementType> *newMatrix = new Matrix<ElementType>(order[0], order[1]);

            for (int index = 0; index < length; index++) {
                newMatrix->array[index] = array[index];
            }

            return *newMatrix;
        }
};