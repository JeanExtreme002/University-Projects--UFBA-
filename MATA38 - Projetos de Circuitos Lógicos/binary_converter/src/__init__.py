__author__ = "Jean Loui Bernard Silva de Jesus"

from .binary import BinaryValue
from .core import paths, window_config
from .frames import InputFrame, LogoFrame, OutputFrame
from tkinter import Frame, Tk

class Application(Tk):
    """
    Classe principal da aplicação.
    """
    
    __conversion_options = [
        "Binário",
        "Decimal",
        "Sinal-Magnitude",
        "Complemento de 1",
        "Complemento de 2",
        "IEEE-754 (32 bits)",
        "IEEE-754 (64 bits)",
    ]

    def __init__(self):
        super().__init__()
        self.__option = 0

        self.title(window_config["title"])
        self.iconbitmap(paths["icon"])
        self.resizable(False, False)

    def __change_option(self, option):
        self.__option = option
        self.__parse_input(self.__input_frame.get_input_var())

    def __convert_value(self, value):
        if len(value.replace("-", "").replace(".", "")) == 0: return ""
        binary_value = BinaryValue(float(value) if self.__option == 0 else value)

        if self.__option == 0: return binary_value.get_binary()
        elif self.__option == 1: return binary_value.to_decimal()
        elif self.__option == 2: return binary_value.to_sign_magnitude()
        elif self.__option == 3: return binary_value.to_one_s_complement()
        elif self.__option == 4: return binary_value.to_two_s_complement()
        elif self.__option == 5: return binary_value.to_ieee_754()
        elif self.__option == 6: return binary_value.to_ieee_754_x64()

    def __parse_input(self, input_var):
        string = input_var.get().replace(",", ".")

        if "-" in string: string = string[0] + string[1:].replace("-", "")
        if "." in string: string = string.replace(".", "", string.count(".") - 1)

        if self.__option != 0: input_var.set("".join([char for char in string if char in "01.-"]))
        else: input_var.set("".join([char for char in string if char in "0123456789.-"]))

    def __on_key_release(self, input_var):
        self.__parse_input(input_var)
        value = input_var.get()

        output = self.__convert_value(value)
        self.__output_frame.set_output(output)

    def build(self):
        main_frame = Frame(self)
        main_frame.pack(padx = 10, pady = 10)

        LogoFrame(main_frame, paths["logo"]).pack()
        self.__input_frame = InputFrame(main_frame, self.__on_key_release)
        self.__input_frame.set_menu_options(self.__conversion_options, self.__change_option)
        self.__input_frame.pack(pady = 20)

        self.__output_frame = OutputFrame(main_frame)
        self.__output_frame.pack()
