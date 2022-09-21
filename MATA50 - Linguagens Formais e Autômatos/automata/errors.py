class TransitionException(Exception):
    def __init__(self, state, operation):
        self.state = state
        self.operation = operation


class IllegalTransitionOperationError(TransitionException):
    def __str__(self):
        return "Operation \"{}:{}\" is not defined".format(self.state, self.operation)


class TransitionExistsException(TransitionException):
    def __str__(self):
        return "Transition from \"{}\" by \"{}\" already exists".format(self.state, self.operation)
