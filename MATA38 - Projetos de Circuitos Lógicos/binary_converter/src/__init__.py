__author__ = "Jean Loui Bernard Silva de Jesus"

from .binary import BinaryValue
from .core import paths, window_config
from .gui import ApplicationWindow

class Application(object):
    """
    Classe principal da aplicação.
    """

    __conversion_options = [
        {"label": "Binário", "function": BinaryValue.get_binary},
        {"label":"Decimal", "function": BinaryValue.to_decimal},
        {"label":"Sinal-Magnitude", "function": BinaryValue.to_sign_magnitude},
        {"label":"Complemento de 1", "function": BinaryValue.to_one_s_complement},
        {"label":"Complemento de 2", "function": BinaryValue.to_two_s_complement},
        {"label":"IEEE-754 (32 bits)", "function": BinaryValue.to_ieee_754},
        {"label":"IEEE-754 (64 bits)", "function": BinaryValue.to_ieee_754_x64}
    ]

    def __init__(self):
        super().__init__()
        self.__option = 0

    def __change_option(self, option):
        # Define a opção e faz o tratamento do input, para que o mesmo se adeque à opção selecionada.
        self.__option = option
        self.__parse_input(self.__window.get_input_variable())

    def __convert_value(self, value):
        # Caso o input não contenha valor númerico, nenhuma conversão é realizada.
        if len(value.replace("-", "").replace(".", "")) == 0: return ""

        # Cria um objeto de BinaryValue, a partir do input do usuário, e chama o método
        # respectivo à opção que o usuário selecionou.
        binary_value = BinaryValue(float(value) if self.__option == 0 else value)
        return self.__conversion_options[self.__option]["function"](binary_value)

    def __parse_input(self, input_variable):
        string = input_variable.get().replace(",", ".")

        # Remove sinais negativos e pontos flutuantes excedentes, deixando a string
        # com apenas um sinal negativo e um ponto flutuante no máximo.
        if "-" in string: string = string[0] + string[1:].replace("-", "")
        if "." in string: string = string.replace(".", "", string.count(".") - 1)

        # Caso a opção seja zero (converter decimal para binário), sinal negativo, ponto flutuante e números
        # de 0 à 9 serão aceitos. Caso contrário, o input deverá ser um binário, ou seja, será aceito apenas
        # sinal negativo, ponto flutuante e bit (0 ou 1).
        if self.__option == 0: input_variable.set("".join([char for char in string if char in "0123456789.-"]))
        else: input_variable.set("".join([char for char in string if char in "01.-"]))

    def __on_key_release(self, input_variable):
        # Faz o tratamento do input do usuário antes de usuá-lo na conversão, removendo caracteres inválidos.
        self.__parse_input(input_variable)
        value = input_variable.get()

        # Obtém o resultado da conversão e mostra na tela.
        output = self.__convert_value(value)
        self.__window.set_output(output)

    def run(self):
        # Obtém as configurações da janela, caminhos de arquivos necessários e lista de opções de conversão.
        title, icon, logo = window_config["title"], paths["icon"], paths["logo"]
        options = [option["label"] for option in self.__conversion_options]

        # Cria a janela da aplicação, constrói os widgets e inicializa a execução.
        self.__window = ApplicationWindow(title, icon)
        self.__window.build(options, self.__on_key_release, self.__change_option, logo)
        self.__window.mainloop()
