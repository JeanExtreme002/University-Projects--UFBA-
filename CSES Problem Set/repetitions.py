# Author: Jean Loui Bernard Silva de Jesus

string = input()
max_length = 0
current_char, current_length = string[0], 0

for char in string:

    # Se o caractere for o mesmo do anterior, o comprimento
    # da substring atual é aumentado em 1.
    current_length += 1 if char == current_char else 0

    if max_length < current_length:
        max_length = current_length

    # Se o caractere for diferente do anterior, o comprimento
    # da substring atual é resetado para 1.
    if char != current_char:
        current_char = char
        current_length = 1

print(max_length)
