from app import Application, paths
from core import ChessGame
from locale import getlocale

import sys
import traceback

__project__ = "https://github.com/JeanExtreme002/Chess-Battle"
__version__ = "2.0.0"

def generate_info_file(filename: str):
    """
    Função para gerar arquivo com as informações do jogo.
    """
    with open(filename, "w") as file:
        file.write("Project URL: {}\n".format(__project__))
        file.write("VERSION: {}\n".format(__version__))

def main():
    """
    Função principal para executar o jogo.
    """
    chess_game = ChessGame(paths.replay_path)

    title = "Xadrez de Batalha" if "pt" in getlocale()[0] else "Battle Chess"
    winter_theme = len(sys.argv) > 1 and sys.argv[1].lower() == "winter_theme"

    application = Application(title, chess_game, winter_theme = winter_theme)
    application.run()

def save_errors_to_file(filename: str):
    """
    Salva o erro gerado em um arquivo.
    """
    with open(filename, "a+") as file:
        traceback.print_exc(file = file)
        file.write("\n" + "=" * 100 + "\n")

# Executa o código principal e, caso haja erro,
# o mesmo será salvo em um arquivo.
try:
    generate_info_file("info.txt")
    main()
except Exception:
    input("It looks like the game has crashed due to an error. Check it in the log file.")
    save_errors_to_file(filename = "log.txt")

