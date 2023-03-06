from typing import Any
import random
import os

__all__ = ("Paths",)

class Paths(object):
    """
    Classe responsável por gerenciar
    diretórios e nomes de arquivos.
    """
    sound_path = "sounds"
    image_path = "images"

    data_path = "data"
    
    replay_path = os.path.join(data_path, "replay")
    replay_images_path = os.path.join(replay_path, "images")
    
    screenshot_path = os.path.join(data_path, "screenshots")

    achievements_filename = os.path.join(data_path, "0001.userdata")
    settings_filename = os.path.join(data_path, "0002.userdata")

    __image_extensions = [".png", ".jpg", ".jpeg"]
    __sound_extensions = [".mp3", ".wav"]

    def __init__(self):
        for key, value in self.__class__.__dict__.items():
            if key.endswith("path"): self.__initialize_directory(value)

    def __setattr__(self, key: str, value: Any):
        raise AttributeError("'{}' object has no attribute '{}'".format(
            self.__class__.__name__, key
        ))

    def __get_file(self, base: str, *path: str) -> str:
        """
        Retorna o nome do arquivo com os separadores corretos.
        """
        return os.path.join(base, *path)

    def __get_file_list(self, base: str, extensions: list[str], *folders: str) -> list[str]:
        """
        Retorna lista de todos os arquivos presentes em
        um diretório, filtrando os arquivos pela sua extensão.
        """
        path = os.path.join(base, *folders)
        filenames = []
        
        for filename in os.listdir(path):
            if "." + filename.split(".")[-1] in extensions:
                filenames.append(os.path.join(path, filename))
        return filenames

    def __initialize_directory(self, path: str):
        """
        Cria um diretório se ele não existir.
        """
        if not os.path.exists(path): os.mkdir(path)
    
    def get_image(self, *path: str) -> str:
        """
        Retorna o nome do arquivo de imagem com o diretório base e os separadores corretos.
        """
        return self.__get_file(self.image_path, *path)

    def get_image_list(self, *folders: str, shuffle: bool = False) -> list[str]:
        """
        Retorna lista de todos os arquivos de imagem
        presentes em um dado diretório.
        """
        images = self.__get_file_list(self.image_path, self.__image_extensions, *folders)

        if shuffle: random.shuffle(images)
        return images

    def get_random_image(self, *folders: str) -> str:
        """
        Retorna um arquivo de imagem aleatório, de um dado diretório.
        """
        filenames = self.get_image_list(*folders)
        return random.choice(filenames)

    def get_random_screenshot(self) -> str:
        """
        Retorna uma screenshot aleatória.
        """
        filenames = self.get_screenshot_list()
        return random.choice(filenames)

    def get_random_sound(self, *folders: str) -> str:
        """
        Retorna um arquivo de som aleatório, de um dado diretório.
        """
        filenames = self.get_sound_list(*folders)
        return random.choice(filenames)

    def get_replay_image(self, filename: str) -> str:
        """
        Retorna o nome do arquivo de imagem de replay com o diretório base e os separadores corretos.
        """
        return self.__get_file(self.replay_images_path, filename)

    def get_screenshot(self, filename: str) -> str:
        """
        Retorna o nome do arquivo de screenshot com o diretório base e os separadores corretos.
        """
        return self.__get_file(self.screenshot_path, filename)

    def get_screenshot_list(self, shuffle: bool = False) -> list[str]:
        """
        Retorna lista de todas as screenshots.
        """
        images = self.__get_file_list(self.screenshot_path, self.__image_extensions)
            
        if shuffle: random.shuffle(images)
        return images

    def get_sound(self, *path: str) -> str:
        """
        Retorna o nome do arquivo de som com o diretório base e os separadores corretos.
        """
        return self.__get_file(self.sound_path, *path)

    def get_sound_list(self, *folders: str, shuffle: bool = False) -> list[str]:
        """
        Retorna lista de todos os arquivos de som
        presentes em um dado diretório.
        """
        sounds = self.__get_file_list(self.sound_path, self.__sound_extensions, *folders)
            
        if shuffle: random.shuffle(sounds)
        return sounds
