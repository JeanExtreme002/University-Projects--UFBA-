__all__ = ("commands", "help_string")

commands = [
    ("clear", "Apaga o histórico de instruções"),
    ("delete <matrix>", "Deleta uma matriz"),
    ("execute <arquivo.ext> [--encoding]", "Carrega um arquivo de instruções e as executa"),
    ("exit", "Encerra o programa"),
    ("help", "Mostra uma lista com todos os comandos do terminal"),
    ("list", "Mostra uma lista com todas as matrizes"),
    ("load <arquivo.ext> [--encoding]", "Carrega um arquivo contendo matrizes"),
    ("log <true | false>", "Mostra os comandos anteriores"),
    ("prop <matrix>", "Mostra uma lista com todas as propriedades da matriz"),
    ("save <arquivo.ext> [--encoding]", "Salva as matrizes em um arquivo"),
    ("show <true | false>", "Mostra a matriz que está sendo utilizada"),
    ("use <matrix>", "Define uma matriz para ser utilizada")
]
commands.sort()

title = "Lista de Comandos do Terminal:\n"
template = "- {:<" + str(max([len(command) for command, description in commands])) + "} | {}"

help_string = title + "\n".join([template.format(command, description) for command, description in commands])
