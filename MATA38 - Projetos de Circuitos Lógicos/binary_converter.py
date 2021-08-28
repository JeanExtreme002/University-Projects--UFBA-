__author__ = "Jean Loui Bernard Silva de Jesus"

def convert_binary_to_decimal(binary: str) -> float:
    # Guarda o sinal e transforma o valor em positivo.
    sign = -1 if "-" == binary[0] else 1
    binary = binary.replace("-", "")

    # Separa a parte inteira e a parte fracionária do valor binário.
    if not "." in binary: binary += "."
    integer_part, fractional_part = binary.split(".")

    decimal = 0

    # Inverte a string para realizar a conversão utilizando o índice do bit como expoente.
    integer_part = integer_part[::-1]

    # Converte a parte inteira do valor binário para decimal.
    for exponent in range(len(integer_part)):
        if integer_part[exponent] == "1": decimal += 2 ** exponent

    # Converte a parte fracionária do valor binário para decimal.
    for exponent in range(1, len(fractional_part) + 1):
        if fractional_part[exponent - 1] == "1": decimal += 2 ** -exponent
    return sign * decimal

def convert_decimal_to_binary(decimal: float) -> str:
    # Separa o sinal, a parte inteira e a parte fracionária do valor.
    sign, absolute_value = ("-" if decimal < 0 else ""), abs(decimal)
    integer_part = int(absolute_value)
    fractional_part = absolute_value - integer_part

    binary = ""

    # Converte a parte inteira para binário.
    while integer_part >= 1 or not binary:
        integer_part, remainder = divmod(integer_part, 2)
        binary = str(remainder) + binary

    # Converte a parte fracionária para binário, caso haja.
    if fractional_part != 0: binary += "."

    while fractional_part != 0:
        fractional_part *= 2
        bit = int(fractional_part)
        binary += str(bit)
        if bit: fractional_part -= bit

    return sign + binary
