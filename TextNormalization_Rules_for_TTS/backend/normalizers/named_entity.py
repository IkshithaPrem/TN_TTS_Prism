"""
Named Entity Normalizer
Expands known abbreviations and titles (டாக்டர். → டாக்டர்).
"""


class NamedEntityNormalizer:

    def __init__(self, resources):
        ne_res = resources.get('named_entities', {})
        self.abbreviations = ne_res.get('abbreviations', {})

    def normalize(self, text):
        """டாக்டர். → டாக்டர்"""
        return self.abbreviations.get(text, text)
