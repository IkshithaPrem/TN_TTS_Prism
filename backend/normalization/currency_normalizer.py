"""
Currency normalization
"""
from typing import Dict
import re
from .number_normalizer import NumberNormalizer


class CurrencyNormalizer:
    """Normalizes currency expressions"""
    
    def normalize(self, currency_str: str, locale: str, rules: Dict) -> str:
        """Normalize a currency string"""
        currency_symbol = rules.get("symbol", "₹")
        currency_name = rules.get("name", {})
        singular = currency_name.get("singular", "रुपया")
        plural = currency_name.get("plural", "रुपये")
        
        # Extract number from currency string
        number_match = re.search(r'[\d,]+', currency_str)
        if not number_match:
            return currency_str
        
        number_str = number_match.group().replace(",", "")
        
        try:
            number = int(number_str)
        except ValueError:
            return currency_str
        
        # Normalize number
        normalizer = NumberNormalizer()
        number_rules = {"words": rules.get("number_words", {})}
        number_word = normalizer.normalize_cardinal(number_str, locale, number_rules)
        
        # Choose singular or plural
        if number == 1:
            currency_word = singular
        else:
            currency_word = plural
        
        return f"{number_word} {currency_word}"
