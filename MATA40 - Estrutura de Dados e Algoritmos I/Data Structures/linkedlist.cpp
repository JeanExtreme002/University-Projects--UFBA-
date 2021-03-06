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
        const static int BEGIN = 0;
        const static int END = -1;
        const static int LEFT = 0;
        const static int RIGHT = -1;

        int length = 0;

        LinkedElement<ElementType> *firstElement = NULL;
        LinkedElement<ElementType> *lastElement = NULL;

        /**
        Método para criar um novo objeto de LinkedElement, retornando o seu ponteiro.
        */
        struct LinkedElement<ElementType> *createLinkedElement(const ElementType &element) {
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
        Método para comparar uma lista com outra.
        */
        bool equals(LinkedList &list) {

            // Verifica se o tamanho das listas é diferente.
            if (list.getLength() != length) {
                return false;
            }

            struct LinkedElement<ElementType> *element1 = list.lastElement;
            struct LinkedElement<ElementType> *element2 = lastElement;

            // Percorre os elementos de ambas as listas, verificando se são diferentes.
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

        /**
        Método para mover a lista para a esquerda ou direita.
        */
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

        /**
        Método recursivo para ordenar a lista, utilizando o algoritmo QuickSort.
        */
        void quickSort(bool reverse, struct LinkedElement<ElementType> *first, struct LinkedElement<ElementType> *pivot, int steps) {
            
            // Se não houver itens para ordenar, ele encerra a execução.
            if (steps == 0) {
                return;
            }

            struct LinkedElement<ElementType> *elementOnRight = first;
            struct LinkedElement<ElementType> *element = first->previous;

            int separator = 0;

            // Organiza a lista em elementos menores e maiores que o pivô recebido.
            for (int index = 0; index < steps; index++) {
                element = element->next;

                // Se o elemento for menor que o pivô, ele será colocado à esquerda do separador.
                if (compare(reverse, element->content, pivot->content)) {
                    ElementType content = element->content;

                    element->content = elementOnRight->content;
                    elementOnRight->content = content;

                    elementOnRight = elementOnRight->next;
                    separator++;
                }
            }

            // Divide a lista em duas partes e realiza o mesmo procedimento para as suas metades.
            quickSort(reverse, first, elementOnRight->previous->previous, separator - 1);
            quickSort(reverse, elementOnRight, pivot, steps - separator);
        }

        /**
        Método utilizado pelo método de "sorting" para comparar os elementos.
        */
        bool compare(bool reverse, const ElementType &element1, const ElementType &element2) {
            if (!reverse && (element1 <= element2)) {
                return true;
            }
            if (reverse && (element1 >= element2)) {
                return true;
            }
            return false;
        }

    public:
        /**
        Destrutor da classe.
        */
        ~LinkedList() {
            clear();
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
            if (length == 0) {
                return;
            }

            steps %= length;

            for (int i = 0; i < steps; i++) {
                move(LEFT);
            }
        }

        /**
        Método para mover a lista N vezes à direita.
        */
        void operator >>(int steps) {
            if (length == 0) {
                return;
            }
            
            steps %= length;

            for (int i = 0; i < steps; i++) {
                move(RIGHT);
            }
        }

        /**
        Método para adicionar um elemento ao final da lista, utilizando a atribuição com soma.
        */
        void operator +=(const ElementType &element) {
            return add(element);
        }

        /**
        Método para verificar se a lista é igual à outra, 
        utilizando o operador de comparação.
        */
        bool operator ==(LinkedList &list) {
            return equals(list);
        }

        /**
        Método para verificar se a lista é diferente de outra, 
        utilizando o operador de comparação.
        */
        bool operator !=(LinkedList &list) {
            return !equals(list);
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
        void add(const ElementType &element) {
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
        bool contains(const ElementType &element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;

            // Percorre os elementos da lista, verificando
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
        Método para contar quantos elementos X existem na lista.
        */
        int count(const ElementType &element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;
            int elementCount = 0;

            // Percorre os elementos da lista, verificando
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
        int indexOf(const ElementType &element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;

            // Percorre os elementos da lista, verificando 
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
        Método para inserir um elemento em uma posição existente da lista.
        */
        void insert(int index, const ElementType &element) {

            // Valida o índice recebido.
            if (index != BEGIN && index != END) {
                validateIndex(index, true);
            }

            // Cria um LinkedElement para o elemento a ser inserido.
            struct LinkedElement<ElementType> *newElement = createLinkedElement(element);

            // Se não houver elemento na lista, o elemento será adicionado como 
            // o primeiro e último da lista.
            if (length == 0) {
                firstElement = newElement;
                firstElement->previous = newElement;
                firstElement->next = newElement;

                lastElement = firstElement;
            }

            // Caso solicitado a inserção do elemento no início da lista, será necessário
            // apenas vincular o último elemento com o elemento da inserção e o elemento
            // da inserção com o primeiro elemento. Após isso, o primeiro elemento passará
            // a ser o elemento da inserção.
            else if (index == BEGIN) {
                newElement->next = firstElement;
                newElement->previous = lastElement;

                firstElement->previous = newElement;
                lastElement->next = newElement;

                firstElement = newElement;
            }

            // Caso solicitado a inserção do elemento no final da lista, será necessário
            // apenas vincular o último elemento com o elemento da inserção e o elemento
            // da inserção com o primeiro elemento. Após isso, o último elemento passará
            // a ser o elemento da inserção.
            else if (index == END) {
                newElement->next = firstElement;
                newElement->previous = lastElement;

                lastElement->next = newElement;
                firstElement->previous = newElement;

                lastElement = newElement;
            }

            // Caso solicitado a inserção do elemento entre dois elementos, será necessário
            // obter o elemento que ocupa a posição especificada, para então vincular
            // o elemento de inserção com o elemento anterior e o elemento que ocupa a posição.
            else {
                struct LinkedElement<ElementType> *targetElement = getLinkedElement(index);

                newElement->next = targetElement;
                newElement->previous = targetElement->previous;

                targetElement->previous->next = newElement;
                targetElement->previous = newElement;
            }

            // Computa a inserção do elemento na lista.
            length++;
        }

        /**
        Método para preencher a lista com um dado elemento.
        */
        void fill(const ElementType &element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;

            for (int index = 0; index < length; index++) {
                targetElement = targetElement->next;
                targetElement->content = element;
            }
        }

        /**
        Método para adicionar todos os elementos de uma dada lista.
        */
        void expand(LinkedList<ElementType> &list) {
            struct LinkedElement<ElementType> *element = list.lastElement;

            for (int index = 0; index < list.getLength(); index++) {
                element = element->next;
                add(element->content);
            }
        }

        /**
        Método para definir um elemento, em um dado índice.
        */
        void set(int index, const ElementType &element) {

            // Valida o índice recebido.
            validateIndex(index, true);  

            // Obtém o elemento alvo, através do índice especificado.
            struct LinkedElement<ElementType> *targetElement = getLinkedElement(index);

            targetElement->content = element;
        }

        /**
        Método para ordenar a lista (algoritmo: QuickSort).
        */
        void sort(bool reverse = false) {
            quickSort(reverse, firstElement, lastElement, length);
        }

        /**
        Método para retornar um elemento, a partir de um índice.
        */
        ElementType &get(int index) {

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
        void remove(int index) {

            // Valida o índice recebido.
            validateIndex(index, true);

            // Cria um ponteiro para receber o elemento a ser removido.
            struct LinkedElement<ElementType> *targetElement;

            // Caso solicitado a remoção do elemento no primeiro índice, será necessário
            // apenas vincular o segundo elemento com o último elemento. Após isso, 
            // o primeiro elemento da lista será o segundo elemento.
            if (index == BEGIN) {
                targetElement = firstElement;

                lastElement->next = targetElement->next;
                targetElement->next->previous = lastElement;

                firstElement = targetElement->next;
            }

            // Caso solicitado a remoção do último elemento da lista, será necessário
            // apenas vincular o penúltimo elemento com o primeiro elemento. Após isso,
            // o penúltimo elemento da lista será o último elemento.
            else if (index == (length - 1)) {
                targetElement = lastElement;
        
                targetElement->previous->next = firstElement;
                firstElement->previous = targetElement->previous;

                lastElement = targetElement->previous;
            }

            // Caso solicitado a remoção de um elemento entre dois elementos, será necessário
            // obter o elemento que ocupa a posição especificada, para então vincular o seu
            // elemento antecessor com o elemento sucessor, removendo a ligação do elemento alvo.
            else {
                targetElement = getLinkedElement(index);
                targetElement->previous->next = targetElement->next;
                targetElement->next->previous = targetElement->previous;
            }

            // Apaga o elemento da memória.
            delete targetElement;

            // Computa a remoção do elemento.
            length--;
        }

        /**
        Método para retornar uma cópia da lista, copiando todos os seus elementos.
        */
        LinkedList<ElementType> &copy() {

            // Cria na memória um novo objeto da lista.
            LinkedList<ElementType> * newList = new LinkedList<ElementType>;

            // Adiciona todos os elementos na nova lista.
            newList->expand(*this);
            return *newList;
        }
};