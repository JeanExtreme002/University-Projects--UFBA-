def comparar_strings(string1, string2) -> bool:
    """
    Compara as atrings, alfabeticamente, e verifica
    se a primeira string é "menor ou igual" que a segunda string.
    """

    # Retorna True se a segunda string for infinito.
    if string2 == float("inf"): return True

    for i in range(min([len(string1), len(string2)])):

        # Se o código ASCII do caractere da primeira string for maior, então
        # retorna False. Se for menor, retorna True. E se for igual, continua.
        if ord(string1[i]) > ord(string2[i]):
            return False

        elif ord(string1[i]) < ord(string2[i]):
            return True

    # Caso passe na verificação alfabética, o tamanho das duas strings é comparado.
    return len(string1) <= len(string2)

def comparar_valores(value1, value2, tipo) -> bool:
    """
    Obtém dois valores, de mesmo tipo, e verifica se o
    primeiro valor é "menor ou igual" que o segundo valor.
    """
    return comparar_strings(value1, value2) if tipo is str else (value1 <= value2)

def ordenar_relacao(relacao) -> list:
    """
    Obtém uma lista [(a, b), (g, h) ... (x, y)] e a retorna em ordem lexicográfica.
    """

    # Se a lista estiver vazia, uma lista vazia será retornada.
    if not relacao : return list()

    # Cria uma cópia da lista para que a mesma possa ser manipulada ser afetar
    # a lista original. Aqui não é utilizado o método copy() para que as sublistas
    # também sejam copiadas, fazendo assim uma "cópia profunda".
    relacao = [tuple(par) for par in relacao]

    # Obtém o tipo dos valores X e Y.
    tipo_valor_x = type(relacao[0][0])
    tipo_valor_y = type(relacao[0][1])

    relacao_ordenada = []

    for i in range(len(relacao)):

        # Para iniciar a verificação, o menor valor por padrão para cada iteração é infinito.
        par_menor = (float("inf"), float("inf"))
        obtido = False

        # Percorre todos os pares da relação para verificar qual é o menor entre eles.
        for par in relacao:

            # Caso exista dois pares iguais na lista, apenas um deles será adicionado à relação ordenada.
            if par in relacao_ordenada: continue

            # Se o tipo do elemento X ou Y for diferente do tipo registrado, será lançado um erro.
            if not isinstance(par[0], tipo_valor_x) or not isinstance(par[1], tipo_valor_y):
                raise TypeError("Os tipos dos elementos X e Y devem ser iguais para todos os pares")

            # O par é menor que o menor par registrado se seu X for menor ou se seu X for igual e seu Y for menor.
            if comparar_valores(par[0], par_menor[0], tipo_valor_x):
                if par[0] != par_menor[0] or comparar_valores(par[1], par_menor[1], tipo_valor_y):
                    par_menor = par
                    obtido = True

        # Remove o menor par encontrado da relação, adicionando-o à relação ordenada.
        if obtido:
            relacao.remove(par_menor)
            relacao_ordenada.append(par_menor)

    return relacao_ordenada
