from .errors import *
from .transitions import *

class DFAutomata(object):

    def __init__(self, transitions, initial_state, final_states):
        if not isinstance(transitions, DFATransitions):
            raise TypeError("Transitions must be a DFATransitions object")
            
        self.__transition_function = transitions
        self.__initial_state = initial_state
        self.__final_states = set(final_states)

    def run(self, word: str) -> bool:
        if word is None or word == str():
            return self.__initial_state in self.__final_states

        state = self.__initial_state
        
        for char in word:
            try: state = self.__transition_function(state, char)
            except IllegalTransitionOperationError: return False
            
        return state in self.__final_states
