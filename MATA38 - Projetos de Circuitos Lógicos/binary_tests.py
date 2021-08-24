__author__ = "Jean Loui Bernard Silva de Jesus"

from binary import BinaryValue

# Inicia com valor 10 (binário: 1010)
value = BinaryValue(10)
assert value.get_binary() == "1010"

# Ao somá-lo com 5, do tipo float, o valor deve ser 15 (binário: 1111).
value = value + 5
assert value == 15
assert value.get_binary() == "1111"

# Ao somá-lo com 5, do tipo BinaryValue, o valor deve ser 20 (binário: 10100).
value = value + BinaryValue(5)
assert value == 20
assert value.get_binary() == "10100"

# Ao subtrair 5, do tipo float, o valor deve ser 15 (binário: 1111).
value = value - 5
assert value == 15
assert value.get_binary() == "1111"

# Ao subtrair 10, do tipo BinaryValue, o valor deve ser 5 (binário: 101).
value = value - BinaryValue(10)
assert value == 5
assert value.get_binary() == "101"

# Ao subtrair (-2), o valor deve ser 7 (binário: 111).
value = value - (-2)
assert value == 7
assert value.get_binary() == "111"

# Ao subtrair 14, o valor deve ser -7 (binário: -111).
value = value - 14
assert value == -7
assert value.get_binary() == "-111"

# Ao subtrair 0.625, o valor deve ser -7.625 (binário: -111.101).
value = value - 0.625
assert value == -7.625
assert value.get_binary() == "-111.101"

# Tenta converter o número natural em binário para complemento de 1 e 2.
# Como o valor é positivo, o binário não deve ser convertido.
value = BinaryValue(3) # Binário original: "11"
assert value.to_one_s_complement() == "011"
assert value.to_two_s_complement() == "011"

# Converte inteiro negativo para complemento de 1 e 2.
value = BinaryValue(-3) # Binário original: "-11"
assert value.to_one_s_complement() == "100"
assert value.to_two_s_complement() == "101"

# Converte número real negativo para complemento de 1 e 2.
value = BinaryValue(-5.625) # Binário original: "-101.101"
assert value.to_one_s_complement() == "1010.010"
assert value.to_two_s_complement() == "1010.011"

# Converte número real positivo para IEEE-754 com precisão de 32 bits.
value = BinaryValue(0.375) # Binário original: "0.011"
assert value.to_ieee_754() == "0" + "01111101" + "10000000000000000000000"

# Converte número real negativo para IEEE-754 com precisão de 32 bits.
value = BinaryValue(-0.241455078125) # Binário original: "-0.001111011101"
assert value.to_ieee_754() == "1" + "01111100" + "11101110100000000000000"

# Converte número real positivo para IEEE-754 com precisão de 64 bits.
value = BinaryValue(0.625) # Binário original: "0.101"
assert value.to_ieee_754_x64() == "0" + "01111111110" + "0100000000000000000000000000000000000000000000000000"

# Converte número real negativo para IEEE-754 com precisão de 64 bits.
value = BinaryValue(-731.5) # Binário original: "-1011011011.1"
assert value.to_ieee_754_x64() == "1" + "10000001000" + "0110110111000000000000000000000000000000000000000000"
