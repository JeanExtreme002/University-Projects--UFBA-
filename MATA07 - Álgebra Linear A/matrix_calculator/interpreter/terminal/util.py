import os, sys

def clear_terminal():
    """
    Limpa a tela do terminal.
    """
    if "win" in sys.platform: os.system("cls")
    else: os.system("clear")  

def print_matrix_in_use(name, matrix, n_matrices, show_matrix_string):
    """
    Imprime a matrix que está sendo usada.
    """
    if matrix:
        print("Atualmente usando a matriz \"{}\". [{} {}]".format(
            name, n_matrices, "disponíveis" if n_matrices > 1 else "disponível"
        ))

        # Mostra a matriz, caso o usuário queira.
        if show_matrix_string: print("\n" + str(matrix))
            
    else:
        print("Atualmente nenhuma matriz está sendo usada. [{} {}]".format(
            n_matrices, "disponíveis" if n_matrices > 1 else "disponível"
        ))
    print("\n")
