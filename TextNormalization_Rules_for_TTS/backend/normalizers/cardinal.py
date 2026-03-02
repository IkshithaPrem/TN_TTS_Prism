"""
Cardinal Normalizer
Converts cardinal numbers (123) to spoken Tamil form.
"""

from .number_converter import NumberToWordsConverter


class CardinalNormalizer:

    def __init__(self, resources):
        self.converter = NumberToWordsConverter(resources)

    def normalize(self, text):
        """123 → நூற்று இருபத்திமூன்று"""
        return self.converter.convert(int(text))
