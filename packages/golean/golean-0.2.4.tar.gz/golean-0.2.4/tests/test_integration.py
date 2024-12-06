import unittest
import os
from golean import GoLean

class TestGoLeanIntegration(unittest.TestCase):
    @unittest.skipIf(not os.getenv('GOLEAN_API_KEY'), "GOLEAN_API_KEY not set")
    def test_compress_prompt_integration(self):
        golean = GoLean()
        result = golean.compress_prompt(
            context="The quick brown fox jumps over the lazy dog."
        )
        
        print("Compression Result:", result)  # Print the result
        
        self.assertIn('compressed_prompt', result)
        self.assertIsInstance(result['compressed_prompt'], str)
