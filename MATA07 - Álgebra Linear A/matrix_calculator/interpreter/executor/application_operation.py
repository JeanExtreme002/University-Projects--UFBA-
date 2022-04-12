from .docs import command_list_string
from .operation_errors import *

class ApplicationOperationExecutor(object):
    def __init__(self, core):
        self.__core = core

    def __get_matrix_list_string(self, matrices):
        # Verifica se há matrizes. Se não, retorna uma mensagem diferente.
        if not matrices:
            return "Nenhuma matriz disponível. Use o comando \"load <arquivo.ext>\"."

        string = "Lista de Matrizes:"
            
        for name, matrix in matrices.items():
            string += "\n- {} <{},{}>".format(name, *matrix.get_order())
        return string

    def __get_matrix_properties_string(self, matrix):
        string = "Propriedades da Matrix:"
        string += "\n- Anti-hermitiana: " + str(matrix.is_skew_hermitian())
        string += "\n- Anti-simétrica: " + str(matrix.is_skew_symmetric())
        string += "\n- Coluna: " + str(matrix.is_column())
        string += "\n- Complexa: " + str(matrix.is_complex())
        string += "\n- Determinante: " + (str(matrix.get_determinant()).replace("(","").replace(")","").replace("j","i") if matrix.is_square() else "N/D")
        string += "\n- Diagonal: " + str(matrix.is_diagonal())
        string += "\n- Escalar: " + str(matrix.is_scalar())
        string += "\n- Identidade: " + str(matrix.is_identity())
        string += "\n- Hermitiana: " + str(matrix.is_hermitian())
        string += "\n- Linha: " + str(matrix.is_row())
        string += "\n- Normal: " + str(matrix.is_normal())
        string += "\n- Nula: " + str(matrix.is_null())
        string += "\n- Ortogonal: " + str(matrix.is_orthogonal())
        string += "\n- Quadrada: " + str(matrix.is_square())
        string += "\n- Simétrica: " + str(matrix.is_symmetric())
        string += "\n- Traço: " + (str(matrix.get_trace()).replace("(","").replace(")","").replace("j","i") if matrix.is_square() else "N/D")
        string += "\n- Triangular Inferior: " + str(matrix.is_lower_triangular())
        string += "\n- Triangular Superior: " + str(matrix.is_upper_triangular())
        return string

    def execute(self, instruction: dict):
        command = instruction["command"]
        args = instruction["args"]
        
        # Carrega as matrizes de um arquivo.
        if command == "load":
            self.__core.load_matrices_from_file(args)

        # Salva as matrizes em um arquivo.
        elif command == "save":
            self.__core.save_matrices(args)

        # Deleta uma matriz do dicionário de matrizes.
        elif command == "delete":
            self.__core.delete_matrix(args)

        # Carrega instruções de um arquivo e as executa.
        elif command == "execute":
            self.__core.execute_instructions(args)

        # Altera a configuração de imprimir a matriz na tela.
        elif command == "show":
            self.__core.set_config("show_matrix", args)

        # Altera a configuração de salvar as instruções.
        elif command == "log":
            self.__core.set_config("show_old_instructions", args)          
            
        # Imprime uma lista com todas as matrizes disponíveis.
        elif command == "list":
            return self.__get_matrix_list_string(self.__core.get_matrices())

        # Imprime uma lista com todas as propriedades da matriz atual.
        elif command == "prop":
            matrix = self.__core.get_matrix(args)
            return self.__get_matrix_properties_string(matrix)

        # Define uma matriz a ser usada nas operações elementares.
        elif command == "use":
            self.__core.use_matrix(args)

        # Imprime uma lista de comando do terminal.
        elif command == "help":
            return command_list_string

        # Encerra a aplicação.
        elif command == "exit":
            self.__core.stop()

        # Apaga o histórico de instruções.
        elif command == "clear":
            self.__core.clear_history()

        # Caso nenhuma condição acima seja atendida, o comando não existe.
        else: raise CommandNotExistsError(command)
