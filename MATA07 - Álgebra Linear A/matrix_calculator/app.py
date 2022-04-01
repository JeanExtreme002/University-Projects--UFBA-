from matrix import Matrix
from terminal import file
from terminal import parser
import os, sys

class Application(object):

    __matrices = dict()
    __command_log = []
    __show_matrix = True
    __show_old_commands = False
    __current_matrix_name = None

    def __execute_application_operation(self, command):
        
        # Carrega as matrizes de um arquivo.
        if command["command"] == "load":
            self.__matrices.update(file.load_matrices(command["args"], convert_to = Matrix))

        # Altera a configuração de imprimir a matriz na tela.
        elif command["command"] == "show":
            if not command["args"].lower() in ["true", "false"]: raise ValueError("Você deve informar a configuração! (true ou false)")
            self.__show_matrix = True if command["args"].lower() == "true" else False

        # Altera a configuração de salvar as instruções.
        elif command["command"] == "log":
            if not command["args"].lower() in ["true", "false"]: raise ValueError("Você deve informar a configuração! (true ou false)")
            self.__show_old_commands = True if command["args"].lower() == "true" else False            
            
        # Imprime uma lista com todas as matrizes disponíveis.
        elif command["command"] == "list":
            self.print_matrices()
            input()

        # Imprime uma lista com todas as propriedades da matriz atual.
        elif command["command"] == "prop":
            self.print_current_matrix_properties()
            input()

        # Define uma matriz a ser usada nas operações elementares.
        elif command["command"] == "use":

            # Verifica se a matriz existe.
            if not command["args"] in self.__matrices:
                raise KeyError("A matriz \"{}\" não existe!".format(command["args"]))
            
            self.__current_matrix_name = command["args"]

        # Imprime uma lista de comando do terminal.
        elif command["command"] == "help":
            print("Lista de Comandos do Terminal:")
            print("{:<20} | Encerra o programa".format("- exit"))
            print("{:<20} | Mostra uma lista com todas as matrizes".format("- list"))
            print("{:<20} | Carrega um arquivo contendo matrizes".format("- load <arquivo.ext>"))
            print("{:<20} | Mostra os comandos anteriores".format("- log <true | false>"))
            print("{:<20} | Mostra uma lista com todas as propriedades da matriz".format("- prop"))
            print("{:<20} | Mostra a matriz que está sendo utilizada".format("- show <true | false>"))
            print("{:<20} | Define uma matriz para ser utilizada".format("- use <matrix>"))
            input()

        # Encerra a aplicação.
        elif command["command"] == "exit":
            self.stop()

        # Caso nenhuma condição acima seja atendida, o comando não existe.
        else: raise ValueError("Esse comando não existe.")
    
    def __execute_elementary_operation(self, command):
        try: matrix = self.__matrices[self.__current_matrix_name]
        except: raise KeyError("Nenhuma matriz está sendo utilizada no momento.")
        
        row1, row2 = int(command["row1"]), (int(command["row2"]) if command["row2"] else None)
        scalar = float(command["scalar"]) if command["scalar"] else 1

        # Troca a posição de duas linhas.
        if command["operator"] == "<>":
            if not row2: raise SyntaxError("Informe a linha que deseja trocar!")
            if command["scalar"]: raise SyntaxError("Não é possível realizar essa operação com um escalar!")
            matrix.interchange_rows(row1, row2)

        # Verifica se as linhas são iguais.
        if command["operator"] == "==":
            if not row2: raise SyntaxError("Informe a linha que deseja verificar a igualdade!")
            if command["scalar"]: raise SyntaxError("Não é possível realizar essa operação com um escalar!")
            input(matrix.get_row(row1) == matrix.get_row(row2))
            
        # Soma, ou subtrai, uma linha por outra linha.
        elif command["operator"] in "+=-=":
            if not row2: raise SyntaxError("Somas e subtrações de linhas são feitas apenas por outras linhas!")
            matrix.add_row(row1, row2, scalar * (-1 if "-" in command["operator"] else 1))

        # Multiplica, ou divide, uma linha por um escalar. 
        else:
            if not command["scalar"]: raise SyntaxError("Informe o escalar para multiplicar ou dividir a linha!")
            matrix.multiply_row(row1, scalar, div = True if command["operator"] == "/=" else False)
            
    def __execute_matrix_operation(self, command):

        # Obtém a matriz conjugada.
        if "c" in command["operator"]:
            if not command["x"] in self.__matrices: raise KeyError("A matriz \"{}\" não existe!".format(command["x"]))
            if command["y"]: raise SyntaxError("Por qual motivo o \"{}\" está presente?".format(command["y"]))
            self.__matrices[command["var"]] = self.__matrices[command["x"]].conjugate()

        # Obtém a matriz transposta.
        if "t" in command["operator"]:
            if not command["x"] in self.__matrices: raise KeyError("A matriz \"{}\" não existe!".format(command["x"]))
            if command["y"]: raise SyntaxError("Por qual motivo o \"{}\" está presente?".format(command["y"]))
            self.__matrices[command["var"]] = self.__matrices[command["x"]].transpose()

        # Soma ou subtrai as matrizes.
        if command["operator"] in "+-":

            # Verifica se existem duas matrizes.
            if not command["x"].isalpha() or not command["y"].isalpha():
                raise SyntaxError("Para operações de soma e subtração, é necessário duas matrizes!")

            # Verifica se elas existem.
            if not command["x"] in self.__matrices: raise KeyError("A matriz \"{}\" não existe!".format(command["x"]))
            if not command["y"] in self.__matrices: raise KeyError("A matriz \"{}\" não existe!".format(command["y"]))

            # Faz a soma, ou subtração, das matrizes.
            try:
                if command["operator"] == "+": self.__matrices[command["var"]] = self.__matrices[command["x"]] + self.__matrices[command["y"]]
                else: self.__matrices[command["var"]] = self.__matrices[command["x"]] - self.__matrices[command["y"]]
            except: raise ValueError("Ambas as matrizes devem ter a mesma ordem!")

        # Multiplica ou divide as matrizes.
        elif command["operator"] in "*/":

            # Verifica se existe pelo menos uma matriz.
            if not command["x"].isalpha():
                raise SyntaxError("Informe uma matriz à esquerda para operações de multiplicação e divisão!")

            # Verifica se as matrizes existem.
            if not command["x"] in self.__matrices: raise KeyError("A matriz \"{}\" não existe!".format(command["x"]))
            if command["y"].isalpha() and not command["y"] in self.__matrices: raise KeyError("A matriz \"{}\" não existe!".format(command["y"]))

            x = self.__matrices[command["x"]]
            y = self.__matrices[command["y"]] if command["y"].isalpha() else float(command["y"])

            if command["operator"] == "/":
                if isinstance(y, Matrix): raise ValueError("Não é possível dividir uma matriz por outra!")
                if y == 0: raise ValueError("Não é possível dividir por zero!")
                
            try:
                if command["operator"] == "*": self.__matrices[command["var"]] = x * y
                else: self.__matrices[command["var"]] = x / y
            except: raise ValueError("O número de colunas da matriz à esquerda deve ser o número de linhas da matriz à direita!")

    def __get_user_input(self):
        """
        Obtém o input do usuário.
        """
        command = input("Command> ").strip()
        print()
        return command
    
    def clear_terminal(self):
        """
        Limpa a tela do terminal.
        """
        if "win" in sys.platform: os.system("cls")
        else: os.system("clear")  

    def execute(self, command):
        """
        Executa uma instrução.
        """
        self.__command_log.append(command)
        command = parser.parse_command(command)
        
        return {
            "application": self.__execute_application_operation,
            "matrix": self.__execute_matrix_operation,
            "elementary": self.__execute_elementary_operation
        }[command["operation"]](command)
        
    def print_current_matrix(self):
        """
        Imprime a matrix que está sendo usada.
        """
        if self.__current_matrix_name:
            print("Atualmente usando a matriz \"{}\". [{} {}]".format(
                self.__current_matrix_name, len(self.__matrices),
                "disponíveis" if len(self.__matrices) > 1 else "disponível"
            ))

            # Mostra a matriz, caso o usuário queira.
            if self.__show_matrix:
                print()
                print(self.__matrices[self.__current_matrix_name])
                
        else:
            print("Atualmente nenhuma matriz está sendo usada. [{} {}]".format(
                len(self.__matrices), "disponíveis" if len(self.__matrices) > 1 else "disponível"
            ))
        print("\n")

    def print_current_matrix_properties(self):
        """
        Imprime as propriedades da matriz.
        """
        try: matrix = self.__matrices[self.__current_matrix_name]
        except: raise KeyError("Nenhuma matriz está sendo utilizada no momento.")
        
        print("Propriedades da Matrix:")
        print("- Anti-hermitiana:", matrix.is_skew_hermitian())
        print("- Anti-simétrica:", matrix.is_skew_symmetric())
        print("- Coluna:", matrix.is_column())
        print("- Complexa:", matrix.is_complex())
        print("- Diagonal:", matrix.is_diagonal())
        print("- Escalar:", matrix.is_scalar())
        print("- Identidade:", matrix.is_identity())
        print("- Hermitiana:", matrix.is_hermitian())
        print("- Linha:", matrix.is_row())
        print("- Nula:", matrix.is_null())
        print("- Quadrada:", matrix.is_square())
        print("- Simétrica:", matrix.is_symmetric())
        print("- Triangular Inferior:", matrix.is_lower_triangular())
        print("- Triangular Superior:", matrix.is_upper_triangular())
        
    def print_matrices(self):
        if self.__matrices: 
            print("Lista de Matrizes:")
            
            for name in self.__matrices.keys():
                print("- {} <{},{}>".format(name, *self.__matrices[name].get_order()))
        else: print("Nenhuma matriz disponível. Use o comando \"load <arquivo.ext>\".")

    def print_old_commands(self):
        """
        Imprime todos os comandos executados anteriormente.
        """
        for command in self.__command_log:
            print("Command>", command)

    def run(self):
        """
        Inicia a execução do programa.
        """
        self.__finish = False

        # Executa o método enquanto não pedir para encerrar.
        while not self.__finish:
            self.clear_terminal()
            self.print_current_matrix()

            # Mostra todos os comandos antigos.
            if self.__show_old_commands:
                self.print_old_commands()
            
            # Executa a instrução do usuário.
            try: self.execute(self.__get_user_input())
            except Exception as error: input("ERRO: " + str(error))

    def stop(self):
        """
        Encerra a aplicação.
        """
        self.__finish = True
            
            
if __name__ == "__main__":
    application = Application()
    application.run()
