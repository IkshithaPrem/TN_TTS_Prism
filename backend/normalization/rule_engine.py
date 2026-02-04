"""
Rule Engine for loading and managing normalization rules per locale
"""
import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


class RuleEngine:
    """Manages normalization rules for different locales"""
    
    def __init__(self, locales_dir: Optional[str] = None):
        if locales_dir is None:
            # Default to locales directory relative to this file
            base_dir = Path(__file__).parent.parent
            locales_dir = base_dir / "locales"
        
        self.locales_dir = Path(locales_dir)
        self.rules_cache: Dict[str, Dict[str, Any]] = {}
        self._load_all_rules()
    
    def _load_all_rules(self):
        """Load all locale rule files"""
        if not self.locales_dir.exists():
            raise FileNotFoundError(f"Locales directory not found: {self.locales_dir}")
        
        for rule_file in self.locales_dir.glob("*.yml"):
            locale = rule_file.stem
            self._load_locale_rules(locale)
    
    def _load_locale_rules(self, locale: str):
        """Load rules for a specific locale"""
        rule_file = self.locales_dir / f"{locale}.yml"
        
        if not rule_file.exists():
            raise FileNotFoundError(f"Rule file not found: {rule_file}")
        
        with open(rule_file, 'r', encoding='utf-8') as f:
            rules = yaml.safe_load(f)
            self.rules_cache[locale] = rules
    
    def get_rules(self, locale: str) -> Dict[str, Any]:
        """Get rules for a locale"""
        if locale not in self.rules_cache:
            self._load_locale_rules(locale)
        
        return self.rules_cache.get(locale, {})
    
    def get_supported_locales(self) -> List[str]:
        """Get list of all supported locales"""
        return list(self.rules_cache.keys())
    
    def reload_rules(self, locale: Optional[str] = None):
        """Reload rules for a locale or all locales"""
        if locale:
            self._load_locale_rules(locale)
        else:
            self._load_all_rules()
