"""
Tests for normalization pipeline
"""
import unittest
from normalization.pipeline import NormalizationPipeline


class TestNormalizationPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = NormalizationPipeline()
    
    def test_supported_locales(self):
        """Test that supported locales are returned"""
        locales = self.pipeline.get_supported_locales()
        self.assertIn("hi-IN", locales)
        self.assertIn("ta-IN", locales)
    
    def test_hindi_number_normalization(self):
        """Test Hindi number normalization"""
        result = self.pipeline.normalize("123", "hi-IN")
        self.assertIn("normalized_text", result)
        self.assertIn("tokens", result)
        # Should normalize the number
        self.assertNotEqual(result["normalized_text"], "123")
    
    def test_hindi_currency_normalization(self):
        """Test Hindi currency normalization"""
        result = self.pipeline.normalize("₹250", "hi-IN")
        self.assertIn("normalized_text", result)
        # Should contain normalized currency
        self.assertIn("रुपये", result["normalized_text"])
    
    def test_tamil_number_normalization(self):
        """Test Tamil number normalization"""
        result = self.pipeline.normalize("123", "ta-IN")
        self.assertIn("normalized_text", result)
        # Should normalize the number
        self.assertNotEqual(result["normalized_text"], "123")
    
    def test_tamil_currency_normalization(self):
        """Test Tamil currency normalization"""
        result = self.pipeline.normalize("₹250", "ta-IN")
        self.assertIn("normalized_text", result)
        # Should contain normalized currency
        self.assertIn("ரூபாய்", result["normalized_text"])
    
    def test_unsupported_locale(self):
        """Test that unsupported locale raises error"""
        with self.assertRaises(ValueError):
            self.pipeline.normalize("test", "en-US")


if __name__ == '__main__':
    unittest.main()
