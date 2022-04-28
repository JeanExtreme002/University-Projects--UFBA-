#include <stdexcept>

/**
StaticList é uma classe para criar listas estáticas, ou seja, listas com
tamanhos predefinidos, permitindo certas manipulações sob ela.
*/
template <typename ElementType> class StaticList {
    private:
        const static int LEFT = 0;
        const static int RIGHT = -1;

        ElementType *array = NULL;

        int beginsAt = 0;
        int length = 0;

        /**
        Método para verificar se a lista é igual à outra.
        */
        bool equals(StaticList &list) {

            // Verifica se o tamanho das listas é diferente.
            if (list.length != length) {
                return false;
            }

            // Percorre os elementos, verificando se são diferentes.
            for (int index = 0; index < length; index++) {
                if (list.get(index) != get(index)) {
                    return false;
                }
            }
            return true;
        }

        /**
        Método para retornar o relativo, levando em conta
        a posição em que a lista começa.
        */
        int getRelativeIndex(int index) {
            return (beginsAt + index) % length;
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
        Método para mover a lista para a esquerda ou direita.
        */
        void move(int direction) {
            beginsAt += direction == LEFT ? 1 : -1;
            beginsAt = beginsAt < 0 ? (length + beginsAt) : (beginsAt % length);
        }

    public:
        /**
        Construtor da classe.
        */
        StaticList(int size) {
            if (size < 0) {
                throw std::invalid_argument("size must be a positive number");
            }

            length = size;
            array = new ElementType[length];

        }

        /**
        Destrutor da classe.
        */
        ~StaticList() {
            delete[] array;
        }

        /**
        Método para retornar um elemento, a partir de um índice, 
        utilizando a sintaxe dos colchetes.
        */
        ElementType &operator [](int index) {
            return get(index);
        }

        /**
        Método para mover a lista N vezes à esquerda.
        */
        void operator <<(int steps) {
            steps %= length;

            for (int i = 0; i < steps; i++) {
                move(LEFT);
            }
        }

        /**
        Método para mover a lista N vezes à direita.
        */
        void operator >>(int steps) {
            steps %= length;

            for (int i = 0; i < steps; i++) {
                move(RIGHT);
            }
        }

        /**
        Método para verificar se a lista é igual à outra, 
        utilizando o operador de comparação.
        */
        bool operator ==(StaticList &list) {
            return equals(list);
        }

        /**
        Método para verificar se a lista é diferente de outra, 
        utilizando o operador de comparação.
        */
        bool operator !=(StaticList &list) {
            return !equals(list);
        }

        /**
        Método para retornar o tamanho da lista.
        */
        int getLength() {
            return length;
        }

        /**
        Método para verificar se a lista possui um dado elemento.
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
        Método para contar quantos elementos X existem na lista.
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
        Método para retornar o índice de um dado elemento.
        */
        int indexOf(ElementType element) {
            for (int index = 0; index < length; index++) {
                if (array[index] == element) {

                    // Retorna o índice relativo.
                    if (index < beginsAt) {
                        return length - (beginsAt - index);
                    }
                    return index - beginsAt;
                }
            }
            return -1;
        }

        /**
        Método para preencher a lista com um dado elemento.
        */
        void fill(ElementType element) {
            for (int index = 0; index < length; index++) {
                array[index] = element;
            }
        }

        /**
        Método para definir um elemento, em um dado índice.
        */
        void set(int index, ElementType element) {
            validateIndex(index);
            array[getRelativeIndex(index)] = element;
        }

        /**
        Método para retornar um elemento, a partir de um índice.
        */
        ElementType &get(int index) {
            validateIndex(index);
            return array[getRelativeIndex(index)];

        }

        /**
        Método para retornar uma cópia da lista, copiando todos os seus elementos.
        */
        StaticList<ElementType> &copy() {
            StaticList<ElementType> *newList = new StaticList<ElementType>(length);

            for (int index = 0; index < length; index++) {
                newList->array[index] = array[index];
            }
            
            newList->beginsAt = beginsAt;
            return *newList;
        }
};