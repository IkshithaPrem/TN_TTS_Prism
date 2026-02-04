"""
Date normalization
"""
from typing import Dict
import re
from datetime import datetime


class DateNormalizer:
    """Normalizes dates"""
    
    def normalize(self, date_str: str, locale: str, rules: Dict) -> str:
        """Normalize a date string"""
        date_formats = rules.get("formats", [])
        month_names = rules.get("months", {})
        day_names = rules.get("days", {})
        
        # Try to parse different date formats
        for fmt_info in date_formats:
            pattern = fmt_info.get("pattern", "")
            format_str = fmt_info.get("format", "")
            
            try:
                match = re.match(pattern, date_str)
                if match:
                    # Parse the date
                    if format_str == "DD/MM/YYYY":
                        day, month, year = match.groups()
                        day = int(day)
                        month = int(month)
                        year = int(year)
                        
                        # Get month name
                        month_name = month_names.get(str(month), str(month))
                        
                        # Normalize year
                        year_words = self._normalize_year(year, locale, rules)
                        
                        # Normalize day
                        day_words = self._normalize_day(day, locale, rules)
                        
                        return f"{day_words} {month_name} {year_words}"
            except:
                continue
        
        return date_str
    
    def _normalize_year(self, year: int, locale: str, rules: Dict) -> str:
        """Normalize year to words"""
        from .number_normalizer import NumberNormalizer
        normalizer = NumberNormalizer()
        number_rules = {"words": rules.get("number_words", {})}
        return normalizer.normalize_cardinal(str(year), locale, number_rules)
    
    def _normalize_day(self, day: int, locale: str, rules: Dict) -> str:
        """Normalize day to words"""
        from .number_normalizer import NumberNormalizer
        normalizer = NumberNormalizer()
        number_rules = {"words": rules.get("number_words", {})}
        return normalizer.normalize_cardinal(str(day), locale, number_rules)
