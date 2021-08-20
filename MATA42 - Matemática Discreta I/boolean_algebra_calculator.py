__author__ = "Jean Loui Bernard Silva de Jesus"

import itertools

def calculate_boolean_expression(expression):
    """
    Calcula uma expressão booleana, cujo valor lógico das sentenças
    que compõem a expressão e do resultado final deve ser 0 ou 1.

    OPERADORES LÓGICOS:
    Negação: (~ ou ¬)
    Conjunção: (^)
    Disjunção Inclusiva: (V)
    Disjunção Exclusiva: (XV)
    Condicional: (->)
    Bicondicional: (<->)
    """

    # Caso haja uma expressão dentro de parênteses, esta será calculada primeiro, através da recursividade,
    # e terá o seu resultado final inserido na expressão externa. Exemplo: "~(1 ^ 0)" se torna "~0".
    if "(" in expression:
        for start, end in find_encapsulated_expressions(expression):
            exp = expression[start: end]
            exp_value = calculate_boolean_expression(exp[1: -1])
            expression = expression[:start] + " " * (len(exp) - len(exp_value)) + exp_value + expression[end:]

    # Substitui a(s) sentença(s) e seu operador, pelo seu resultado na tabela verdade.
    expression = expression.replace(" ", "").replace("¬", "~").replace("~~", "")
    expression = expression.replace("~0", "1").replace("~1", "0")
    expression = expression.replace("1^1", "1").replace("1^0", "0").replace("0^1", "0").replace("0^0", "0")
    expression = expression.replace("1V1", "1").replace("1V0", "1").replace("0V1", "1").replace("0V0", "0")
    expression = expression.replace("1XV1", "0").replace("1XV0", "1").replace("0XV1", "1").replace("0XV0", "0")
    expression = expression.replace("1->1", "1").replace("1->0", "0").replace("0->1", "1").replace("0->0", "1")
    return expression.replace("1<->1", "1").replace("1<->0", "0").replace("0<->1", "0").replace("0<->0", "1")

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
            end = find_closing_parenthesis(index + 1, expression)
            yield index, end + 1
            index = end
        index += 1

def get_expression_sentences(expression):
    """
    Retorna todas as sentenças que compõem a expressão. As sentenças podem
    ser letras ou palavras, desde que sejam obrigatoriamente minúsculas e
    formadas apenas por letras sem acentos (a-z).
    """
    sentences = []

    # Remove todos os operadores lógicos. Isso é feito para que seja possível
    # separar as sentenças pelos espaços em branco. Do contrário, haveria
    # problemas para identificar as sentenças que não estão separadas dos
    # operadores lógicos ou parênteses, como "~(p^q)", por exemplo.
    for operator in get_logical_operators():
        expression = expression.replace(operator, " ")

    # Separa a expressão pelos espaços em branco e procura pelas sentenças, verificando
    # se a substring está dentro do range [ord("a") = 97, ord("z") = 122].
    for substring in expression.split():
        if not substring in sentences and all([97 <= ord(char) <= 122 for char in substring]):
            sentences.append(substring)
    return sentences

def get_logical_operators():
    """
    Retorna uma lista com todos os símbolos de operadores lógicos que podem ser utilizados.
    """
    return ["(", ")", "~", "¬", "^", "XV", "V", "<->", "->"]

if __name__ == "__main__":
    # Abre o arquivo de informações do programa e imprime o texto.
    with open("boolean_algebra_calculator_info.txt", encoding = "utf-8") as info_file:
        print(info_file.read())

    # Obtém a expressão a ser calculada e substitui chaves e colchetes por parênteses.
    expression = input("Expressão: ")
    expression = expression.replace("{", "(").replace("}", ")").replace("[", "(").replace("]", ")")

    # Obtém as sentenças da expressão e todas as suas combinações na tabela verdade.
    sentences = get_expression_sentences(expression)
    truth_table = list(itertools.product((1, 0), repeat = len(sentences)))

    # Imprime o header da tabela.
    print("\nTABELA VERDADE:\n")
    print(*sentences, expression, sep = " | ")
    print("-" * (len(sentences) * 4 + len(expression) + 5))

    # Percorre cada linha da tabela verdade.
    for row in range(len(truth_table)):
        new_expression = expression

        # Percorre as colunas da tabela, trocando as sentenças na expressão pelos valores booleanos.
        for column in range(len(sentences)):
            new_expression = new_expression.replace(sentences[column], str(truth_table[row][column]))

        # Calcula e imprime o resultado, junto com os parâmetros usados.
        print(*truth_table[row], calculate_boolean_expression(new_expression), sep = " | ")
    input()
