class BooleanConfigError(Exception):
    def __str__(self):
        return "Informe \"true\" ou \"false\" para essa configuração."

class ConfigNotExistsError(Exception):
    def __str__(self):
        return "Essa configuração não existe."
