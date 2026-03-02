"""
Named Entity DFA — detects known abbreviations and titles (rule-based, NOT ML NER).
"""

from .base import BaseDFA


class NamedEntityDFA(BaseDFA):
    """
    DFA for detecting known abbreviations and titles.

    Patterns recognised:
        Tamil titles : டா., டாக்டர்., திரு, திருமதி, செல்வி
        English titles: Dr., Mr., Mrs., Prof.

    The lookup table comes from the language resource file.

    State Machine:
        START → ENTITY_MATCH → END
    """

    _DEFAULT_ENTITIES = {
        'டா.', 'டாக்டர்.', 'திரு', 'திருமதி', 'செல்வி',
        'Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Prof.',
        'Sr.', 'Jr.', 'St.',
    }

    def __init__(self, known_entities=None):
        super().__init__()
        self.states = ['START', 'ENTITY_MATCH', 'END']
        self._entities = set(known_entities) if known_entities else self._DEFAULT_ENTITIES

    def match(self, text):
        states_traversed = ['START']
        if text in self._entities:
            states_traversed.extend(['ENTITY_MATCH', 'END'])
            return {
                'matched': True,
                'states': states_traversed,
                'entity': text,
            }
        return {'matched': False, 'states': states_traversed}
