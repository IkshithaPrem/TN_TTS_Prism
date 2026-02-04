"""
DFA (Deterministic Finite Automata) Engine for pattern matching
"""
from typing import Dict, List, Tuple, Optional, Set
import re


class DFAState:
    """Represents a state in the DFA"""
    def __init__(self, state_id: int):
        self.state_id = state_id
        self.transitions: Dict[str, int] = {}  # char -> next_state_id
        self.is_final = False
        self.category: Optional[str] = None
        self.pattern: Optional[str] = None


class DFAEngine:
    """DFA-based pattern matcher for text normalization"""
    
    def __init__(self):
        self.dfas: Dict[str, List[DFAState]] = {}  # category -> DFA states
        self.start_states: Dict[str, int] = {}  # category -> start state ID
    
    def build_dfa_from_patterns(self, category: str, patterns: List[Dict[str, str]]):
        """Build a DFA from a list of patterns"""
        states: List[DFAState] = []
        start_state = DFAState(0)
        states.append(start_state)
        state_counter = 1
        
        for pattern_info in patterns:
            pattern = pattern_info.get("pattern", "")
            regex_pattern = pattern_info.get("regex", pattern)
            
            # Convert regex pattern to DFA states
            current_state = start_state
            
            # For simplicity, we'll use regex matching instead of full DFA
            # In production, you'd want a proper regex-to-DFA conversion
            # For now, we'll store patterns and use regex matching
            
            final_state = DFAState(state_counter)
            final_state.is_final = True
            final_state.category = category
            final_state.pattern = regex_pattern
            states.append(final_state)
            state_counter += 1
        
        self.dfas[category] = states
        self.start_states[category] = 0
    
    def match_patterns(self, text: str, category: str, patterns: List[Dict[str, str]]) -> List[Tuple[int, int, str, Dict]]:
        """
        Match patterns in text and return matches as (start, end, matched_text, pattern_info)
        """
        matches = []
        
        for pattern_info in patterns:
            pattern = pattern_info.get("pattern", "")
            regex_pattern = pattern_info.get("regex", pattern)
            
            try:
                # Compile regex pattern
                regex = re.compile(regex_pattern, re.IGNORECASE)
                
                # Find all matches
                for match in regex.finditer(text):
                    matches.append((
                        match.start(),
                        match.end(),
                        match.group(),
                        pattern_info
                    ))
            except re.error:
                # Invalid regex, skip
                continue
        
        # Sort by start position
        matches.sort(key=lambda x: x[0])
        
        # Remove overlapping matches (keep first)
        non_overlapping = []
        last_end = -1
        
        for start, end, matched, pattern_info in matches:
            if start >= last_end:
                non_overlapping.append((start, end, matched, pattern_info))
                last_end = end
        
        return non_overlapping
    
    def find_all_matches(self, text: str, category_rules: Dict[str, List[Dict]]) -> List[Tuple[int, int, str, str, Dict]]:
        """
        Find all matches across multiple categories
        Returns: (start, end, matched_text, category, pattern_info)
        """
        all_matches = []
        
        for category, patterns in category_rules.items():
            matches = self.match_patterns(text, category, patterns)
            for start, end, matched, pattern_info in matches:
                all_matches.append((start, end, matched, category, pattern_info))
        
        # Sort by start position
        all_matches.sort(key=lambda x: x[0])
        
        return all_matches
