import unittest
from unittest.mock import patch
from tolmate import configure_behavior, tolmate

class TestTolMate(unittest.TestCase):
    def setUp(self):
        """
        Setup default behavior for all tests.
        """
        configure_behavior(show_popup=False, show_message=False)

    @patch('builtins.print')
    def test_within_one_sigma(self, mock_print):
        """
        Test if a value within ±1σ is correctly identified as valid.
        """
        result = tolmate(25, 20, 40, 10, 50, 0, 60)
        self.assertTrue(result)
        mock_print.assert_called_with("Info: the value 25 is within [20,40]")

    @patch('builtins.print')
    def test_within_two_sigma(self, mock_print):
        """
        Test if a value within ±2σ is correctly identified as a warning.
        """
        result = tolmate(15, 20, 40, 10, 50, 0, 60)
        self.assertTrue(result)
        mock_print.assert_called_with("Soft Warning: The temperature is within [10,50]")

    @patch('builtins.print')
    def test_within_three_sigma(self, mock_print):
        """
        Test if a value within ±3σ is correctly identified as a critical warning.
        """
        result = tolmate(5, 20, 40, 10, 50, 0, 60)
        self.assertTrue(result)
        mock_print.assert_called_with("Critical Warning: the value 5 is within [0,60]")

    @patch('builtins.print')
    def test_out_of_specification(self, mock_print):
        """
        Test if a value outside all ranges is correctly identified as an error.
        """
        result = tolmate(-5, 20, 40, 10, 50, 0, 60)
        self.assertFalse(result)
        mock_print.assert_called_with("Error: the value -5 is out of specifications [0,60]")

    def test_behavior_configuration(self):
        """
        Test global behavior configuration for show_popup and show_message.
        """
        configure_behavior(show_popup=False, show_message=True)
        with patch('builtins.print') as mock_print:
            result = tolmate(15, 20, 40, 10, 50, 0, 60)
            self.assertTrue(result)
            mock_print.assert_called_with("Soft Warning: The temperature is within [10,50]")

        configure_behavior(show_popup=True, show_message=False)
        with patch('tolmate.show_popup') as mock_popup:
            result = tolmate(15, 20, 40, 10, 50, 0, 60)
            self.assertTrue(result)
            mock_popup.assert_called()

    @patch('tolmate.show_popup')
    def test_popup_invocation(self, mock_popup):
        """
        Test if the popup function is invoked when show_popup is enabled.
        """
        configure_behavior(show_popup=True, show_message=False)
        result = tolmate(25, 20, 40, 10, 50, 0, 60)
        self.assertTrue(result)
        mock_popup.assert_called()

    def test_no_behavior(self):
        """
        Test when both show_popup and show_message are disabled.
        """
        configure_behavior(show_popup=False, show_message=False)
        with patch('builtins.print') as mock_print, patch('tolmate.show_popup') as mock_popup:
            result = tolmate(25, 20, 40, 10, 50, 0, 60)
            self.assertTrue(result)
            mock_print.assert_not_called()
            mock_popup.assert_not_called()

if __name__ == "__main__":
    unittest.main()
