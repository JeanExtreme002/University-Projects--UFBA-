from .errors import *
from .transitions import *

class DFAutomata(object):
    """
    Classe para criar Autômatos Finitos Determinísticos.
    """
    def __init__(self, transitions, initial_state, final_states):
        if not isinstance(transitions, DFATransitions):
            raise TypeError("Transitions must be a DFATransitions object")
            
        self.__transition_function = transitions
        self.__initial_state = initial_state
        self.__final_states = set(final_states)

    def run(self, word: str) -> bool:
        # Verifica se o estado inicial é final.
        if word is None or word == str():
            return self.__initial_state in self.__final_states

        state = self.__initial_state

        # Executa a função de transição para cada caractere, até chegar no último estado possível.
        for char in word:
            try: state = self.__transition_function(state, char)
            except IllegalTransitionOperationError: return False

        # Verifica se o estado é final.
        return state in self.__final_states

class NDFAutomata(object):
    """
    Classe para criar Autômatos Finitos Não Determinísticos.
    """
    def __init__(self, transitions, initial_states, final_states):
        if not isinstance(transitions, NDFATransitions):
            raise TypeError("Transitions must be a NDFATransitions object")
            
        self.__transition_function = transitions
        self.__initial_states = set(initial_states)
        self.__final_states = set(final_states)

    def __walk_through(self, word, states):
        for state in states:
            result = self.__validate(word, state)
            if result: return True
        return False
    
    def __validate(self, word, state):
        # Executa a função de transição e obtém os resultados.
        try: states = self.__transition_function(state, word[0])
        except IllegalTransitionOperationError: return False

        # Se ainda houver caracteres, o autômato continua percorrendo todos os possíveis caminhos.
        if len(word) > 1: return self.__walk_through(word[1:], states)

        # Se chegou ao final da palavra, verifica se algum dos estados é final.
        else: return any([state in self.__final_states for state in states])

    def run(self, word: str) -> bool:
        # Verifica se algum dos estados inicias é final.
        if word is None or word == str():
            return any([state in self.__final_states for state in self.__initial_states])

        # Percorre todos os possíveis caminhos.
        return self.__walk_through(word, self.__initial_states)
