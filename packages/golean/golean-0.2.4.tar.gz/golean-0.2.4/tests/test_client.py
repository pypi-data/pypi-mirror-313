import unittest
from unittest.mock import patch, Mock
from golean import GoLean

class TestGoLeanClient(unittest.TestCase):
    def setUp(self):
        self.golean = GoLean(api_key="test_key")

    def test_init_with_key(self):
        self.assertEqual(self.golean.api_key, "test_key")

    @patch.dict('os.environ', {'GOLEAN_API_KEY': 'env_test_key'})
    def test_init_with_env_var(self):
        golean = GoLean()
        self.assertEqual(golean.api_key, "env_test_key")

    def test_init_without_key(self):
        with self.assertRaises(ValueError):
            GoLean()

    @patch('requests.Session.post')
    def test_compress_prompt(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"compressed_prompt": "Test compressed"}
        mock_post.return_value = mock_response

        result = self.golean.compress_prompt("contet")
        
        self.assertEqual(result, {"compressed_prompt": "Test compressed"})
        mock_post.assert_called_once()