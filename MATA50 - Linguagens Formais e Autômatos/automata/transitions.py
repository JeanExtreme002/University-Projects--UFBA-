from .errors import *

class Transitions(object):
    """
    Transições de Autômatos.
    """
    def __init__(self):
        self.__transitions = dict()

    def __call__(self, state, operation):
        try: return self.__transitions[state][operation]
        except KeyError: raise IllegalTransitionOperationError(state, operation)

    def add_transition(self, origin, operation, dest):
        if not self.has_transition(origin, operation): self.set_transition(origin, operation, dest)
        else: raise TransitionExistsException(origin, operation)

    def has_transition(self, origin, operation):
        return origin in self.__transitions and operation in self.__transitions[origin]
        
    def set_transition(self, origin, operation, dest):
        if not isinstance(origin, str): raise TypeError("Origin must be a string, not {}".format(type(origin).__name__))
        if not isinstance(operation, str): raise TypeError("Operation must be a string, not {}".format(type(operation).__name__))

        state = self.__transitions.get(origin, dict())
        state[operation] = dest
        self.__transitions[origin] = state

    def remove_transition(self, origin, operation):
        try: self.__transitions.get(origin, dict()).pop(operation)
        except KeyError: pass


class DFATransitions(Transitions):
    """
    Transições de Autômatos Finitos Determinísticos.
    """    
    def set_transition(self, origin, operation, dest):
        if not isinstance(dest, str): raise TypeError("Dest must be a string, not {}".format(type(dest).__name__))
        super().set_transition(origin, operation, dest)


class NDFATransitions(Transitions):
    """
    Transições de Autômatos Finitos Não Determinísticos.
    """
    def add_transition(self, origin, operation, *dest):
        super().add_transition(origin, operation, dest)
        
    def set_transition(self, origin, operation, *dest):
        
        if len(dest) == 1 and type(dest[0]) is tuple:
            dest = dest[0]

        if len(dest) == 0:
            raise TypeError("You must set at least one destination")
            
        for state in dest:
            if not isinstance(state, str):
                raise TypeError("Dest must be a string, not {}".format(type(state).__name__))
        super().set_transition(origin, operation, set(dest))
