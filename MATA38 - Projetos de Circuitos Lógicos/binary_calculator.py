__author__ = "Jean Loui Bernard Silva de Jesus"

def add_binary(binary1: str, binary2: str) -> str:

    # Iguala a quantidade de bits dos valores binários.
    size = max([len(binary1), len(binary2)])
    if len(binary1) < size: binary1 = "0" * (size - len(binary1)) + binary1
    if len(binary2) < size: binary2 = "0" * (size - len(binary2)) + binary2

    # Como a soma é realizada da esquerda para direita, os valores são invertidos para
    # que se possa somar da direita para esquerda. Dessa forma, é possível adicionar
    # cada bit à string sem problemas.
    binary1, binary2 = binary1[::-1], binary2[::-1]
    final_result, carry = "", 0

    for index in range(size):
        # Soma os bits e o carry da última operação.
        result = int(binary1[index]) + int(binary2[index]) + carry
        carry = 0

        # O decimal 2 é igual ao binário "10" (carry = 1, bit = 0)
        if result == 2: carry, result = 1, 0

        # O decimal 3 é igual ao binário "11" (carry = 1, bit = 1)
        if result == 3: carry, result = 1, 1

        # Adiciona o bit do resultado ao valor final.
        final_result += str(result)

    # Adiciona o último carry ao binário invertido.
    return ("" if not carry else "1") + final_result[::-1]

if __name__ == "__main__":
    print("SOMA DE BINÁRIOS (INTEIROS):")
    value1 = input("Primeiro valor: ")
    value2 = input("Segundo valor: ")
    input(f"O resultado de {value1} + {value2} é {add_binary(value1, value2)}.")
