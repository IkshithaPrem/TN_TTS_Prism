"""
Time normalization
"""
from typing import Dict
import re


class TimeNormalizer:
    """Normalizes time expressions"""
    
    def normalize(self, time_str: str, locale: str, rules: Dict) -> str:
        """Normalize a time string"""
        time_formats = rules.get("formats", [])
        time_words = rules.get("words", {})
        
        # Try to match time patterns
        for fmt_info in time_formats:
            pattern = fmt_info.get("pattern", "")
            
            try:
                match = re.match(pattern, time_str, re.IGNORECASE)
                if match:
                    hour = int(match.group(1))
                    minute = int(match.group(2)) if match.group(2) else 0
                    period = match.group(3) if len(match.groups()) > 2 and match.group(3) else None
                    
                    # Normalize hour
                    hour_word = self._normalize_hour(hour, locale, rules)
                    
                    # Normalize minute
                    if minute == 0:
                        minute_word = ""
                        time_phrase = time_words.get("o_clock", "बजे")
                    else:
                        minute_word = self._normalize_minute(minute, locale, rules)
                        time_phrase = time_words.get("minutes", "मिनट")
                    
                    # Handle AM/PM
                    period_word = ""
                    if period:
                        if period.upper() == "AM":
                            period_word = time_words.get("am", "सुबह")
                        elif period.upper() == "PM":
                            period_word = time_words.get("pm", "शाम")
                    
                    # Construct time string
                    if minute == 0:
                        if period_word:
                            return f"{period_word} {hour_word} {time_phrase}"
                        else:
                            return f"{hour_word} {time_phrase}"
                    else:
                        if period_word:
                            return f"{period_word} {hour_word} {time_words.get('and', 'बजकर')} {minute_word} {time_phrase}"
                        else:
                            return f"{hour_word} {time_words.get('and', 'बजकर')} {minute_word} {time_phrase}"
            except:
                continue
        
        return time_str
    
    def _normalize_hour(self, hour: int, locale: str, rules: Dict) -> str:
        """Normalize hour to words"""
        from .number_normalizer import NumberNormalizer
        normalizer = NumberNormalizer()
        number_rules = {"words": rules.get("number_words", {})}
        return normalizer.normalize_cardinal(str(hour), locale, number_rules)
    
    def _normalize_minute(self, minute: int, locale: str, rules: Dict) -> str:
        """Normalize minute to words"""
        from .number_normalizer import NumberNormalizer
        normalizer = NumberNormalizer()
        number_rules = {"words": rules.get("number_words", {})}
        return normalizer.normalize_cardinal(str(minute), locale, number_rules)
