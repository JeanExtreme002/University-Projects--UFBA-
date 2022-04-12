from .operation_errors import *

class ArithmeticOperationExecutor(object):
    def __init__(self, core):
        self.__core = core

    def __get_element_position(self, element):
        row, column = element[1:].split(",")
        return int(row), int(column)

    def __get_matrix_in_use(self):
        return self.__core.get_matrix_in_use()[0]
     
    def __replace_matrix_elements(self, expression, elements):
        # Obtém a matriz em uso para substituir a representação
        # dos elementos pelos seus respectivos valores.
        matrix = self.__get_matrix_in_use()
        
        for element in elements:
            row, column = self.__get_element_position(element)

            # Obtém o valor a partir da posição do elemento.
            try: value = matrix.get(row, column)
            except: raise ElementPositionError((row, column))

            # Formata o valor caso ele seja complexo.
            if isinstance(value, complex):
                value = "complex({},{})".format(value.real, value.imag)

            # Insere o valor na expressão.
            expression = expression.replace(element, str(value))
            
        return expression
    
    def execute(self, instruction: dict):
        """
        Obtém um dicionário {"expression": ..., "elements": [...]}
        e retorna o resultado do cálculo da expressão.
        """
        expression = instruction["expression"]
        elements = instruction["elements"]
        
        # Substitui os E(posição) pelos seus respectivos valores.
        expression = self.__replace_matrix_elements(expression, elements)

        # Realiza o cálculo.
        try:
            result = str(eval(expression))
            result = result.replace("(","").replace(")","").replace("j","i")
            return "Resultado: " + result
        except:
            raise ExpressionSyntaxError
