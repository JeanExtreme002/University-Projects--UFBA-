__author__ = "Jean Loui Bernard Silva de Jesus"

from .calculator import NotAWellFormedFormulaError, calculate_boolean_expression
from .core import operator_buttons, operators, paths, window_config
from .gui import ApplicationWindow
import itertools

class Application(object):
    """
    Classe principal da aplicação.
    """

    def __calculate_expression(self, expression):
        # Retorna uma lista vazia se não houver nada na expressão.
        if not expression.strip(): return list()

        # Obtém todas as variáveis da expressão e cria uma lista,
        # que será a tabela verdade, com seu cabeçalho.
        variables = self.__get_expression_variables(expression)
        if self.__window.get_user_options()["sort_variables"]: variables.sort()

        truth_table = []

        # Percorre todas as combinações de valores para as variáveis para criar a tabela verdade.
        for row in itertools.product((1, 0), repeat = len(variables)):

            # Calcula a expressão, obtendo o seu resultado e um dicionário com todas as etapas realizadas.
            try: result, steps = calculate_boolean_expression(expression, variables, row)
            except NotAWellFormedFormulaError as error: return list()

            # Cria um cabeçalho para a tabela, se ainda não existir, contendo as
            # variáveis e expressões encontradas durante o cálculo.
            if len(truth_table) == 0: truth_table.append(variables + steps["expressions"])

            # Adiciona uma linha à tabela, com os valores utilizados para as variáveis e o resultado da expressão.
            truth_table.append(list(row) + steps["results"])
        return truth_table

    def __get_expression_variables(self, expression):
        variables = []

        # Remove todos os operadores da expressão.
        for operator in self.__get_valid_operators():
            expression = expression.replace(operator, " ")

        # Separa a string pelos espaços vazios e retorna todas as variáveis da expressão.
        for var in expression.replace(" " * 2, " ").split():
            if not var in variables: variables.append(var)
        return variables

    def __get_valid_operators(self):
        # Retorna uma lista contendo todos os operadores que uma expressão pode conter, além
        # dos operadores lógicos, como os operadores de tautologia e contradição, por exemplo.
        return list(operator_buttons.values()) + list("[]()10")

    def __on_button_press(self, input_variable):
        # Remove espaços vazios nas laterais da expressão e substitui colchetes por aspas.
        expression = input_variable.get().strip().replace("[", "(").replace("]", ")")

        # Calcula a expressão e mostra sua tabela verdade.
        truth_table = self.__calculate_expression(expression)
        self.__window.set_output(truth_table)

    def __on_key_release(self, input_variable):
        # Faz o tratamento do input, removendo caracteres inválidos.
        self.__parse_input(input_variable)
        expression = input_variable.get()

    def __parse_input(self, input_variable):
        # Obtém uma lista com todos os caracteres que a expressão pode conter.
        valid_chars = self.__get_valid_operators() + [chr(char_id) for char_id in range(ord("a"), ord("z") + 1)]
        valid_chars.append(" ")

        # Faz o tratamento da string, permitindo que fique apenas os caracteres válidos.
        expression = input_variable.get().lower().lstrip().replace(" " * 2, " ").replace("~", operators.NEGATION)
        input_variable.set("".join([char for char in expression if char in valid_chars]))

    def run(self):
        # Cria a janela da aplicação, constrói os widgets e inicializa a execução.
        self.__window = ApplicationWindow(window_config["title"], paths["icon"])
        self.__window.build(operator_buttons, self.__on_key_release, self.__on_button_press)
        self.__window.mainloop()
