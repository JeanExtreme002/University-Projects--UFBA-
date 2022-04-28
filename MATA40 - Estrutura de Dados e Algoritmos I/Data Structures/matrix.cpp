#include <stdexcept>

/**
Matrix é uma classe para criar uma matriz estática, de ordem predefinida.
*/
template <typename ElementType> class Matrix {
    private:
        ElementType *array = NULL;
        int order[2] = {0, 0};
        int length = 0;

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
                throw std::invalid_argument("matrix row must be a positive number");
            }
            if (column < 0) {
                throw std::invalid_argument("matrix column must be a positive number");
            }
            if (row >= order[0]) {
                throw std::out_of_range("matrix row out of range");
            }
            if (column >= order[1]) {
                throw std::out_of_range("matrix column out of range");
            }
        }

        /**
        Método para verificar se um dado índice é válido.
        */
        void validateIndex(int index) {
            if (index >= length) {
                throw std::out_of_range("list index out of range");
            }
        }

        /**
        Método para verificar se a matriz é igual à outra.
        */
        bool equals(Matrix &matrix) {

            // Verifica se a ordem das matrizes é diferente.
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
        /**
        Construtor da classe.
        */
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

        /**
        Destrutor da classe.
        */
        ~Matrix() {
            delete[] array;
        }

        /**
        Método para retornar um elemento da matriz, a partir de um índice, 
        utilizando a sintaxe dos colchetes.
        */
        ElementType &operator [](int index) {
            validateIndex(index);
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
        Método para preencher a matriz com um dado elemento.
        */
        void fill(ElementType element) {
            for (int index = 0; index < length; index++) {
                array[index] = element;
            }
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