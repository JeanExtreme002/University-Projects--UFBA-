__author__ = "Jean Loui Bernard Silva de Jesus"

from .converter import convert_binary_to_decimal, convert_decimal_to_binary

class BinaryValue(object):
    def __init__(self, value):
        """
        O parâmetro "value" deve ser um número, inteiro ou flutuante,
        um binário em formato de string ou mesmo um objeto de BinaryValue.

        Veja alguns exemplos abaixo:
        >>> b = BinaryValue(27.93)
        >>> b = BinaryValue(27)
        >>> b = BinaryValue("10011011")
        >>> b = BinaryValue("-10011011.101001")
        """
        if isinstance(value, str):
            if self.__is_binary(value): self.__init_from_binary(value)
            else: raise ValueError("invalid literal for binary: '{}'".format(value))
        else:
            # Impede que o valor seja infinito ou indefinido.
            if abs(value) == float("inf"): raise OverflowError("cannot convert float infinity to binary")
            if value == float("NaN"): raise ValueError("cannot convert float NaN to binary")
            self.__init_from_decimal(value)

    def __init_from_binary(self, binary):
        binary = self.__format_binary(binary)
        self.__decimal_value = self.__to_decimal(binary)
        self.__binary_value = binary

    def __init_from_decimal(self, decimal):
        self.__decimal_value = float(decimal)
        self.__binary_value = self.__to_binary(self.__decimal_value)

    def __abs__(self):
        return BinaryValue(abs(self.__decimal_value))

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

    def __format_binary(self, binary):
        # Separa o sinal do valor para tratar a string.
        sign = "-" if binary[0] == "-" else ""
        binary = binary.replace("-", "")

        # Remove bits zeros à esquerda desnecessários.
        binary = binary.lstrip("0")
        if not binary.split(".")[0]: binary = "0" + binary

        # Remove bits zeros à direita desnecessários.
        if "." in binary: binary = binary.rstrip("0").rstrip(".")

        return sign + binary

    def __is_binary(self, string):
        try:
            float(string) # Se conseguir converter para float, então o formato está correto.
            return all([char in "01-." for char in string])
        except ValueError: return False

    def __to_binary(self, value):
        return convert_decimal_to_binary(value)

    def __to_decimal(self, value):
        return convert_binary_to_decimal(value)

    def __to_ieee_754(self, precision = 32):
        binary = self.__binary_value.replace("-", "") + ("." if not "." in self.__binary_value else "")
        sign = "1" if "-" in self.__binary_value else "0"

        # Obtém o tamanho do expoente e da mantissa com base na precisão definida para valor.
        exponent_size, mantissa_size = (11, 52) if precision == 64 else (8, 23)

        # A representação para zero no padrão IEEE-754 é o expoente e a mantissa zerados.
        if self.__decimal_value == 0: exponent, mantissa = "0" * exponent_size, "0" * mantissa_size

        # Obtém o expoente, com base no número de casas entre o MSB e o ponto flutuante,
        # e a mantissa, a partir do valor após o MSB, removendo o ponto flutuante da string.
        elif int(binary.split(".")[0]) >= 1:
            exponent = self.__to_binary(2 ** (exponent_size - 1) - 1 + binary.index(".") - 1)
            mantissa = binary.replace(".", "")[1: mantissa_size]
        else:
            msb_index = binary.index("1")
            exponent = self.__to_binary(2 ** (exponent_size - 1) - 1 + (msb_index - binary.index(".")) * -1)
            mantissa = binary[msb_index + 1: msb_index + 1 + mantissa_size]

        # Completa o expoente e a mantissa para ficarem dentro do padrão.
        exponent = "0" * (exponent_size - len(exponent)) + exponent
        mantissa += "0" * (mantissa_size - len(mantissa))

        # Retorna o binário no padrão IEEE-754 (sinal | expoente | mantissa).
        return sign + exponent + mantissa

    def get_binary(self) -> str:
        return self.__binary_value

    def to_decimal(self) -> float:
        return self.__decimal_value

    def to_ieee_754(self) -> str:
        return self.__to_ieee_754(precision = 32)

    def to_ieee_754_x64(self) -> str:
        return self.__to_ieee_754(precision = 64)

    def to_sign_magnitude(self) -> str:
        return ("1" if "-" in self.__binary_value else "0") + self.__binary_value.replace("-", "")

    def to_one_s_complement(self) -> str:
        # Se o valor for positivo, não é necessário a conversão.
        if not "-" in self.__binary_value: return "0" + self.__binary_value.replace("-", "")

        # Remove o sinal negativo do valor e realiza o flip (troca de bit).
        binary = "0" + self.__binary_value.replace("-", "")
        return "".join([("0" if bit == "1" else "1") if bit in "01" else bit for bit in binary])

    def to_two_s_complement(self) -> str:
        # Se o valor for positivo, não é necessário a conversão.
        if self.__decimal_value >= 0: return "0" + self.__binary_value.replace("-", "")

        binary = self.__binary_value

        # Armazena a posição do ponto flutuante para unir os bits e fazer o
        # complemento de 2. Essa posição é o número de casas andadas da
        # direita para esquerda do valor. Isso porque, depois da conversão, o
        # binário pode aumentar em 1 bit. Sendo assim, a referência passa a ser
        # a posição do último bit da parte fracionária.
        point_position = (len(binary) - (binary.find(".") + 1)) if binary.find(".") != -1 else -1

        # Converte para complemento de 1, removendo o seu ponto flutuante, depois converte para decimal,
        # soma 1 ao valor e converte novamente para binário, obtendo assim o complemento de 2.
        binary = self.to_one_s_complement().replace(".", "")
        binary = self.__to_binary(self.__to_decimal(binary) + 1)

        # Retorna o valor convertido com o seu ponto flutuante, caso haja.
        return binary if point_position == -1 else (binary[:-point_position] + "." + binary[-point_position:])
