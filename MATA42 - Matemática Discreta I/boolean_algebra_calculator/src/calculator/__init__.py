__author__ = "Jean Loui Bernard Silva de Jesus"

from .operators import NEGATION, CONJUNCTION, INCLUSIVE_DISJUNCTION, EXCLUSIVE_DISJUNCTION, CONDITIONAL, BICONDITIONAL
from .util import find_encapsulated_expressions

def calculate_boolean_expression(expression):
    """
    Calcula uma expressão booleana, cujo valor lógico das sentenças
    que compõem a expressão e do resultado final deve ser 0 ou 1.
    """

    # Caso haja uma expressão dentro de parênteses, ela será calculada primeiro, através da recursividade,
    # e terá o seu resultado inserido na expressão externa. Exemplo: "~(1 ^ 0)" se torna "~0".
    if "(" in expression:
        for start, end in find_encapsulated_expressions(expression):
            exp = expression[start: end]
            exp_value = calculate_boolean_expression(exp[1: -1])
            expression = expression[:start] + " " * (len(exp) - len(exp_value)) + exp_value + expression[end:]

    # Realiza o cálculo da expressão, substituindo cada "sub-expressão", que contém
    # no máximo dois valores lógicos e um operador, pelo seu resultado.
    expression = expression.replace(" ", "").replace(NEGATION * 2, "")
    expression = expression.replace(NEGATION + "0", "1").replace(NEGATION + "1", "0")

    expression = expression.replace("1" + CONJUNCTION + "1", "1").replace("1" + CONJUNCTION + "0", "0")
    expression = expression.replace("0" + CONJUNCTION + "1", "0").replace("0" + CONJUNCTION + "0", "0")

    expression = expression.replace("1" + INCLUSIVE_DISJUNCTION + "1", "1").replace("1" + INCLUSIVE_DISJUNCTION + "0", "1")
    expression = expression.replace("0" + INCLUSIVE_DISJUNCTION + "1", "1").replace("0" + INCLUSIVE_DISJUNCTION + "0", "0")

    expression = expression.replace("1" + EXCLUSIVE_DISJUNCTION + "1", "0").replace("1" + EXCLUSIVE_DISJUNCTION + "0", "1")
    expression = expression.replace("0" + EXCLUSIVE_DISJUNCTION + "1", "1").replace("0" + EXCLUSIVE_DISJUNCTION + "0", "0")

    expression = expression.replace("1" + CONDITIONAL + "1", "1").replace("1" + CONDITIONAL + "0", "0")
    expression = expression.replace("0" + CONDITIONAL + "1", "1").replace("0" + CONDITIONAL + "0", "1")

    expression = expression.replace("1" + BICONDITIONAL + "1", "1").replace("1" + BICONDITIONAL + "0", "0")
    expression = expression.replace("0" + BICONDITIONAL + "1", "0").replace("0" + BICONDITIONAL + "0", "1")
    return expression
