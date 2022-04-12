from .errors import *
import os

def load_instructions(filename):
    """
    Função geradora para retornar instruções de um arquivo.
    """
    if not os.path.exists(filename): raise UserFileNotFoundError(filename)
    
    with open(filename) as file:
        for instruction in file:
            yield instruction.replace("\n", "").strip()
