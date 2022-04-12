from matrix import Matrix
from .executor import Executor
from .terminal import Terminal
from .file import load_instructions, load_matrices, save_matrices

class MatrixNotExistsError(Exception):
    def __init__(self, matrix_name):
        self.__matrix_name = matrix_name
        
    def __str__(self):
        return "A matriz \"{}\" não existe.".format(self.__matrix_name)

class NoMatrixInUseError(Exception):
    def __str__(self):
        return "Nenhuma matriz está sendo utilizada no momento."

class Application(object):
    
    __matrices = dict()
    __current_matrix_name = None
    __finish = False

    def __init__(self):
        self.__executor = Executor(self)
        self.__terminal = Terminal(self)

    def clear_history(self):
        self.__terminal.clear_history()
    
    def delete_matrix(self, matrix_name):
        if not matrix_name in self.__matrices: raise MatrixNotExistsError(matrix_name)
        self.__matrices.pop(matrix_name)

        # Verifica se a matriz deletada era a que estava em uso.
        if matrix_name == self.__current_matrix_name:
            self.__current_matrix_name = None

    def execute(self, instruction, n_line = None):
        try:
            output = self.__executor.execute(instruction) if instruction else None
            self.__terminal.output(output)
            return True
        except Exception as error:
            self.__terminal.output(error, error = True, error_line = n_line)
            return False

    def execute_instructions(self, filename):
        line_count = 0
        
        for instruction in load_instructions(filename):
            line_count += 1
            
            instruction = self.__terminal.input(instruction)
            if not self.execute(instruction, line_count): break

    def get_number_of_matrices(self):
        return len(self.__matrices)

    def get_matrices(self):
        return self.__matrices.copy()

    def get_matrix(self, matrix_name):
        if not matrix_name in self.__matrices: raise MatrixNotExistsError(matrix_name)
        return self.__matrices[matrix_name]

    def get_matrix_in_use(self):
        try: return self.get_matrix(self.__current_matrix_name), self.__current_matrix_name
        except: raise NoMatrixInUseError
   
    def load_matrices(self, matrices):
        self.__matrices.update(matrices)

    def load_matrices_from_file(self, filename):
        for matrix in load_matrices(filename):
            self.__matrices[matrix["name"]] = Matrix(*matrix["order"], matrix["values"])

    def run(self):
        self.__finish = False
        
        # Enquanto o usuário não pedir para parar, o programa costantemente obterá
        # e executará uma instrução digitada pelo usuário.
        while not self.__finish:
            self.__terminal.update()
            self.execute(self.__terminal.input()) 

    def save_matrices(self, filename):
        matrices = [{"name": name, "order": matrix.get_order(), "values": matrix.to_list()} for name, matrix in self.__matrices.items()]
        save_matrices(filename, matrices)

    def set_config(self, name, value):
        self.__terminal.set_config(name, value)

    def set_matrix(self, matrix_name, matrix):
        self.__matrices[matrix_name] = matrix

    def stop(self):
        self.__finish = True
    
    def use_matrix(self, matrix_name):
        if not matrix_name in self.__matrices: raise MatrixNotExistsError(matrix_name)
        self.__current_matrix_name = matrix_name
