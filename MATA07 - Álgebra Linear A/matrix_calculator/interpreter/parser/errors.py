class NoImaginaryPartError(Exception):
    def __init__(self):
        self.__value = str(value)
        
    def __str__(self):
        return "O valor \"{}\" não possui parte imaginária.".format(self.__value)

class UnrecognizedSyntaxError(Exception):
    def __str__(self):
        return "Não foi possível reconhecer essa instrução."
