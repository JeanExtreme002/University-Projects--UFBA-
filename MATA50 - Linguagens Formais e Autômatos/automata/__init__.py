from .errors import *

class DeterministicFiniteAutomata(object):

    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.__states = states
        self.__alphabet = alphabet
        
        self.__transition_function = transitions
        
        self.__initial_state = initial_state
        self.__final_states = final_states

    def __validate(self, word, current_state):
        if not word: return str() in self.__final_states
        
        try: new_state = self.__transition_function(current_state, word[0])
        except IllegalTransitionOperationError: return False

        if len(word) == 1: return new_state in self.__final_states
        else: return self.__validate(word[1:], new_state)

    def run(self, word) -> bool:
        return self.__validate(word, self.__initial_state)
