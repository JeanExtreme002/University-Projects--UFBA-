from .achievements import UserAchievements
from .file_crypter import FileCrypter
from .paths import Paths
from .settings import ApplicationSettings

__all__ = ("paths", "settings")

paths = Paths()

file_crypter = FileCrypter()

achievements_filename = paths.achievements_filename
settings_filename = paths.settings_filename

achievements = UserAchievements(achievements_filename, file_crypter)
settings = ApplicationSettings(settings_filename, file_crypter)

