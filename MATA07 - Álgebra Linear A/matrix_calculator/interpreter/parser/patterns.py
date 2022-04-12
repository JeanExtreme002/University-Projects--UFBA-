# Patterns de valores numéricos.
integer_pattern = "-?[0-9]+"
float_pattern = "-?[0-9]+\.[0-9]+"
complex_pattern = "\((?:{0}|{1})?[\+-]?(?:{2}|{3})?i\)".format(float_pattern, integer_pattern, float_pattern[2:], integer_pattern[2:])
numeric_pattern = "{0}|{1}|{2}".format(complex_pattern, float_pattern, integer_pattern)

# Patterns de elementos de uma expressão.
elementary_operators_pattern = "\+=|\-=|\*=|/=|<>|=="
matrix_element_pattern = "E[0-9]+,[0-9]+"
matrix_minor_pattern = "m\([0-9]+,[0-9]\)"
matrix_operators_pattern = "\+|-|\*\*|\*|/|tc|ct|c|t|adj|cof|inv|{0}".format(matrix_minor_pattern)

# Patterns de instruções do usuário.
application_operation_pattern = "^([a-z]+)(\s.+|)"
elementary_operation_pattern = "^L([0-9])({0})({1}|)L?([0-9]+|)$".format(elementary_operators_pattern, numeric_pattern)
matrix_operation_pattern = "^([A-Z]+)=([A-Z]+|{1})({0})([A-Z]+|{1}|)$".format(matrix_operators_pattern, numeric_pattern)
