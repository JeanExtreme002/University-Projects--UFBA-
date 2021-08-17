# Author: Jean Loui Bernard Silva de Jesus

value = int(input())
values = [int(i) for i in input().split()]

total = int((1 + value) * value / 2) # Calcula a PA.

# O que sobrar será o valor que falta.
for n in values:
    total -= n

print(total)
