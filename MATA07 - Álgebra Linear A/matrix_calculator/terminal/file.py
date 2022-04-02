from .parser import parse_complex_value

def load_matrices(filename, convert_to):
    matrices = dict()
    
    with open(filename) as file:
        for line in file:

            # Verifica se a linha está vazia.
            line = line.replace("\n", "")
            if not line: continue
            
            # Separa a linha em assinatura (nome, ordem) e valores.
            signature, values = line.split(":", maxsplit = 1)
            name, order = signature.upper().split(maxsplit = 1)
            
            # Obtém a ordem da matrix.
            order = [int(v) for v in order.split(",", maxsplit = 1)]

            # Verifica se o nome da matriz e adiciona ao dicionário.
            if not name.isalpha(): raise ValueError("O nome \"{}\" para matriz não é permitido!".format(name))
            matrices[name] = list()
            
            # Obtém uma lista com todos os valores da matriz
            for value in values.split(","):
                value = value.strip().replace(" ", "")
                matrices[name].append(parse_complex_value(value) if "i" in value else float(value))

            # Adiciona ao dicionário a matriz, com os valores já inseridos.
            matrices[name] = convert_to(*order, matrices[name])
    return matrices

def save_matrices(filename, matrices):
    with open(filename, "w") as file:

        # Percorre o dicionário de matrizes, salvando uma matriz em cada linha.
        for name, matrix in matrices.items():
            line = "{} {},{}: ".format(name, *matrix.get_order())

            # Percorre os elementos da matrix, inserindo-os na string..
            for row, column, value in matrix:
                line += "{}{}i".format(value.real, value.imag) if isinstance(value, complex) else str(value)
                if [row + 1, column + 1] != list(matrix.get_order()): line += ", "

            # Escreve a linha no arquivo.
            file.write(line + "\n")
        
