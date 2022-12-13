import math

def get_linear_correlation(n, sum_x, sum_y, sum_pow_x, sum_pow_y, sum_mult_xy):
    """
    Retorna o coeficiente de correlação linear.
    """
    numerator = (n * sum_mult_xy) - (sum_x * sum_y)
    
    denominator_1 = math.sqrt(n*sum_pow_x - (sum_x ** 2))
    denominator_2 = math.sqrt(n*sum_pow_y - (sum_y ** 2))

    return numerator / (denominator_1 * denominator_2)

def get_estimated_linear_function(data):
    """
    Calcula uma função linear estimada para um determinado conjunto de dados.
    """
    data = set(data)
    n = len(data)

    sum_x, sum_y, sum_pow_x, sum_pow_y, sum_mult_xy = 0, 0, 0, 0, 0

    # Calcula todos os valores preliminares necessários para o cálculo.
    for x, y in data:
        sum_x += x
        sum_y += y

        sum_pow_x += x ** 2
        sum_pow_y += y ** 2
        
        sum_mult_xy += x * y

    # Calcula o coeficiente de correlação linear.
    linear_correlation = get_linear_correlation(
        n, sum_x, sum_y,
        sum_pow_x, sum_pow_y,
        sum_mult_xy
    )

    # Calcula os parâmetros da regressão.
    b1 = (n * sum_mult_xy - (sum_x * sum_y)) / ((n * sum_pow_x) - (sum_x ** 2))
    b0 = (sum_y - b1 * sum_x) / n

    return (lambda x: b0 + b1 * x), linear_correlation, b0, b1

