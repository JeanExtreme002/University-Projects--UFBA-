__author__ = "Jean Loui Bernard Silva de Jesus"

from .operators import NEGATION, CONJUNCTION, INCLUSIVE_DISJUNCTION, EXCLUSIVE_DISJUNCTION, CONDITIONAL, BICONDITIONAL
from .util import find_encapsulated_expressions, insert_bool_values

class NotAWellFormedFormulaError(Exception):
    def __init__(self, expression):
        self.__expression = expression

    def __str__(self):
        return "The formula '{}' is not a well-formed formula".format(self.__expression)

def calculate_boolean_expression(expression, variables, values):
    """
    Calcula uma expressão booleana, retornando o seu resultado e um dicionário,
    contendo todas as subexpressões encontradas e os seus respectivos resultados.
    """

    steps = {"expressions": list(), "results": list()}
    original_expression = expression

    # Caso haja uma expressão dentro de parênteses, ela será calculada primeiro, através da recursividade,
    # e terá o seu resultado inserido na expressão externa. Exemplo: sendo a=1 e b=0, "~(a ^ b)" se torna "~0".
    if "(" in original_expression:
        for start, end in find_encapsulated_expressions(original_expression):

            # Se o índice do parêntese de fechamento for zero, significa que
            # o mesmo não existe. Logo, a expressão não é bem formada.
            if end == 0: raise NotAWellFormedFormulaError(original_expression)

            # Obtém a subexpressão, sem os parênteses, e a calcula.
            sub_expression = original_expression[start: end]
            result, calc_steps = calculate_boolean_expression(sub_expression[1: -1], variables, values)

            # Adiciona as subexpressões encontradas e seus resultados à lista.
            steps["expressions"] += calc_steps["expressions"]
            steps["results"] += calc_steps["results"]

            # Substitui a subexpressão na expressão pelo seu resultado.
            expression = expression[:start] + " " * (len(sub_expression) - len(result)) + result + expression[end:]

    # Realiza o cálculo da expressão, substituindo cada subexpressão, que contém
    # no máximo dois valores lógicos e um operador, pelo seu resultado.
    result = insert_bool_values(expression, variables, values).replace(" ", "").replace(NEGATION * 2, "")
    result = result.replace(NEGATION + "0", "1").replace(NEGATION + "1", "0")

    result = result.replace("1" + CONJUNCTION + "1", "1").replace("1" + CONJUNCTION + "0", "0")
    result = result.replace("0" + CONJUNCTION + "1", "0").replace("0" + CONJUNCTION + "0", "0")

    result = result.replace("1" + INCLUSIVE_DISJUNCTION + "1", "1").replace("1" + INCLUSIVE_DISJUNCTION + "0", "1")
    result = result.replace("0" + INCLUSIVE_DISJUNCTION + "1", "1").replace("0" + INCLUSIVE_DISJUNCTION + "0", "0")

    result = result.replace("1" + EXCLUSIVE_DISJUNCTION + "1", "0").replace("1" + EXCLUSIVE_DISJUNCTION + "0", "1")
    result = result.replace("0" + EXCLUSIVE_DISJUNCTION + "1", "1").replace("0" + EXCLUSIVE_DISJUNCTION + "0", "0")

    result = result.replace("1" + CONDITIONAL + "1", "1").replace("1" + CONDITIONAL + "0", "0")
    result = result.replace("0" + CONDITIONAL + "1", "1").replace("0" + CONDITIONAL + "0", "1")

    result = result.replace("1" + BICONDITIONAL + "1", "1").replace("1" + BICONDITIONAL + "0", "0")
    result = result.replace("0" + BICONDITIONAL + "1", "0").replace("0" + BICONDITIONAL + "0", "1")

    # Se o resultado não for um valor lógico (0 ou 1), significa que a fórmula não é bem formada.
    if not result in "01": raise NotAWellFormedFormulaError(original_expression)

    # Adiciona à lista a expressão atual e o seu resultado.
    steps["expressions"].append(original_expression)
    steps["results"].append(result)
    return result, steps
