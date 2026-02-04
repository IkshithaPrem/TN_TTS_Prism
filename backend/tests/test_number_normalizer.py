"""
Tests for number normalization
"""
import unittest
from normalization.number_normalizer import NumberNormalizer


class TestNumberNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = NumberNormalizer()
        
        # Hindi number words
        self.hi_rules = {
            "words": {
                "ones": ["", "एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ", 
                         "दस", "ग्यारह", "बारह", "तेरह", "चौदह", "पंद्रह", "सोलह", "सत्रह", "अठारह", "उन्नीस"],
                "tens": ["", "दस", "बीस", "तीस", "चालीस", "पचास", "साठ", "सत्तर", "अस्सी", "नब्बे"],
                "hundreds": ["", "एक सौ", "दो सौ", "तीन सौ", "चार सौ", "पाँच सौ", "छह सौ", "सात सौ", "आठ सौ", "नौ सौ"],
                "thousands": ["हज़ार", "हज़ार"],
                "lakhs": ["लाख", "लाख"],
                "crores": ["करोड़", "करोड़"],
                "0": "शून्य"
            }
        }
        
        # Tamil number words
        self.ta_rules = {
            "words": {
                "ones": ["", "ஒன்று", "இரண்டு", "மூன்று", "நான்கு", "ஐந்து", "ஆறு", "ஏழு", "எட்டு", "ஒன்பது",
                         "பத்து", "பதினொன்று", "பன்னிரண்டு", "பதிமூன்று", "பதினான்கு", "பதினைந்து", "பதினாறு", "பதினேழு", "பதினெட்டு", "பத்தொன்பது"],
                "tens": ["", "பத்து", "இருபது", "முப்பது", "நாற்பது", "ஐம்பது", "அறுபது", "எழுபது", "எண்பது", "தொண்ணூறு"],
                "hundreds": ["", "நூறு", "இருநூறு", "முன்னூறு", "நானூறு", "ஐநூறு", "அறுநூறு", "எழுநூறு", "எண்ணூறு", "தொள்ளாயிரம்"],
                "thousands": ["ஆயிரம்", "ஆயிரம்"],
                "lakhs": ["லட்சம்", "லட்சம்"],
                "crores": ["கோடி", "கோடி"],
                "0": "பூஜ்யம்"
            }
        }
    
    def test_hindi_cardinal_simple(self):
        """Test simple Hindi cardinal numbers"""
        self.assertEqual(self.normalizer.normalize_cardinal("5", "hi-IN", self.hi_rules), "पाँच")
        self.assertEqual(self.normalizer.normalize_cardinal("10", "hi-IN", self.hi_rules), "दस")
        self.assertEqual(self.normalizer.normalize_cardinal("15", "hi-IN", self.hi_rules), "पंद्रह")
    
    def test_hindi_cardinal_tens(self):
        """Test Hindi tens"""
        self.assertEqual(self.normalizer.normalize_cardinal("20", "hi-IN", self.hi_rules), "बीस")
        self.assertEqual(self.normalizer.normalize_cardinal("25", "hi-IN", self.hi_rules), "बीस पाँच")
        self.assertEqual(self.normalizer.normalize_cardinal("50", "hi-IN", self.hi_rules), "पचास")
    
    def test_hindi_cardinal_hundreds(self):
        """Test Hindi hundreds"""
        self.assertEqual(self.normalizer.normalize_cardinal("100", "hi-IN", self.hi_rules), "एक सौ")
        self.assertEqual(self.normalizer.normalize_cardinal("250", "hi-IN", self.hi_rules), "दो सौ पचास")
        self.assertEqual(self.normalizer.normalize_cardinal("123", "hi-IN", self.hi_rules), "एक सौ बीस तीन")
    
    def test_tamil_cardinal_simple(self):
        """Test simple Tamil cardinal numbers"""
        self.assertEqual(self.normalizer.normalize_cardinal("5", "ta-IN", self.ta_rules), "ஐந்து")
        self.assertEqual(self.normalizer.normalize_cardinal("10", "ta-IN", self.ta_rules), "பத்து")
        self.assertEqual(self.normalizer.normalize_cardinal("15", "ta-IN", self.ta_rules), "பதினைந்து")
    
    def test_tamil_cardinal_tens(self):
        """Test Tamil tens"""
        self.assertEqual(self.normalizer.normalize_cardinal("20", "ta-IN", self.ta_rules), "இருபது")
        self.assertEqual(self.normalizer.normalize_cardinal("25", "ta-IN", self.ta_rules), "இருபது ஐந்து")
        self.assertEqual(self.normalizer.normalize_cardinal("50", "ta-IN", self.ta_rules), "ஐம்பது")
    
    def test_tamil_cardinal_hundreds(self):
        """Test Tamil hundreds"""
        self.assertEqual(self.normalizer.normalize_cardinal("100", "ta-IN", self.ta_rules), "நூறு")
        self.assertEqual(self.normalizer.normalize_cardinal("250", "ta-IN", self.ta_rules), "இருநூறு ஐம்பது")
        self.assertEqual(self.normalizer.normalize_cardinal("123", "ta-IN", self.ta_rules), "நூறு இருபது மூன்று")


if __name__ == '__main__':
    unittest.main()
