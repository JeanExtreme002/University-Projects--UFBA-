def obter_classe_de_equivalencia(relacao, y):
    conjunto = []
    
    for par in relacao:
        if y == par[1]: 
            conjunto.append(par[0])
    return conjunto
