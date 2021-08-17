# Author: Jean Loui Bernard Silva de Jesus

value = int(input())

while value != 1:
    print(value, end = " ")
    value = int(value / 2) if value % 2 == 0 else value * 3 + 1
print(1)
