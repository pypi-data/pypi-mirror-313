import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from tolmate import tolmate, configure_behavior, show_popup

class TestToleranceChecker(unittest.TestCase):
    def setUp(self):
        """Set up environment for tests."""
        self.root = Tk()
        self.root.withdraw()  # Prevent Tkinter window from showing during tests
        configure_behavior(show_popup=False, show_message=False)  # Disable popups for testing

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_info_range(self):
        """Test if a value in the info range is correctly identified."""
        result = tolmate(15, 10, 20, 5, 25, 0, 30)
        self.assertTrue(result, "Value 15 should be within the info range [10, 20].")

    def test_soft_warning_range(self):
        """Test if a value in the soft warning range is correctly identified."""
        result = tolmate(23, 10, 20, 5, 25, 0, 30)
        self.assertTrue(result, "Value 23 should be within the soft warning range [5, 25].")

    def test_critical_warning_range(self):
        """Test if a value in the critical warning range is correctly identified."""
        result = tolmate(28, 10, 20, 5, 25, 0, 30)
        self.assertTrue(result, "Value 28 should be within the critical warning range [0, 30].")

    def test_error_out_of_range(self):
        """Test if a value out of all ranges is correctly identified as an error."""
        result = tolmate(35, 10, 20, 5, 25, 0, 30)
        self.assertFalse(result, "Value 35 should be out of all specified ranges.")

    @patch('tolmate.show_popup')
    def test_popup_behavior_info(self, mock_show_popup):
        """Test popup behavior for info messages."""
        configure_behavior(show_popup=True, show_message=False)
        tolmate(15, 10, 20, 5, 25, 0, 30)
        mock_show_popup.assert_called_with(
            value=15, level="info", title="->| Info |<-",
            message="Info: \nthe value \n\n15 \n\nis within \n\n[10,20]",
            limits=(10, 20, 5, 25, 0, 30)
        )

    @patch('tolmate.show_popup')
    def test_popup_behavior_error(self, mock_show_popup):
        """Test popup behavior for error messages."""
        configure_behavior(show_popup=True, show_message=False)
        tolmate(35, 10, 20, 5, 25, 0, 30)
        mock_show_popup.assert_called_with(
            level="error", title="->| Error |<- ",
            message="Error: \n\nthe value \n\n35 \n\nis outside specifications \n\n[0,30]",
            limits=(10, 20, 5, 25, 0, 30)
        )

    @patch('builtins.print')
    def test_console_message(self, mock_print):
        """Test if console messages are printed correctly."""
        configure_behavior(show_popup=False, show_message=True)
        tolmate(15, 10, 20, 5, 25, 0, 30)
        mock_print.assert_any_call("Info: the value 15 is within [10,20]")

    def test_no_popup_no_message(self):
        """Ensure no popups or messages are triggered when both are disabled."""
        configure_behavior(show_popup=False, show_message=False)
        with patch('tolmate.show_popup') as mock_popup, patch('builtins.print') as mock_print:
            result = tolmate(15, 10, 20, 5, 25, 0, 30)
            self.assertTrue(result)
            mock_popup.assert_not_called()
            mock_print.assert_not_called()

if __name__ == '__main__':
    unittest.main()

# running with
# python -m unittest .\test_tolmate.py