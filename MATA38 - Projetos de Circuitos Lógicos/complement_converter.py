__author__ = "Jean Loui Bernard Silva de Jesus"

from binary_calculator import add_binary

def convert_binary_to_ones_complement(binary: str):
    # Realiza o flip-flop (troca de bit).
    binary = ["0" if bit == "1" else "1" for bit in binary]
    return "".join(binary)

def convert_binary_to_twos_complement(binary: str):
    # Converte para complemento de 1 e depois soma 1.
    binary = convert_binary_to_ones_complement(binary)
    return add_binary(binary, "1")
