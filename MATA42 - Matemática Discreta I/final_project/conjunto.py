def salvar_conjunto(conjunto, nome_do_arquivo, encoding = None):
    """
    Salva um conjunto dentro de um arquivo.
    """

    with open(nome_do_arquivo, "w", encoding = encoding) as arquivo:

        # Converte o conjunto para string.
        conjunto = "{" + ", ".join([str(elemento) for elemento in conjunto]) + "}"

        # Escreve o conteúdo no arquivo.
        arquivo.write(conjunto)
