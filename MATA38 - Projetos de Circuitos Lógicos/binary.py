__author__ = "Jean Loui Bernard Silva de Jesus"

from binary_calculator import add_binary
from binary_converter import convert_decimal_to_binary

class BinaryValue(object):

    def __init__(self, value):
        self.__decimal_value = float(value)
        self.__binary_value = self.__to_binary(value)

    def __add__(self, value):
        return BinaryValue(self.__decimal_value + float(value))

    def __sub__(self, value):
        return BinaryValue(self.__decimal_value - float(value))

    def __iadd__(self, value):
        self.__decimal_value += float(value)
        self.__binary_value = self.__to_binary(self.__decimal_value)
        return self

    def __isub__(self, value):
        self.__decimal_value -= float(value)
        self.__binary_value = self.__to_binary(self.__decimal_value)
        return self

    def __eq__(self, value):
        return self.__decimal_value == float(value)

    def __float__(self):
        # A classe BinaryValue possui esse método para possibilitar operações
        # aritméticas entre dois objetos de BinaryValue ou entre um objeto de
        # BinaryValue e um valor float.
        return self.__decimal_value

    def __int__(self):
        return int(self.__decimal_value)

    def __repr__(self):
        return self.__binary_value + "(2)"

    def __str__(self):
        return self.__binary_value

    def __to_binary(self, value):
        return convert_decimal_to_binary(value)

    def get_binary(self):
        return self.__binary_value

    def to_decimal(self):
        return self.__decimal_value

    def to_one_s_complement(self):
        # Se o valor for positivo, não é necessário a conversão.
        if self.__decimal_value >= 0: return "0" + self.__binary_value

        # Remove o sinal negativo do valor e realiza o flip (troca de bit).
        binary = "0" + self.__binary_value.replace("-", "")
        return "".join([("0" if bit == "1" else "1") if bit in "01" else bit for bit in binary])

    def to_two_s_complement(self):
        # Se o valor for positivo, não é necessário a conversão.
        if self.__decimal_value >= 0: return "0" + self.__binary_value

        binary = self.__binary_value

        # Armazena a posição do ponto flutuante para unir os bits e fazer o
        # complemento de 2. Essa posição é o número de casas andadas da
        # direita para esquerda do valor. Isso porque, depois da conversão, o
        # binário pode aumentar em 1 bit. Sendo assim, a referência passa a ser
        # a posição do último bit da parte fracionária.
        point_position = (len(binary) - (binary.find(".") + 1)) if binary.find(".") != -1 else -1

        # Converte para complemento de 1, remove o seu ponto flutuante e depois soma 1.
        binary = add_binary(self.to_one_s_complement().replace(".", ""), "1")

        # Retorna o valor convertido com o seu ponto flutuante, caso haja.
        return binary if point_position == -1 else (binary[:-point_position] + "." + binary[-point_position:])
