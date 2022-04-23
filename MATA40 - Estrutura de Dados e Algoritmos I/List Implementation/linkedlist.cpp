#include <stdexcept>

/**
LinkedElement é uma struct utilizada pela classe LinkedList, no qual 
possuirá o seu próprio conteúdo e o endereço dos elementos vinculados ao mesmo.
*/
template <typename Type> struct LinkedElement {
    Type content;
    LinkedElement<Type> *previous;
    LinkedElement<Type> *next;
};


/**
LinkedList é uma classe para criar listas dinâmicas, onde cada 
elemento estará vinculado com próximo elemento da lista.
*/
template <typename ElementType> class LinkedList {
    private:
        const int BEGIN = 0;
        const int END = -1;
        const int LEFT = 0;
        const int RIGHT = -1;

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

            // Se o índice for maior que a metade da lista, é mais eficiente começar 
            // a busca a partir do final da lista.
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
        Método para validar um índice, verificando se ele é menor que o tamanho da lista.
        */
        bool validateIndex(int index, bool throwError = false) {
            if (index < length) {
                return true;
            }

            if (throwError) {
                throw std::out_of_range("list index out of range");
            }
            return false;
        }

        void move(int direction) {
            // Não é possível mover a lista caso haja menos de dois elementos.
            if (length < 2) {
                return;
            }

            struct LinkedElement<ElementType> *start;
            struct LinkedElement<ElementType> *end;

            // Move a lista para a esquerda ou direita, alterando 
            // o elemento inicial e final da lista.
            if (direction == LEFT) {
                start = firstElement->next;
                end = firstElement;
            } 
            else {
                start = lastElement;
                end = lastElement->previous;
            }

            firstElement = start;
            lastElement = end;
        }

    public:
        /**
        Destrutor da classe.
        */
        ~LinkedList() {
            clear();
        }

        /**
        Método para retornar um elemento, a partir de um índice, utilizando a sintaxe dos colchetes.
        */
        ElementType operator [](int index) {
            return get(index);
        }

        /**
        Método mover a lista N vezes à esquerda.
        */
        void operator <<(int steps) {
            steps %= length;

            for (int i = 0; i < steps; i++) {
                move(LEFT);
            }
        }

        /**
        Método mover a lista N vezes à direita.
        */
        void operator >>(int steps) {
            steps %= length;

            for (int i = 0; i < steps; i++) {
                move(RIGHT);
            }
        }

        /**
        Método para adicionar um elemento ao final da lista, utilizando a atribuição com soma.
        */
        void operator +=(ElementType element) {
            return add(element);
        }       

        /**
        Método para retornar o tamanho da lista.
        */
        int getLength() {
            return length;
        }

        /**
        Método para adicionar um elemento ao final da lista.
        */
        void add(ElementType element) {
            insert(END, element);
        }

        /**
        Método para limpar a lista.
        */
        void clear() {
            while (length != 0) {
                remove(0);
            }
        }

        /**
        Método para verificar se a lista possui um determinado elemento.
        */
        bool contains(ElementType element) {
            for (int index = 0; index < length; index++) {
                if (get(index) == element) {
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
                elementCount += get(index) == element ? 1 : 0;
            }
            return elementCount;
        }

        /**
        Método para inserir um elemento em uma posição existente da lista.
        */
        void insert(int index, ElementType element) {

            // Valida o índice recebido.
            if (index != BEGIN && index != END) {
                validateIndex(index, true);
            }

            // Cria um LinkedElement para o elemento a ser inserido.
            struct LinkedElement<ElementType> *newElement = createLinkedElement(element);

            // Se não houver elemento na lista, o elemento será adicionado como 
            // o primeiro e último da lista.
            if (length++ == 0) {
                firstElement = newElement;
                firstElement->previous = newElement;
                firstElement->next = newElement;

                lastElement = newElement;
                lastElement->previous = newElement;
                lastElement->next = newElement;
                return;
            }

            // Caso solicitado a inserção do elemento no início da lista, será necessário
            // apenas vincular o último elemento com o elemento da inserção e o elemento
            // da inserção com o primeiro elemento. Após isso, o primeiro elemento passará
            // a ser o elemento da inserção.
            if (index == BEGIN) {
                newElement->next = firstElement;
                newElement->previous = lastElement;

                firstElement->previous = newElement;
                lastElement->next = newElement;

                firstElement = newElement;
                return;
            }

            // Caso solicitado a inserção do elemento no final da lista, será necessário
            // apenas vincular o último elemento com o elemento da inserção e o elemento
            // da inserção com o primeiro elemento. Após isso, o último elemento passará
            // a ser o elemento da inserção.
            if (index == END) {
                newElement->next = firstElement;
                newElement->previous = lastElement;

                lastElement->next = newElement;
                lastElement = newElement;
                return;
            }

            // Obtém o elemento alvo, através do índice especificado.
            struct LinkedElement<ElementType> *targetElement = getLinkedElement(index);
    
            // Insere no elemento na lista, colocando-o entre o elemento anterior
            // e o atual elemento no índice especificado.
            newElement->next = targetElement;
            newElement->previous = targetElement->previous;

            targetElement->previous->next = newElement;
            targetElement->previous = newElement;
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
        Método para remover um elemento, a partir de um índice.
        */
        ElementType remove(int index) {

            // Valida o índice recebido.
            validateIndex(index, true);

            // Computa a remoção de elemento.
            length--;

            // Caso solicitado a remoção do elemento no primeiro índice, será necessário
            // apenas vincular o segundo elemento com o último elemento. Após isso, 
            // o primeiro elemento da lista será o segundo elemento.
            if (index == BEGIN) {
                struct LinkedElement<ElementType> *targetElement = firstElement;

                lastElement->next = targetElement->next;
                targetElement->next->previous = lastElement;

                firstElement = targetElement->next;
                ElementType content = targetElement->content;

                delete targetElement;
                return content;
            }

            // Caso solicitado a remoção do último elemento da lista, será necessário
            // apenas vincular o penúltimo elemento com o primeiro elemento. Após isso,
            // o penúltimo elemento da lista será o último elemento.
            if (index == length - 1) {
                struct LinkedElement<ElementType> *targetElement = lastElement;

                targetElement->previous->next = firstElement;
                firstElement->previous = targetElement->previous;

                ElementType content = targetElement->content;

                delete targetElement;
                return content;
            }

            // Obtém o elemento alvo, através do índice especificado.
            struct LinkedElement<ElementType> *targetElement = getLinkedElement(index);

            // Conecta o elemento anterior com o sucessor do elemento alvo.
            targetElement->previous->next = targetElement->next;
            ElementType content = targetElement->content;

            delete targetElement;
            return content;
        }
};