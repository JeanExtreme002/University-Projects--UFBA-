#include <stdexcept>

/**
LinkedElement é uma struct utilizada pela classe LinkedStack, no qual 
possuirá o seu próprio conteúdo e o endereço dos elementos vinculados ao mesmo.
*/
template <typename Type> struct LinkedElement {
    Type content;
    LinkedElement<Type> *previous;
    LinkedElement<Type> *next;
};


/**
LinkedStack é uma classe para criar pilhas dinâmicas, onde cada 
elemento estará vinculado com o próximo elemento da pilha.
*/
template <typename ElementType> class LinkedStack {
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

            // Se o índice for maior que a metade da pilha, é mais eficiente começar 
            // a busca a partir do final da pilha.
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
        Método para comparar uma pilha com outra.
        */
        bool equals(LinkedStack &stack) {

            // Verifica se o tamanho das pilhas é diferente.
            if (stack.getLength() != length) {
                return false;
            }

            struct LinkedElement<ElementType> *element1 = stack.lastElement;
            struct LinkedElement<ElementType> *element2 = lastElement;

            // Percorre os elementos de ambas as pilhas, verificando se são diferentes.
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
        Método para validar um índice, verificando se ele é menor que o tamanho da pilha.
        */
        bool validateIndex(int index, bool throwError = false) {
            if (index < length) {
                return true;
            }

            if (throwError) {
                throw std::out_of_range("stack index out of range");
            }
            return false;
        }

    public:
        /**
        Destrutor da classe.
        */
        ~LinkedStack() {
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
        Método para adicionar um elemento na pilha, utilizando a atribuição com soma.
        */
        void operator +=(ElementType element) {
            return add(element);
        }

        /**
        Método para verificar se a pilha é igual à outra, 
        utilizando o operador de comparação.
        */
        bool operator ==(LinkedStack &stack) {
            return equals(stack);
        }

        /**
        Método para verificar se a pilha é diferente de outra, 
        utilizando o operador de comparação.
        */
        bool operator !=(LinkedStack &stack) {
            return !equals(stack);
        }             

        /**
        Método para retornar o tamanho da pilha.
        */
        int getLength() {
            return length;
        }

        /**
        Método para limpar a pilha.
        */
        void clear() {
            while (length != 0) {
                remove();
            }
        }

        /**
        Método para verificar se a pilha possui um determinado elemento.
        */
        bool contains(ElementType element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;

            // Percorre os elementos da pilha, verificando
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
        Método para contar quantos elementos X existem na pilha.
        */
        int count(ElementType element) {
            struct LinkedElement<ElementType> *targetElement = lastElement;
            int elementCount = 0;

            // Percorre os elementos da pilha, verificando
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

            // Percorre os elementos da pilha, verificando 
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
        Método para adicionar um elemento na pilha.
        */
        void add(ElementType element) {

            // Cria um LinkedElement para o elemento a ser inserido.
            struct LinkedElement<ElementType> *newElement = createLinkedElement(element);

            // Se não houver elemento na pilha, o elemento será adicionado como 
            // o primeiro e último da pilha.
            if (length == 0) {
                firstElement = newElement;
                firstElement->previous = newElement;
                firstElement->next = newElement;

                lastElement = firstElement;
            }

            // Insere o elemento no final da pilha, vinculando o último elemento com o elemento 
            // da inserção e o elemento da inserção com o primeiro elemento. Após isso, o último 
            // elemento passará a ser o elemento da inserção.
            else {
                newElement->next = firstElement;
                newElement->previous = lastElement;

                lastElement->next = newElement;
                firstElement->previous = newElement;

                lastElement = newElement;
            }

            // Computa a inserção do elemento na pilha.
            length++;
        }

        /**
        Método para adicionar todos os elementos de uma dada pilha.
        */
        void expand(LinkedStack<ElementType> &stack) {
            struct LinkedElement<ElementType> *element = stack.lastElement;

            for (int index = 0; index < stack.getLength(); index++) {
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
        Método para remover o próximo elemento da pilha.
        */
        ElementType remove() {

            // Remove o último elemento (último a entrar) da pilha, vinculando o
            // penúltimo elemento com o primeiro elemento. Após isso, o penúltimo 
            // elemento da pilha será o último elemento.
            struct LinkedElement<ElementType> *targetElement = lastElement;
            
            targetElement->previous->next = firstElement;
            firstElement->previous = targetElement->previous;

            lastElement = targetElement->previous;

            // Salva o conteúdo e apaga o elemento da memória.
            ElementType content = targetElement->content;
            delete targetElement;

            // Computa a remoção do elemento.
            length--;

            return content;
        }

        /**
        Método para retornar uma cópia da pilha, copiando todos os seus elementos.
        */
        LinkedStack<ElementType> &copy() {

            // Cria na memória um novo objeto da pilha.
            LinkedStack<ElementType> * newStack = new LinkedStack<ElementType>;

            // Adiciona todos os elementos no novo objeto.
            newStack->expand(*this);
            return *newStack;
        }
};