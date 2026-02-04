"""
Main normalization pipeline
"""
from typing import Dict, List, Any, Optional, Tuple
import re

from .rule_engine import RuleEngine
from .dfa_engine import DFAEngine
from .number_normalizer import NumberNormalizer
from .date_normalizer import DateNormalizer
from .time_normalizer import TimeNormalizer
from .currency_normalizer import CurrencyNormalizer
from .unit_normalizer import UnitNormalizer
from .abbreviation_normalizer import AbbreviationNormalizer


class NormalizationPipeline:
    """Main pipeline for text normalization"""
    
    def __init__(self, locales_dir: Optional[str] = None):
        self.rule_engine = RuleEngine(locales_dir)
        self.dfa_engine = DFAEngine()
        self.number_normalizer = NumberNormalizer()
        self.date_normalizer = DateNormalizer()
        self.time_normalizer = TimeNormalizer()
        self.currency_normalizer = CurrencyNormalizer()
        self.unit_normalizer = UnitNormalizer()
        self.abbreviation_normalizer = AbbreviationNormalizer()
    
    def get_supported_locales(self) -> List[str]:
        """Get list of supported locales"""
        return self.rule_engine.get_supported_locales()
    
    def get_rules(self, locale: str) -> Dict[str, Any]:
        """Get rules for a locale"""
        return self.rule_engine.get_rules(locale)
    
    def normalize(self, text: str, locale: str) -> Dict[str, Any]:
        """
        Normalize text for a given locale
        Returns: {
            "normalized_text": str,
            "tokens": List[Dict]  # Each token has: text, category, original, normalized
        }
        """
        if locale not in self.get_supported_locales():
            raise ValueError(f"Locale '{locale}' not supported")
        
        rules = self.get_rules(locale)
        tokens = []
        normalized_parts = []
        
        # Track positions of normalized segments
        last_pos = 0
        segments = []
        
        # Process each category
        # 1. Numbers (cardinal and ordinal)
        number_matches = self._find_number_matches(text, locale, rules)
        segments.extend(number_matches)
        
        # 2. Currency
        currency_matches = self._find_currency_matches(text, locale, rules)
        segments.extend(currency_matches)
        
        # 3. Dates
        date_matches = self._find_date_matches(text, locale, rules)
        segments.extend(date_matches)
        
        # 4. Time
        time_matches = self._find_time_matches(text, locale, rules)
        segments.extend(time_matches)
        
        # 5. Units
        unit_matches = self._find_unit_matches(text, locale, rules)
        segments.extend(unit_matches)
        
        # 6. Abbreviations
        abbrev_matches = self._find_abbreviation_matches(text, locale, rules)
        segments.extend(abbrev_matches)
        
        # Sort segments by position
        segments.sort(key=lambda x: x[0])
        
        # Remove overlaps (keep first match)
        non_overlapping = []
        last_end = -1
        for start, end, original, category, normalized in segments:
            if start >= last_end:
                non_overlapping.append((start, end, original, category, normalized))
                last_end = end
        
        # Build normalized text
        result_text = ""
        last_pos = 0
        
        for start, end, original, category, normalized in non_overlapping:
            # Add text before match
            if start > last_pos:
                result_text += text[last_pos:start]
            
            # Add normalized match
            result_text += normalized
            
            # Track token
            tokens.append({
                "original": original,
                "normalized": normalized,
                "category": category,
                "start": start,
                "end": end
            })
            
            last_pos = end
        
        # Add remaining text
        if last_pos < len(text):
            result_text += text[last_pos:]
        
        return {
            "normalized_text": result_text,
            "tokens": tokens
        }
    
    def _find_number_matches(self, text: str, locale: str, rules: Dict) -> List[Tuple[int, int, str, str, str]]:
        """Find and normalize number matches"""
        matches = []
        number_rules = rules.get("numbers", {})
        
        # Cardinal numbers
        cardinal_patterns = number_rules.get("cardinal", {}).get("patterns", [])
        for pattern_info in cardinal_patterns:
            regex = pattern_info.get("regex", pattern_info.get("pattern", ""))
            try:
                for match in re.finditer(regex, text):
                    number_str = match.group()
                    normalized = self.number_normalizer.normalize_cardinal(
                        number_str, locale, number_rules.get("cardinal", {})
                    )
                    matches.append((match.start(), match.end(), number_str, "cardinal", normalized))
            except:
                continue
        
        # Ordinal numbers
        ordinal_patterns = number_rules.get("ordinal", {}).get("patterns", [])
        for pattern_info in ordinal_patterns:
            regex = pattern_info.get("regex", pattern_info.get("pattern", ""))
            try:
                for match in re.finditer(regex, text):
                    number_str = match.group()
                    normalized = self.number_normalizer.normalize_ordinal(
                        number_str, locale, number_rules.get("ordinal", {})
                    )
                    matches.append((match.start(), match.end(), number_str, "ordinal", normalized))
            except:
                continue
        
        return matches
    
    def _find_currency_matches(self, text: str, locale: str, rules: Dict) -> List[Tuple[int, int, str, str, str]]:
        """Find and normalize currency matches"""
        matches = []
        currency_rules = rules.get("currency", {})
        patterns = currency_rules.get("patterns", [])
        
        for pattern_info in patterns:
            regex = pattern_info.get("regex", pattern_info.get("pattern", ""))
            try:
                for match in re.finditer(regex, text):
                    currency_str = match.group()
                    normalized = self.currency_normalizer.normalize(
                        currency_str, locale, currency_rules
                    )
                    matches.append((match.start(), match.end(), currency_str, "currency", normalized))
            except:
                continue
        
        return matches
    
    def _find_date_matches(self, text: str, locale: str, rules: Dict) -> List[Tuple[int, int, str, str, str]]:
        """Find and normalize date matches"""
        matches = []
        date_rules = rules.get("dates", {})
        patterns = date_rules.get("patterns", [])
        
        for pattern_info in patterns:
            regex = pattern_info.get("regex", pattern_info.get("pattern", ""))
            try:
                for match in re.finditer(regex, text):
                    date_str = match.group()
                    normalized = self.date_normalizer.normalize(
                        date_str, locale, date_rules
                    )
                    matches.append((match.start(), match.end(), date_str, "date", normalized))
            except:
                continue
        
        return matches
    
    def _find_time_matches(self, text: str, locale: str, rules: Dict) -> List[Tuple[int, int, str, str, str]]:
        """Find and normalize time matches"""
        matches = []
        time_rules = rules.get("time", {})
        patterns = time_rules.get("patterns", [])
        
        for pattern_info in patterns:
            regex = pattern_info.get("regex", pattern_info.get("pattern", ""))
            try:
                for match in re.finditer(regex, text):
                    time_str = match.group()
                    normalized = self.time_normalizer.normalize(
                        time_str, locale, time_rules
                    )
                    matches.append((match.start(), match.end(), time_str, "time", normalized))
            except:
                continue
        
        return matches
    
    def _find_unit_matches(self, text: str, locale: str, rules: Dict) -> List[Tuple[int, int, str, str, str]]:
        """Find and normalize unit matches"""
        matches = []
        unit_rules = rules.get("units", {})
        patterns = unit_rules.get("patterns", [])
        
        for pattern_info in patterns:
            regex = pattern_info.get("regex", pattern_info.get("pattern", ""))
            try:
                for match in re.finditer(regex, text):
                    unit_str = match.group()
                    normalized = self.unit_normalizer.normalize(
                        unit_str, locale, unit_rules
                    )
                    matches.append((match.start(), match.end(), unit_str, "unit", normalized))
            except:
                continue
        
        return matches
    
    def _find_abbreviation_matches(self, text: str, locale: str, rules: Dict) -> List[Tuple[int, int, str, str, str]]:
        """Find and normalize abbreviation matches"""
        matches = []
        abbrev_rules = rules.get("abbreviations", {})
        patterns = abbrev_rules.get("patterns", [])
        
        for pattern_info in patterns:
            pattern = pattern_info.get("pattern", "")
            regex = pattern_info.get("regex", pattern)
            try:
                for match in re.finditer(regex, text, re.IGNORECASE):
                    abbrev_str = match.group()
                    normalized = self.abbreviation_normalizer.normalize(
                        abbrev_str, locale, abbrev_rules
                    )
                    matches.append((match.start(), match.end(), abbrev_str, "abbreviation", normalized))
            except:
                continue
        
        return matches
