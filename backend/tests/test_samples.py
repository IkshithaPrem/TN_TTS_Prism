"""
Sample test sentences for each language
"""
import unittest
from normalization.pipeline import NormalizationPipeline


class TestSampleSentences(unittest.TestCase):
    """Test with real-world sample sentences"""
    
    def setUp(self):
        self.pipeline = NormalizationPipeline()
    
    def test_hindi_samples(self):
        """Test Hindi sample sentences"""
        samples = [
            "₹250 on 12/03/2024",
            "10:30AM पर मिलते हैं",
            "5kg चावल",
            "Dr. शर्मा आए",
            "123 लोग"
        ]
        
        for sample in samples:
            result = self.pipeline.normalize(sample, "hi-IN")
            self.assertIn("normalized_text", result)
            self.assertIsInstance(result["normalized_text"], str)
            print(f"Hindi: '{sample}' -> '{result['normalized_text']}'")
    
    def test_tamil_samples(self):
        """Test Tamil sample sentences"""
        samples = [
            "₹250 on 12/03/2024",
            "10:30AM க்கு வருகிறேன்",
            "5kg அரிசி",
            "Dr. குமார் வந்தார்",
            "123 பேர்"
        ]
        
        for sample in samples:
            result = self.pipeline.normalize(sample, "ta-IN")
            self.assertIn("normalized_text", result)
            self.assertIsInstance(result["normalized_text"], str)
            print(f"Tamil: '{sample}' -> '{result['normalized_text']}'")


if __name__ == '__main__':
    unittest.main()
