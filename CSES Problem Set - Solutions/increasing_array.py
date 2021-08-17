# Author: Jean Loui Bernard Silva de Jesus

length = int(input())
array = [int(i) for i in input().split()]
moves = 0

for i in range(1, length):
    n1, n2 = array[i - 1], array[i]

    # Se o número X for menor que o seu anterior, a quantidade de movimentos será
    # a diferença entre o seu anterior e o valor X. Vamos supor que o array seja
    # [10, 7], por exemplo. Como 7 é menor que 10, precisamos dar um jeito de 7
    # ser maior ou IGUAL a 10, para organizar o array em ordem crescente. Logo,
    # fazemos 10 - 7 = 3. Sendo assim, o valor X que antes era 7 se torna 10,
    # e a quantidade de movimentos para tal foi 3.

    if n1 > n2:
        array[i] = n1
        moves += n1 - n2

print(moves)
