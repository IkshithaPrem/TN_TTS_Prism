"""
SSML Generator for TTS
"""
from typing import Dict, List


class SSMLGenerator:
    """Generates SSML output for normalized text"""
    
    def generate(self, normalized_text: str, tokens: List[Dict], locale: str) -> str:
        """
        Generate SSML from normalized text and tokens
        """
        if not tokens:
            return f'<speak xml:lang="{locale}">{normalized_text}</speak>'
        
        # Map categories to SSML interpret-as values
        category_map = {
            "cardinal": "cardinal",
            "ordinal": "ordinal",
            "currency": "currency",
            "date": "date",
            "time": "time",
            "unit": "measure",
            "abbreviation": "characters"
        }
        
        # Build SSML with say-as tags
        ssml_parts = []
        last_pos = 0
        
        # Sort tokens by position
        sorted_tokens = sorted(tokens, key=lambda x: x.get("start", 0))
        
        for token in sorted_tokens:
            start = token.get("start", 0)
            end = token.get("end", start + len(token.get("original", "")))
            category = token.get("category", "")
            normalized = token.get("normalized", "")
            
            # Add text before token
            if start > last_pos:
                ssml_parts.append(normalized_text[last_pos:start])
            
            # Add token with SSML tag
            interpret_as = category_map.get(category, "characters")
            ssml_parts.append(f'<say-as interpret-as="{interpret_as}">{normalized}</say-as>')
            
            last_pos = end
        
        # Add remaining text
        if last_pos < len(normalized_text):
            ssml_parts.append(normalized_text[last_pos:])
        
        ssml_content = "".join(ssml_parts)
        return f'<speak xml:lang="{locale}">{ssml_content}</speak>'
