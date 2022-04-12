from .numeric import parse_complex_value
from .patterns import *
from .errors import *
import re

def parse_instruction(instruction):
    # Verifica se o comando refere-se à um comando da aplicação. 
    result = re.findall(application_operation_pattern, instruction)
    if result: return {"operation": "application", "command": result[0][0], "args": result[0][1].strip()}

    # Verifica se o comando refere-se à uma operação de matriz.
    result = re.findall(matrix_operation_pattern, instruction.replace(" ", ""))
    if result: return {"operation": "matrix", "var": result[0][0], "x": result[0][1], "operator": result[0][2], "y": result[0][3]}

    # Verifica se o comando refere-se à uma operação elementar.
    result = re.findall(elementary_operation_pattern, instruction.replace(" ", ""))
    if result: return {"operation": "elementary", "row1": result[0][0], "operator": result[0][1], "scalar": result[0][2], "row2": result[0][3]}

    # Verifica se o comando refere-se à uma operação de aritmética com elementos.
    result = re.findall(matrix_element_pattern, instruction)
    
    if result and all([char in " E,.0123456789+-/%*()i" for char in instruction]):
        
        # Converte os valores complexos, se houverem.
        for complex_string in re.findall(complex_pattern, instruction):
            complex_value = parse_complex_value(complex_string)
            instruction = instruction.replace(complex_string, "complex({}, {})".format(complex_value.real, complex_value.imag))
        return {"operation": "arithmetic", "expression": instruction, "elements": result}
    
    raise UnrecognizedSyntaxError
