import unittest
from unittest.mock import patch, MagicMock
from LeetcodeWrapper import leetcode_Wrapper
from LeetcodeWrapper.exceptions import APIError


class TestLeetcodeWrapper(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.username = "test_user"
        self.api = leetcode_Wrapper(self.username)

    @patch("requests.get")
    def test_get_profile(self, mock_get):
        """Test the get_profile method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"username": "test_user"}
        mock_get.return_value = mock_response

        response = self.api.get_profile()
        self.assertEqual(response, {"username": "test_user"})
        mock_get.assert_called_once_with(f"https://alfa-leetcode-api.onrender.com/{self.username}", params=None)

    @patch("requests.get")
    def test_get_badges(self, mock_get):
        """Test the get_badges method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"name": "Badge1"}, {"name": "Badge2"}]
        mock_get.return_value = mock_response

        response = self.api.get_badges()
        self.assertEqual(response, [{"name": "Badge1"}, {"name": "Badge2"}])
        mock_get.assert_called_once_with(f"https://alfa-leetcode-api.onrender.com/{self.username}/badges", params=None)

    @patch("requests.get")
    def test_get_solved(self, mock_get):
        """Test the get_solved method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"solvedCount": 42}
        mock_get.return_value = mock_response

        response = self.api.get_solved()
        self.assertEqual(response, {"solvedCount": 42})
        mock_get.assert_called_once_with(f"https://alfa-leetcode-api.onrender.com/{self.username}/solved", params=None)

    @patch("requests.get")
    def test_get_contest_details(self, mock_get):
        """Test the get_contest_details method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"contests": []}
        mock_get.return_value = mock_response

        response = self.api.get_contest_details()
        self.assertEqual(response, {"contests": []})
        mock_get.assert_called_once_with(f"https://alfa-leetcode-api.onrender.com/{self.username}/contest", params=None)

    @patch("requests.get")
    def test_get_submissions(self, mock_get):
        """Test the get_submissions method with and without a limit."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"submissions": []}
        mock_get.return_value = mock_response

        # Test without limit
        response = self.api.get_submissions()
        self.assertEqual(response, {"submissions": []})
        mock_get.assert_called_with(f"https://alfa-leetcode-api.onrender.com/{self.username}/submission", params=None)

        # Test with limit
        response = self.api.get_submissions(limit=10)
        self.assertEqual(response, {"submissions": []})
        mock_get.assert_called_with(f"https://alfa-leetcode-api.onrender.com/{self.username}/submission?limit=10", params=None)

    @patch("requests.get")
    def test_error_handling(self, mock_get):
        """Test error handling when the API returns a non-200 status code."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        with self.assertRaises(APIError) as context:
            self.api.get_profile()

        self.assertIn("Error: 404", str(context.exception))
        mock_get.assert_called_once_with(f"https://alfa-leetcode-api.onrender.com/{self.username}", params=None)


if __name__ == "__main__":
    unittest.main()
