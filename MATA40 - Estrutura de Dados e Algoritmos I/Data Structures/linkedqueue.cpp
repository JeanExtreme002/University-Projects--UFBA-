#include <stdexcept>

/**
LinkedElement é uma struct utilizada pela classe LinkedQueue, no qual 
possuirá o seu próprio conteúdo e o endereço dos elementos vinculados ao mesmo.
*/
template <typename Type> struct LinkedElement {
    Type content;
    LinkedElement<Type> *previous;
    LinkedElement<Type> *next;
};


/**
LinkedQueue é uma classe para criar filas dinâmicas, onde cada 
elemento estará vinculado com o próximo elemento da fila.
*/
template <typename ElementType> class LinkedQueue {
    private:
        int length = 0;

        LinkedElement<ElementType> *firstElement = NULL;
        LinkedElement<ElementType> *lastElement = NULL;

        /**
        Método para criar um novo objeto de LinkedElement, retornando o seu ponteiro.
        */
        struct LinkedElement<ElementType> *createLinkedElement(ElementType element) {
            struct LinkedElement<ElementType> *newElement = new LinkedElement<ElementType>;

            newElement->content = element;
            newElement->previous = NULL;
            newElement->next = NULL;

            return newElement;
        }

        /**
        Método para retornar um elemento, ponteiro de LinkedElement, através do índice.
        */
        struct LinkedElement<ElementType> *getLinkedElement(int index) {
            struct LinkedElement<ElementType> *targetElement;
            bool searchFromBegin = (index < length / 2);

            // Se o índice for maior que a metade da fila, é mais eficiente começar 
            // a busca a partir do final da fila.
            if (searchFromBegin) {
                targetElement = firstElement;
            }
            else {
                targetElement = lastElement;
                index = length - index - 1;
            }

            // Percorre os elementos, começando da direita para esquerda ou da esquerda para direita.
            for (int i = 0; i < index; i++) {
                targetElement = searchFromBegin ? targetElement->next : targetElement->previous;
            }

            // Retorna o elemento encontrado.
            return targetElement;
        }

        /**
        Método para comparar uma fila com outra.
        */
        bool equals(LinkedQueue &queue) {

            // Verifica se o tamanho das filas é diferente.
            if (queue.getLength() != length) {
                return false;
            }

            struct LinkedElement<ElementType> *element1 = queue.lastElement;
            struct LinkedElement<ElementType> *element2 = lastElement;

            // Percorre os elementos de ambas as filas, verificando se são diferentes.
            for (int i = 0; i < length; i++) {
                element1 = element1->next;
                element2 = element2->next;

                if (element1->content != element2->content) {
                    return false;
                }
            }
            return true;
        }

        /**
        Método para validar um índice, verificando se ele é menor que o tamanho da fila.
        */
        bool validateIndex(int index, bool throwError = false) {
            if (index < length) {
                return true;
            }

            if (throwError) {
                throw std::out_of_range("queue index out of range");
            }
            return false;
        }

    public:
        /**
        Destrutor da classe.
        */
        ~LinkedQueue() {
            clear();
        }

        /**
        Método para retornar um elemento, a partir de um índice, 
        utilizando a sintaxe dos colchetes.
        */
        ElementType operator [](int index) {
            return get(index);
        }

        /**
        Método para adicionar um elemento na fila, utilizando a atribuição com soma.
        */
        void operator +=(ElementType element) {
            return add(element);
        }

        /**
        Método para verificar se a fila é igual à outra, 
        utilizando o operador de comparação.
        */
        bool operator ==(LinkedQueue &queue) {
            return equals(queue);
        }

        /**
        Método para verificar se a fila é diferente de outra, 
        utilizando o operador de comparação.
        */
        bool operator !=(LinkedQueue &queue) {
            return !equals(queue);
        }             

        /**
        Método para retornar o tamanho da fila.
        */
        int getLength() {
            return length;
        }

        /**
        Método para limpar a fila.
        */
        void clear() {
            while (length != 0) {
                remove();
            }
        }

        /**
        Método para verificar se a fila possui um determinado elemento.
        */
        bool contains(ElementType element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;

            // Percorre os elementos da fila, verificando
            // se um deles é igual ao elemento recebido.
            for (int i = 0; i < length; i++) {
                targetElement = targetElement->next;

                if (targetElement->content == element) {
                    return true;
                }
            }
            return false;
        }

        /**
        Método para contar quantos elementos X existem na fila.
        */
        int count(ElementType element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;
            int elementCount = 0;

            // Percorre os elementos da fila, verificando
            // se são iguais ao elemento recebido.
            for (int i = 0; i < length; i++) {
                targetElement = targetElement->next;

                if (targetElement->content == element) {
                    elementCount++;
                }
            }
            return elementCount;
        }

        /**
        Método para retornar o índice de um dado elemento.
        */
        int indexOf(ElementType element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;

            // Percorre os elementos da fila, verificando 
            // se são iguais ao elemento recebido.
            for (int index = 0; index < length; index++) {
                targetElement = targetElement->next;

                if (targetElement->content == element) {
                    return index;
                }
            }
            return -1;
        }

        /**
        Método para adicionar um elemento na fila.
        */
        void add(ElementType element) {

            // Cria um LinkedElement para o elemento a ser inserido.
            struct LinkedElement<ElementType> *newElement = createLinkedElement(element);

            // Se não houver elemento na fila, o elemento será adicionado como 
            // o primeiro e último da fila.
            if (length == 0) {
                firstElement = newElement;
                firstElement->previous = newElement;
                firstElement->next = newElement;

                lastElement = firstElement;
            }

            // Insere o elemento no final da fila, vinculando o último elemento com o elemento 
            // da inserção e o elemento da inserção com o primeiro elemento. Após isso, o último 
            // elemento passará a ser o elemento da inserção.
            else {
                newElement->next = firstElement;
                newElement->previous = lastElement;

                lastElement->next = newElement;
                firstElement->previous = newElement;

                lastElement = newElement;
            }

            // Computa a inserção do elemento na fila.
            length++;
        }

        /**
        Método para adicionar todos os elementos de uma dada fila.
        */
        void expand(LinkedQueue<ElementType> &queue) {
            struct LinkedElement<ElementType> *element = queue.lastElement;

            for (int index = 0; index < queue.getLength(); index++) {
                element = element->next;
                add(element->content);
            }
        }

        /**
        Método para retornar um elemento, a partir de um índice.
        */
        ElementType get(int index) {

            // Valida o índice recebido.
            validateIndex(index, true);

            // Obtém o elemento alvo, através do índice especificado.
            struct LinkedElement<ElementType> *targetElement = getLinkedElement(index);

            // Retorna o seu conteúdo.
            return targetElement->content;
        }

        /**
        Método para remover o próximo elemento da fila.
        */
        ElementType remove() {

            // Remove o primeiro elemento da fila, vinculando o segundo elemento com
            // o último elemento. Após isso, o segundo elemento passará a ser o primeiro.
            struct LinkedElement<ElementType> *targetElement = firstElement;

            lastElement->next = targetElement->next;
            targetElement->next->previous = lastElement;

            firstElement = targetElement->next;

            // Salva o conteúdo e apaga o elemento da memória.
            ElementType content = targetElement->content;
            delete targetElement;

            // Computa a remoção do elemento.
            length--;

            return content;
        }

        /**
        Método para retornar uma cópia da fila, copiando todos os seus elementos.
        */
        LinkedQueue<ElementType> &copy() {

            // Cria na memória um novo objeto da fila.
            LinkedQueue<ElementType> * newQueue = new LinkedQueue<ElementType>;

            // Adiciona todos os elementos no novo objeto.
            newQueue->expand(*this);
            return *newQueue;
        }
};