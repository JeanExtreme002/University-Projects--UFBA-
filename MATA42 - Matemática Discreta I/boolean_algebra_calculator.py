__author__ = "Jean Loui Bernard Silva de Jesus"

def find_encapsulated_expressions(expression):
    expressions = []
    index = 0
    
    while index < len(expression):
        char = expression[index]
        
        if char == "(":
            parentheses_count = 1
            for next_index in range(index + 1, len(expression)):
                if expression[next_index] == "(": parentheses_count += 1
                if expression[next_index] == ")": parentheses_count -= 1
                if parentheses_count == 0: break
            expressions.append([index, next_index + 1])
            index = next_index
        index += 1
    return expressions

def get_logic_value(expression):
    if "(" in expression:
        for start, end in find_encapsulated_expressions(expression):
            exp = expression[start: end]
            exp_value = get_logic_value(exp[1: -1])
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
        print(x, i, get_logic_value(exp), exp)


# PROJETO EM ANDAMENTO...

