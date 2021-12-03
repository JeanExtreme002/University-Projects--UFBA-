def verificar_permutabilidade(relacao):
    dominio = set()
    imagem = set()

    for x, y in relacao:

        if x in dominio and y in imagem:
            return False
            
        if x != y:
            dominio.add(x)
            imagem.add(y)

    return dominio == imagem

def relacao_para_ciclica(relacao):
    relacao = relacao.copy()

    ciclica = []
    ciclica.append(list(relacao[0]))
    del relacao[0]

    for par in relacao:
        if par[0] == par[1]:
            relacao.remove(par)

    while relacao:
        for par in relacao:
            if par[0] == ciclica[-1][-1]:
                relacao.remove(par)

                if par[1] != ciclica[-1][0]:
                    ciclica[-1].append(par[1])

                if par[1] == ciclica[-1][0] and relacao:
                    ciclica.append(list(relacao[0]))
                    del relacao[0]
                break
    return ciclica

def relacao_para_matricial(relacao):
    dominio = []
    imagem = []

    for x, y in relacao:
        dominio.append(str(x))
        imagem.append(str(y))

    for e in range(len(dominio)):
        if len(dominio[e]) > len(imagem[e]):
            imagem[e] = (" " * (len(dominio[e]) - len(imagem[e]))) + imagem[e]
        else:
            dominio[e] = (" " * (len(imagem[e]) - len(dominio[e]))) + dominio[e]

    return "  ".join(dominio) + "\n" + "  ".join(imagem)
