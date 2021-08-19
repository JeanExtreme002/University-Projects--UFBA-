__author__ = "Jean Loui Bernard Silva de Jesus"

def find_closing_parenthesis(index, string):
    """
    Recebe a posição do parêntese de abertura e retorna
    a posição do seu respectivo parêntese de fechamento.
    """
    count = 1

    for next_index in range(index + 1, len(string)):
        if string[index] == "(": count += 1
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
            end = find_closing_parenthesis(index + 1, expression)
            yield index, end + 1
            index = end
        index += 1

def calculate_boolean_expression(expression):
    """
    Calcula uma expressão booleana, cujo valor lógico das sentenças
    que compõem a expressão e do resultado final deve ser 0 ou 1.

    CONECTIVOS LÓGICOS:
    Negação: (~ ou ¬)
    Conjunção: (^)
    Disjunção Inclusiva: (v)
    Disjunção Exclusiva: (xv)
    Condicional: (->)
    Bicondicional: (<->)
    """
    if "(" in expression:
        for start, end in find_encapsulated_expressions(expression):
            exp = expression[start: end]
            exp_value = calculate_boolean_expression(exp[1: -1])
            expression = expression[:start] + " " * (len(exp) - len(exp_value)) + exp_value + expression[end:]

    expression = expression.replace(" ", "").replace("¬", "~").replace("~~", "")
    expression = expression.replace("~0", "1").replace("~1", "0")
    expression = expression.replace("1^1", "1").replace("1^0", "0").replace("0^1", "0").replace("0^0", "0")
    expression = expression.replace("1v1", "1").replace("1v0", "1").replace("0v1", "1").replace("0v0", "0")
    expression = expression.replace("1xv1", "0").replace("1xv0", "1").replace("0xv1", "1").replace("0xv0", "0")
    expression = expression.replace("1->1", "1").replace("1->0", "0").replace("0->1", "1").replace("0->0", "1")
    return expression.replace("1<->1", "1").replace("1<->0", "0").replace("0<->1", "0").replace("0<->0", "1")

expression = "(p->q)^(q->p)"

for i in range(1, -1, -1):
    for x in range(1, -1, -1):
        exp = expression.replace("p", str(i)).replace("q", str(x))
        print(x, i, calculate_boolean_expression(exp), exp)


# PROJETO EM ANDAMENTO...
