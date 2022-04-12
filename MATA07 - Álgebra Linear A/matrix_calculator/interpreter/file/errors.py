class UserFileDecodingError(Exception):
    def __str__(self):
        return "Não foi possível descriptografar o arquivo."
        

class UserFileNotFoundError(Exception):
    def __init__(self, filename = None):
        self.__filename = filename

    def __str__(self):
        filename = " \"{}\"".format(self.__filename) if self.__filename else ""
        return "Não foi possível encontrar o arquivo{}.".format(filename)
