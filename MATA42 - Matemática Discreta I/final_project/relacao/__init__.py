import json

def carregar_relacao(nome_do_arquivo, encoding = None) -> list:
    """
    Abre um arquivo contendo uma relação "{(x1,y1), (x2,y2)...}"
    e a retorna em formato de lista.
    """

    with open(nome_do_arquivo, encoding = encoding) as arquivo:

        # Faz o tratamento da string para que a mesma possa ser
        # convertida para uma lista, com o módulo JSON.
        relacao = arquivo.read().replace("'", '"').replace(" ", "").replace("\n", "").replace("\t", "")
        relacao = relacao.replace("{(", "{[").replace(",(", ",[")
        relacao = relacao.replace(")}", "]}").replace("),", "],")
        relacao = "[" + relacao[1: -1] + "]"

        # Retorna a relação convertida para lista.
        return json.loads(relacao)

def salvar_relacao(relacao, nome_do_arquivo, encoding = None):
    """
    Salva uma relação, em formato de lista de listas, dentro de um arquivo.
    """

    with open(nome_do_arquivo, "w", encoding = encoding) as arquivo:

        # Insere a chave de abertura da relação.
        arquivo.write("{\n")

        # Percorre todos os pares da relação e os salva no arquivo.
        for par in relacao:
            par = str(par).replace("[", "(").replace("]", ")").replace("'", '"')
            arquivo.write(" " * 2 + par + ",\n")

        # Insere a chave de fechamento da relação.
        arquivo.write("}")

def salvar_relacao_ciclica(relacao_ciclica, nome_do_arquivo, encoding = None):
    """
    Salva uma relação cíclica, em formato de lista de listas, dentro de um arquivo.
    """
    with open(nome_do_arquivo, "w", encoding = encoding) as arquivo:
        for ciclo in relacao_ciclica:
            arquivo.write(str(ciclo).replace("[", "(").replace("]", ")").replace("'", '"'))
