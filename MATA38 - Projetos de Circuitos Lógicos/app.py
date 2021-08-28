__author__ = "Jean Loui Bernard Silva de Jesus"

from binary import BinaryValue

print("Selecione uma das conversões listadas abaixo:")
print("1 - Converter Decimal para Binário")
print("2 - Converter Binário para Decimal")
print("3 - Converter Binário para Sinal-Magnitude")
print("4 - Converter Binário para Complemento de 1")
print("5 - Converter Binário para Complemento de 2")
print("6 - Converter Binário para IEEE-754 (32 bits)")
print("7 - Converter Binário para IEEE-754 (64 bits)")

while True:
    option = input("\nSua escolha: ")
    if option in "1234567": break
    print("Por favor, digite uma opção válida.")

while True:
    value = input("Digite o valor: ").replace(",", ".")
    try:
        binary_value = BinaryValue(float(value) if option == "1" else value)
        break
    except: print("Por favor, digite um valor válido.")

if option == "1": input(f"\nO valor binário de '{value}' é: {binary_value.get_binary()}")
elif option == "2": input(f"\nO valor decimal de '{value}' é: {binary_value.to_decimal()}")
elif option == "3": input(f"\nO binário '{value}' em S-M é: {binary_value.to_sign_magnitude()}")
elif option == "4": input(f"\nO binário '{value}' em C1 é: {binary_value.to_one_s_complement()}")
elif option == "5": input(f"\nO binário '{value}' em C2 é: {binary_value.to_two_s_complement()}")
elif option == "6": input(f"\nO binário '{value}' em IEEE-754 (32 bits) é: {binary_value.to_ieee_754()}")
elif option == "7": input(f"\nO binário '{value}' em IEEE-754 (64 bits) é: {binary_value.to_ieee_754_x64()}")
