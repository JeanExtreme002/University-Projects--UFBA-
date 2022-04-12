from ..parser import parse_complex_value
from .errors import *
import os

__all__ = ("load_matrices", "save_matrices")

def get_matrix_from_string(string):
    # Verifica se a linha está vazia.
    string = string.replace("\n", "")
    if not string: return None
    
    # Separa a linha em assinatura (nome, ordem) e valores.
    signature, values = string.split(":", maxsplit = 1)
    name, order = signature.upper().split(maxsplit = 1)
    
    # Obtém a ordem da matrix.
    order = [int(v) for v in order.split(",", maxsplit = 1)]

    # Verifica se o nome da matriz é válido e adiciona ao dicionário.
    if not name.isalpha(): raise ValueError("O nome \"{}\" para matriz não é permitido!".format(name))
    matrix = {"name": name, "order": order, "values": list()}
    
    # Separa os valores pela vírgula e os converte para números, reais ou complexos.
    for value in values.split(","):
        matrix["values"].append(parse_complex_value(value) if "i" in value else float(value))
    return matrix
        
def load_matrices(filename):
    """
    Função geradora para retornar matrizes de um arquivo.
    As matrizes do arquivo devem estar no formato "NOME linha,coluna: valor1, valor2, ..."
    """
    if not os.path.exists(filename): raise UserFileNotFoundError(filename)
    
    with open(filename) as file:
        for line in file:
            try:
                matrix = get_matrix_from_string(line)
                if matrix: yield matrix
            except: raise UserFileDecodingError

def save_matrices(filename, matrices):
    """
    Função para salvar uma lista de matrizes em um arquivo.s
    """
    with open(filename, "w") as file:
        # Percorre o dicionário de matrizes, salvando uma matriz em cada linha.
        for matrix in matrices:
            line = "{} {},{}: ".format(matrix["name"], *matrix["order"])

            # Percorre os elementos da matrix, inserindo-os na string..
            for value in matrix["values"]:
                if isinstance(value, complex): value = "({}{}i)".format(value.real, ("+" + str(value.imag)) if value.imag >= 0 else value.imag)
                else: value = str(value)
                
                line += value + ", "

            # Escreve a linha no arquivo.
            file.write(line[:-2] + "\n")
