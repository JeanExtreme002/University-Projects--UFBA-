__author__ = "Jean Loui Bernard Silva de Jesus"

def convert_binary_to_decimal(binary: str) -> float:
    binary = binary.replace(".", ",")
    value = 0

    # Separa a parte inteira e a parte fracionária do valor binário.
    if not "," in binary: binary += ",0"
    integer, decimal = str(binary).split(",")

    # Inverte a string para realizar a conversão utilizando o índice do bit como expoente.
    integer = integer[::-1]

    # Converte a parte inteira do valor binário para decimal.
    for exp in range(len(integer)):
        value += int(integer[exp]) * 2 ** exp

    # Converte a parte fracionária do valor binário para decimal.
    for exp in range(1, len(decimal) + 1):
        value += int(decimal[exp - 1]) * 2 ** -exp
    return value

def convert_decimal_to_binary(value: float) -> str:
    binary = ""

    # Separa a parte inteira e a parte fracionária do valor.
    integer, decimal = str(float(value)).split(".")
    integer, decimal = int(integer), float("0." + decimal)

    # Converte a parte inteira para binário.
    while not integer in [0, 1]:
        integer, remainder = divmod(integer, 2)
        binary += str(remainder)

    binary = str(integer) + binary[::-1]

    # Converte a parte fracionária para binário, caso haja.
    if decimal != 0: binary += ","

    while decimal != 0:
        decimal *= 2
        binary += str(int(decimal))
        if decimal >= 1: decimal -= 1

    return binary


if __name__ == "__main__":
    option = input("Selecione uma das seguintes opções:\n1 - Decimal para Binário\n2 - Binário para Decimal\nEscolha: ")
    value = input("Digite o valor (não pode ser negativo): ").replace(",", ".")

    if option == "1":
        input(f"\nO valor binário de {value} é: {convert_decimal_to_binary(float(value))}")
    elif option == "2":
        input(f"\nO valor decimal de {value} é: {convert_binary_to_decimal(value)}")
    else:
        input("\nA opção selecionada é inválida. Por favor, tente novamente.")
