from .entry import Entry

class IPAddressEntry(Entry):
    """
    Classe para criar caixas de input para endereço IP.
    """
    def add_char(self, char: str):
        """
        Adiciona um caractere ao final da caixa de texto.
        """
        string = self.get_text()

        # Impede a entrada de caracteres inválidos.
        if not char in "0123456789" and not char == ".":
            return False

        # Impede que exista mais de 3 pontos na string.
        if char == "." and string.count(".") >= 3:
            return False

        # Impede que existam pontos repetidos.
        if char == "." and string and string[-1] == ".":
            return False

        # Impede que exista uma sequência de 4 números ou mais.
        if len(string) >= 3 and char.isnumeric() and string[-1:-4:-1].isnumeric():
            return False

        # Adiciona o caractere à caixa de texto.
        super().add_char(char)
        return True
