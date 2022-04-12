from .errors import *

def parse_complex_value(string):
    string = string.replace("(", "").replace(")", "").replace(" ", "").lower()

    # Verifica se é um número complexo.
    if string[-1] != "i": raise NoImaginaryPartError(string)
    
    string = string[:-1]
    real_part, imaginary_part, real = "", "", False

    # Percorre a string começando da parte imaginária.
    for index in range(len(string) - 1, -1, -1):
        char = string[index]

        # Se ainda estiver na parte imaginária, verifica se o caractere
        # é um sinal de soma ou subtração, indicando que os próximos
        # caracteres pertencem à parte real.
        if not real:
            if char in "+-": real = True
            imaginary_part = char + imaginary_part
        else: real_part = char + real_part

    # Transforma para o tipo complexo.
    if not imaginary_part.replace("-","").replace("+",""): imaginary_part += "1"
    if not real_part: real_part = 0
    return complex(float(real_part), float(imaginary_part))
