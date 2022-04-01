from .parser import parse_complex_value

def load_matrices(filename, convert_to = lambda row, column, iterable: None):
    matrices = dict()
    
    with open(filename) as file:
        for line in file:

            # Separa a linha em assinatura (nome, ordem) e valores.
            signature, values = line.replace("\n","").split(":", maxsplit = 1)
            name, order = signature.upper().split(maxsplit = 1)
            
            # Obtém a ordem da matrix.
            order = [int(v) for v in order.split(",", maxsplit = 1)]

            matrices[name] = list()
            
            # Obtém uma lista com todos os valores da matriz
            for value in values.split(","):
                matrices[name].append(parse_complex_value(value) if "i" in value else float(value))

            # Adiciona ao dicionário a matriz, com os valores já inseridos.
            matrices[name] = convert_to(*order, matrices[name])
    return matrices
