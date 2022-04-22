#include <stdexcept>

/**
LinkedElement é uma struct utilizada pela classe LinkedList, no qual 
possuirá o seu próprio conteúdo e o endereço do elemento ao qual está vinculado.
*/
template <typename Type> struct LinkedElement {
    Type content;
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

        LinkedElement<ElementType> *firstElement;
        int length = 0;

        /**
        Método para criar um novo objeto de LinkedElement, retornando o seu ponteiro.
        */
        struct LinkedElement<ElementType> *createLinkedElement(ElementType element) {
            struct LinkedElement<ElementType> *newElement = new LinkedElement<ElementType>;

            newElement->content = element;
            newElement->next = NULL;

            return newElement;
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

    public:
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
        Método para inserir um elemento em uma posição existente da lista.
        */
        void insert(int index, ElementType element) {

            // Valida o índice recebido.
            if (index != BEGIN && index != END) {
                validateIndex(index, true);
            }

            // Cria um LinkedElement para o elemento a ser inserido.
            struct LinkedElement<ElementType> *newElement = createLinkedElement(element);

            // Se não houver elemento na lista, o elemento será adicionado como o primeiro.
            if (length++ == 0) {
                firstElement = newElement;
                return;
            }

            // Caso solicitado a inserção do elemento no início da lista, será necessário
            // apenas fazê-lo apontar para o atual elemento na primeira posição e trocar o objeto.
            if (index == BEGIN) {
                newElement->next = firstElement;
                firstElement = newElement;
                return;
            }

            // Caso solicitado a inserção do elemento no final da lista, o índice será trocado
            // pela quantidade de elementos que a lista possui.
            if (index == END) {
                index = length - 1; // Subtrai (+1) porque a inserção já foi computada lá em cima.
            }

            // Percorre todos os elementos ligados até chegar ao elemento alvo.
            struct LinkedElement<ElementType> *previousElement = NULL;
            struct LinkedElement<ElementType> *targetElement = firstElement;

            while (--index >= 0) {
                previousElement = targetElement;
                targetElement = targetElement->next;
            }
    
            // Insere no elemento na lista, colocando-o entre o elemento anterior
            // e o atual elemento no índice especificado.
            previousElement->next = newElement;
            newElement->next = targetElement;
        }

        /**
        Método para obter um elemento a partir de um índice, utilizando a sintaxe dos colchetes.
        */
        ElementType operator[](int index) {
            return get(index);
        }

        /**
        Método para obter um elemento a partir de um índice.
        */
        ElementType get(int index) {

            // Valida o índice recebido.
            validateIndex(index, true);

            // Obtém o elemento no índice especificado.
            struct LinkedElement<ElementType> *targetElement = firstElement;
            
            for (int i = 0; i < index && targetElement->next != NULL; i++) {
                targetElement = targetElement->next;
            }

            // Retorna o seu conteúdo.
            return targetElement->content;
        }

        ElementType remove(int index) {

            // Valida o índice recebido.
            validateIndex(index, true);

            // Computa a remoção de elemento.
            length--;

            // Caso solicitado a remoção do elemento no primeiro índice, será necessário
            // apenas fazê-lo apontar para o elemento da segunda posição e trocar o objeto.
            if (index == BEGIN) {
                struct LinkedElement<ElementType> *targetElement = firstElement;

                if (length != 0) {
                    firstElement = targetElement->next;
                }
                return targetElement->content;
            }

            // Obtém o elemento no índice especificado.
            struct LinkedElement<ElementType> *previousElement = NULL;
            struct LinkedElement<ElementType> *targetElement = firstElement;

            while (--index >= 0) {
                previousElement = targetElement;
                targetElement = targetElement->next;
            }

            // Conecta o elemento anterior com o sucessor do elemento alvo.
            previousElement->next = targetElement->next;
            return targetElement->content;
        }
};