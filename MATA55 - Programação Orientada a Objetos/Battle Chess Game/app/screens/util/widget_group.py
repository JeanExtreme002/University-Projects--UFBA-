class WidgetGroup(object):
    """
    Classe para criar um grupo de widgets.
    """
    def __init__(self, widget_group = None):
        self.__widgets = []

        if widget_group:
            widget_group.add(self)

    def add(self, widget):
        """
        Adiciona um widget ao grupo.
        """
        self.__widgets.append(widget)

    def draw(self):
        """
        Desenha todos os widgets do grupo.
        """
        for widget in self.__widgets:
            widget.draw()

