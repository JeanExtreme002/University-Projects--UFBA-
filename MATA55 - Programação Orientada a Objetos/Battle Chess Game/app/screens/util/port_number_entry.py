from .entry import Entry

class PortNumberEntry(Entry):
    """
    Classe para criar caixas de input para número PORT.
    """
    def add_char(self, char: str) -> bool:
        """
        Adiciona um caractere ao final da caixa de texto.
        """
        string = self.get_text()

        # Impede a entrada de caracteres inválidos.
        if not char in "0123456789": return False

        # Impede que exista mais de 5 dígitos na string.
        if len(string) >= 5: return False
        
        # Adiciona o caractere à caixa de texto.
        super().add_char(char)
        return True
