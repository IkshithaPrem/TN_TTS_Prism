"""
Abbreviation normalization
"""
from typing import Dict


class AbbreviationNormalizer:
    """Normalizes abbreviations"""
    
    def normalize(self, abbrev_str: str, locale: str, rules: Dict) -> str:
        """Normalize an abbreviation"""
        abbreviations = rules.get("mappings", {})
        
        # Try exact match (case-insensitive)
        abbrev_lower = abbrev_str.lower().rstrip('.')
        
        if abbrev_lower in abbreviations:
            return abbreviations[abbrev_lower]
        
        # Try with period
        if abbrev_str in abbreviations:
            return abbreviations[abbrev_str]
        
        return abbrev_str
