"""
Unit normalization
"""
from typing import Dict
import re
from .number_normalizer import NumberNormalizer


class UnitNormalizer:
    """Normalizes unit expressions"""
    
    def normalize(self, unit_str: str, locale: str, rules: Dict) -> str:
        """Normalize a unit string"""
        units = rules.get("units", {})
        
        # Extract number and unit
        match = re.match(r'([\d,]+)\s*([a-zA-Z]+)', unit_str)
        if not match:
            return unit_str
        
        number_str = match.group(1).replace(",", "")
        unit_symbol = match.group(2).lower()
        
        try:
            number = int(number_str)
        except ValueError:
            return unit_str
        
        # Get unit name
        unit_name = units.get(unit_symbol, unit_symbol)
        
        # Normalize number
        normalizer = NumberNormalizer()
        number_rules = {"words": rules.get("number_words", {})}
        number_word = normalizer.normalize_cardinal(number_str, locale, number_rules)
        
        return f"{number_word} {unit_name}"
