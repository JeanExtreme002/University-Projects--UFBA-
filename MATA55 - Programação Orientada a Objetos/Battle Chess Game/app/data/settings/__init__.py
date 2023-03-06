from ...crypter import Crypter
from .default import default_settings
from typing import Any
import json

__all__ = ("ApplicationSettings",)

class ApplicationSettings(object):
    """
    Classe para carregar e salvar
    configurações do aplicativo.
    """

    def __init__(self, filename: str, crypter: Crypter):
        self.__filename = filename
        self.__crypter = crypter

        self.__settings = default_settings
        self.__load_settings()

    def __getattribute__(self, key: str) -> Any:
        return super().__getattribute__(key) if key.startswith("_") else self.__settings[key]

    def __setattr__(self, key: str, value: Any):
        if key.startswith("_"):
            return super().__setattr__(key, value)

        self.__settings[key] = value
        self.__save_settings()

    def __load_settings(self):
        """
        Carrega as configurações de um arquivo.
        """
        try:
            file = open(self.__filename, encoding = "UTF-8")
            
            data = self.__crypter.decrypt(file.read())
            self.__settings.update(json.loads(data))
            
            file.close()
            
        finally: return self.__save_settings()

    def __save_settings(self):
        """
        Salva as configurações em um arquivo.
        """
        with open(self.__filename, "w", encoding = "UTF-8") as file:
            string = json.dumps(self.__settings)
            file.write(self.__crypter.encrypt(string))

