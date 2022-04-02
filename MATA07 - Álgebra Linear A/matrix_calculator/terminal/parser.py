import re

# Patterns para comandos de usuário.
application_operation_pattern = "^([a-z]+)(\s.+|)"
element_operation_pattern = "E[0-9]+,[0-9]+"
elementary_operation_pattern = "^L([0-9])(\+=|\-=|\*=|/=|<>|==)(-?[0-9]+\.[0-9]+|-?[0-9]+|)L?([0-9]+|)$"
matrix_operation_pattern = "^([A-Z]+)=([A-Z]+|-?[0-9]+\.[0-9]+|-?[0-9]+)(\+|-|\*|/|tc|ct|c|t)([A-Z]+|-?[0-9]+\.[0-9]+|-?[0-9]+|)$"

def parse_command(command):
    # Verifica se o comando refere-se à um comando da aplicação. 
    result = re.findall(application_operation_pattern, command)
    if result: return {"operation": "application", "command": result[0][0], "args": result[0][1].strip()}

    # Verifica se o comando refere-se à uma operação de matriz.
    result = re.findall(matrix_operation_pattern, command.replace(" ", ""))
    if result: return {"operation": "matrix", "var": result[0][0], "x": result[0][1], "operator": result[0][2], "y": result[0][3]}

    # Verifica se o comando refere-se à uma operação elementar.
    result = re.findall(elementary_operation_pattern, command.replace(" ", ""))
    if result: return {"operation": "elementary", "row1": result[0][0], "operator": result[0][1], "scalar": result[0][2], "row2": result[0][3]}

    # Verifica se o comando refere-se à uma operação de aritmética com elementos.
    result = re.findall(element_operation_pattern, command)
    if result and all([char in " E,.0123456789+-/%*()" for char in command]): return {"operation": "arithmetic", "expression": command, "elements": result}

    raise SyntaxError("A sintaxe da instrução está incorreta!")

def parse_complex_value(string):
    if string.lower()[-1] != "i":
        raise ValueError("Must have imaginary part. Got '{}'".format(string))
    
    string = string.replace(" ", "")[:-1]
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
