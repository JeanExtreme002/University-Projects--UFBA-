__author__ = "Jean Loui Bernard Silva de Jesus"

from .calculator import operators
from os.path import join

operator_buttons = {
    "2: Negação ({})".format(operators.NEGATION): operators.NEGATION,
    "3: Conjunção ({})".format(operators.CONJUNCTION): operators.CONJUNCTION,
    "4: Disjunção In. ({})".format(operators.INCLUSIVE_DISJUNCTION): operators.INCLUSIVE_DISJUNCTION,
    "5: Disjunção Ex. ({})".format(operators.EXCLUSIVE_DISJUNCTION): operators.EXCLUSIVE_DISJUNCTION,
    "6: Condicional ({})".format(operators.CONDITIONAL): operators.CONDITIONAL,
    "7: Bicondicional ({})".format(operators.BICONDITIONAL): operators.BICONDITIONAL
}

window_config = {
    "title": "Boolean Algebra Calculator"
}

paths = {
    "icon": join("images", "icon.ico")
}
