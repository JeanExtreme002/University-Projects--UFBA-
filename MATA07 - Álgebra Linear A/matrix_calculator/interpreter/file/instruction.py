from .errors import *
import os

def load_instructions(filename, encoding = None):
    """
    Função geradora para retornar instruções de um arquivo.
    """
    if not filename: raise NoFilenameError
    if not os.path.exists(filename): raise UserFileNotFoundError(filename)
    
    with open(filename, encoding = encoding) as file:
        for instruction in file:
            yield instruction.replace("\n", "").strip()
