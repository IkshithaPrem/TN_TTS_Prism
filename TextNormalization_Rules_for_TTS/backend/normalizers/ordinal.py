"""
Ordinal Normalizer
Converts ordinal expressions (5th, 1st, 3ஆம்) to spoken form.
"""

import re
from .number_converter import NumberToWordsConverter


class OrdinalNormalizer:

    def __init__(self, resources):
        self.converter = NumberToWordsConverter(resources)
        ordinals_res = resources.get('ordinals', {})
        self.mapping = ordinals_res.get('mapping', {})
        self.generic_suffix = ordinals_res.get('generic_suffix', 'ஆம்')

    def normalize(self, text, number_str=None):
        """5th → ஐந்தாவது"""
        if not number_str:
            m = re.match(r'^(\d+)', text)
            if not m:
                return text
            number_str = m.group(1)

        if number_str in self.mapping:
            return self.mapping[number_str]

        return self.converter.convert(int(number_str)) + self.generic_suffix
