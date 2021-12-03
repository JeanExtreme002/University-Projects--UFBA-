REFLEXIVA = "Reflexiva"
IRREFLEXIVA = "Irreflexiva"
SIMETRICA = "Simétrica"
ANTI_SIMETRICA = "Anti-simétrica"
ASSIMETRICA = "Assimétrica"
TRANSITIVA = "Transitiva"
CONGRUENCIA = "Congruência"

def prop_reflexiva(relacao):
    for x in set(x for x, y in relacao):
        if relacao.count((x, x)) == 0:
            return False, [False, (x, x)]
    return [True, None]

def prop_irreflexiva(relacao):
    for x in set(x for x, y in relacao):
        if relacao.count((x, x)) == 1:
            return False, [True, (x, x)]
    return [True, None]

def prop_simetrica(relacao):
    for x, y in relacao:
        if (y, x) not in relacao:
            return False, [False, (y, x)]
    return [True, None]

def prop_anti_simetrica(relacao):
    for x, y in relacao:
        if (y, x) in relacao:
            if x != y:
                return False,[True, (y, x)]
    return [True, None]

def prop_assimetrica(relacao):
    for x, y in relacao:
        if (y, x) in relacao:
            return False, [True, (y, x)]
    return [True, None]

def prop_transitiva(relacao):
    for x, y in relacao:
        for par in relacao:
            if par[0] == y and not (x, par[1]) in relacao:
                return False, [False, (x, par[1])]
    return [True, None]

def prop_congruencia(relacao, modulo):
    for x, y in relacao:
        if (x - y) % modulo != 0:
            return False, [True, (x, y)]
    return [True, None]

def obter_propriedades(relacao, modulo = None):
    propriedades = {
        REFLEXIVA: prop_reflexiva(relacao),
        IRREFLEXIVA: prop_irreflexiva(relacao),
        SIMETRICA: prop_simetrica(relacao),
        ANTI_SIMETRICA: prop_anti_simetrica(relacao),
        ASSIMETRICA: prop_assimetrica(relacao),
        TRANSITIVA: prop_transitiva(relacao)
    }

    if modulo:
        propriedades[CONGRUENCIA] = prop_congruencia(relacao, modulo)
    return propriedades
