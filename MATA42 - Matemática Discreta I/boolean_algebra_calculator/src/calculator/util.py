__author__ = "Jean Loui Bernard Silva de Jesus"

def find_closing_parenthesis(index, string):
    """
    Recebe a posição do parêntese de abertura e retorna
    a posição do seu respectivo parêntese de fechamento.
    """
    count = 1

    for next_index in range(index + 1, len(string)):
        if string[next_index] == "(": count += 1
        elif string[next_index] == ")": count -= 1
        if count == 0: return next_index
    return -1

def find_encapsulated_expressions(expression):
    """
    Função geradora que retorna a posição (start, end) de todas as
    expressões dentro de parênteses (incluindo seus parênteses).
    """
    index = 0

    while index < len(expression):
        if expression[index] == "(":
            end = find_closing_parenthesis(index, expression)
            yield index, end + 1
            index = end
        index += 1

def insert_bool_values(expression, variables, values):
    """
    Substitui as variáveis da expressão pelos valores booleanos.
    """
    for index in range(len(values)):
        expression = expression.replace(variables[index], str(values[index]))
    return expression
