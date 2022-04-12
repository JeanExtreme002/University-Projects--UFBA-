from .errors import *
from .util import *

class Terminal(object):
    
    __config = {
        "show_matrix": True,
        "show_old_instructions": False
    }
    __on_session = False
    __instruction_log = list()
    __input_message = "Command>"

    def __init__(self, core):
        self.__core = core

    def __get_boolean_from_string(self, string):
        string = string.lower()
        
        if string == "true": return True
        elif string == "false": return False
        else: raise BooleanConfigError

    def clear_history(self):
        """
        Apaga o registro de todas as instruções antigas.
        """
        self.__instruction_log = []

    def input(self, input_ = None):
        """
        Obtém o input do usuário.
        """
        instruction = input(self.__input_message + " ").strip() if not input_ else input_
        self.__instruction_log.append(instruction)
        
        self.__on_session = True
        return instruction

    def output(self, message = None, error = False, error_line = None):
        """
        Imprime uma string no terminal.
        """
        self.update()
        self.__on_session = False

        # Se a mensagem for um erro, algumas informações adicionais serão colocadas antes da mensagem.
        if error:
            error_line = " L{}".format(error_line) if error_line else ""
            message = "[ERROR{}]: {}".format(error_line, str(message).replace("'", ""))
        if message: self.wait_user(message)

    def print_matrix_properties(self, matrix):
        """
        Imprime as propriedades da matriz.
        """ 
        print_matrix_properties(matrix)

    def print_matrix_in_use(self):
        """
        Imprime a matrix que está sendo usada.
        """
        try: matrix, name = self.__core.get_matrix_in_use()
        except: matrix, name = None, None

        n_matrices = self.__core.get_number_of_matrices()
        print_matrix_in_use(name, matrix, n_matrices, self.__config["show_matrix"])

    def print_instruction(self, instruction):
        """
        Imprime uma instrução formatada.
        """  
        print(self.__input_message, instruction, "\n")
        
    def print_old_instructions(self):
        """
        Imprime todas as instruções executadas anteriormente.
        """  
        for instruction in self.__instruction_log:
            self.print_instruction(instruction)

    def set_config(self, key, value):
        """
        Define uma configuração do terminal.
        """
        value = self.__get_boolean_from_string(value)
        
        if not key in self.__config: raise ConfigNotExistsError
        self.__config[key] = value

    def wait_user(self, message):
        """
        Imprime uma mensagem de erro e congela o programa
        até o usuário apertar ENTER.
        """
        input((message if message else "") + "\n\n(Pressione ENTER para continuar)")

    def update(self):
        """
        Atualiza a tela do terminal.
        """
        clear_terminal()
        self.print_matrix_in_use()
        
        if self.__config["show_old_instructions"]: self.print_old_instructions()
        elif self.__on_session and self.__instruction_log: self.print_instruction(self.__instruction_log[-1])
