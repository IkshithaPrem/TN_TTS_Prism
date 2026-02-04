"""
Number normalization for cardinal and ordinal numbers
"""
from typing import Dict, List


class NumberNormalizer:
    """Normalizes cardinal and ordinal numbers"""
    
    def normalize_cardinal(self, number_str: str, locale: str, rules: Dict) -> str:
        """Normalize a cardinal number"""
        # Remove commas and spaces
        clean_number = number_str.replace(",", "").replace(" ", "").strip()
        
        try:
            number = int(clean_number)
        except ValueError:
            return number_str
        
        # Get locale-specific number words
        number_words = rules.get("words", {})
        
        if number == 0:
            return number_words.get("0", "शून्य" if locale == "hi-IN" else "பூஜ்யம்")
        
        # Get base mappings
        ones = number_words.get("ones", [])
        tens = number_words.get("tens", [])
        hundreds = number_words.get("hundreds", [])
        thousands = number_words.get("thousands", [])
        lakhs = number_words.get("lakhs", [])
        crores = number_words.get("crores", [])
        
        # Handle Indian numbering system
        if number < 100:
            return self._normalize_under_hundred(number, ones, tens)
        elif number < 1000:
            return self._normalize_under_thousand(number, ones, tens, hundreds)
        elif number < 100000:
            return self._normalize_under_lakh(number, ones, tens, hundreds, thousands)
        elif number < 10000000:
            return self._normalize_under_crore(number, ones, tens, hundreds, thousands, lakhs)
        else:
            return self._normalize_crore_plus(number, ones, tens, hundreds, thousands, lakhs, crores)
    
    def normalize_ordinal(self, number_str: str, locale: str, rules: Dict) -> str:
        """Normalize an ordinal number"""
        # Extract number from ordinal (e.g., "1st" -> "1")
        import re
        match = re.search(r'\d+', number_str)
        if not match:
            return number_str
        
        number = int(match.group())
        ordinal_words = rules.get("words", {})
        
        # Get ordinal word for the number
        if str(number) in ordinal_words:
            return ordinal_words[str(number)]
        
        # For numbers not in the list, construct ordinal
        # This is a simplified version - full implementation would need more rules
        return ordinal_words.get(str(number), number_str)
    
    def _normalize_under_hundred(self, number: int, ones: List[str], tens: List[str]) -> str:
        """Normalize numbers under 100"""
        if number < 20:
            if number < len(ones):
                return ones[number]
            return str(number)
        
        tens_digit = number // 10
        ones_digit = number % 10
        
        if ones_digit == 0:
            return tens[tens_digit] if tens_digit < len(tens) else str(number)
        else:
            tens_word = tens[tens_digit] if tens_digit < len(tens) else str(tens_digit * 10)
            ones_word = ones[ones_digit] if ones_digit < len(ones) else str(ones_digit)
            return f"{tens_word} {ones_word}"
    
    def _normalize_under_thousand(self, number: int, ones: List[str], tens: List[str], hundreds: List[str]) -> str:
        """Normalize numbers under 1000"""
        if number < 100:
            return self._normalize_under_hundred(number, ones, tens)
        
        hundreds_digit = number // 100
        remainder = number % 100
        
        hundreds_word = hundreds[hundreds_digit] if hundreds_digit < len(hundreds) else f"{ones[hundreds_digit]} सौ"
        
        if remainder == 0:
            return hundreds_word
        else:
            remainder_word = self._normalize_under_hundred(remainder, ones, tens)
            return f"{hundreds_word} {remainder_word}"
    
    def _normalize_under_lakh(self, number: int, ones: List[str], tens: List[str], hundreds: List[str], thousands: List[str]) -> str:
        """Normalize numbers under 1 lakh (100,000)"""
        if number < 1000:
            return self._normalize_under_thousand(number, ones, tens, hundreds)
        
        thousands_part = number // 1000
        remainder = number % 1000
        
        if thousands_part == 1:
            thousands_word = thousands[0] if thousands else "हज़ार"
        else:
            thousands_base = self._normalize_under_thousand(thousands_part, ones, tens, hundreds)
            thousands_word = f"{thousands_base} {thousands[1] if len(thousands) > 1 else thousands[0] if thousands else 'हज़ार'}"
        
        if remainder == 0:
            return thousands_word
        else:
            remainder_word = self._normalize_under_thousand(remainder, ones, tens, hundreds)
            return f"{thousands_word} {remainder_word}"
    
    def _normalize_under_crore(self, number: int, ones: List[str], tens: List[str], hundreds: List[str], thousands: List[str], lakhs: List[str]) -> str:
        """Normalize numbers under 1 crore (10,000,000)"""
        if number < 100000:
            return self._normalize_under_lakh(number, ones, tens, hundreds, thousands)
        
        lakhs_part = number // 100000
        remainder = number % 100000
        
        if lakhs_part == 1:
            lakhs_word = lakhs[0] if lakhs else "लाख"
        else:
            lakhs_base = self._normalize_under_hundred(lakhs_part, ones, tens)
            lakhs_word = f"{lakhs_base} {lakhs[1] if len(lakhs) > 1 else lakhs[0] if lakhs else 'लाख'}"
        
        if remainder == 0:
            return lakhs_word
        else:
            remainder_word = self._normalize_under_lakh(remainder, ones, tens, hundreds, thousands)
            return f"{lakhs_word} {remainder_word}"
    
    def _normalize_crore_plus(self, number: int, ones: List[str], tens: List[str], hundreds: List[str], thousands: List[str], lakhs: List[str], crores: List[str]) -> str:
        """Normalize numbers 1 crore and above"""
        crores_part = number // 10000000
        remainder = number % 10000000
        
        if crores_part == 1:
            crores_word = crores[0] if crores else "करोड़"
        else:
            crores_base = self._normalize_under_hundred(crores_part, ones, tens)
            crores_word = f"{crores_base} {crores[1] if len(crores) > 1 else crores[0] if crores else 'करोड़'}"
        
        if remainder == 0:
            return crores_word
        else:
            remainder_word = self._normalize_under_crore(remainder, ones, tens, hundreds, thousands, lakhs)
            return f"{crores_word} {remainder_word}"
