import sys
import os
import pytest
from unittest.mock import patch, MagicMock, call
from io import StringIO

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module to test
from website_automator import normalize_url, open_webpages, main


class TestWebsiteAutomator:
    """Test cases for the website_automator.py module."""

    def test_normalize_url(self):
        """Test that normalize_url adds https:// when protocol is missing."""
        # Without protocol
        assert normalize_url("example.com") == "https://example.com"
        # With protocol
        assert normalize_url("http://example.com") == "http://example.com"
        assert normalize_url("https://example.org") == "https://example.org"
        # With subdomain
        assert normalize_url("subdomain.example.com") == "https://subdomain.example.com"
        # With path
        assert normalize_url("example.com/path") == "https://example.com/path"

    @patch('webbrowser.open_new_tab')
    def test_open_webpages_success(self, mock_open):
        """Test open_webpages when all URLs open successfully."""
        # Mock successful opening of all URLs
        mock_open.return_value = True

        urls = ["https://example.com", "http://example.org"]
        successful, failed = open_webpages(urls)

        assert successful == 2
        assert failed == 0
        assert mock_open.call_count == 2
        mock_open.assert_has_calls([
            call("https://example.com"),
            call("http://example.org")
        ])

    @patch('webbrowser.open_new_tab')
    def test_open_webpages_partial_failure(self, mock_open):
        """Test open_webpages when some URLs fail to open."""
        # Mock first URL succeeds, second fails
        mock_open.side_effect = [True, Exception("Failed to open")]

        urls = ["https://example.com", "http://example.org"]
        successful, failed = open_webpages(urls)

        assert successful == 1
        assert failed == 1
        assert mock_open.call_count == 2

    @patch('webbrowser.open_new_tab')
    def test_open_webpages_all_failure(self, mock_open):
        """Test open_webpages when all URLs fail to open."""
        # Mock all URLs fail
        mock_open.side_effect = Exception("Failed to open")

        urls = ["https://example.com", "http://example.org"]
        successful, failed = open_webpages(urls)

        assert successful == 0
        assert failed == 2
        assert mock_open.call_count == 2

    @patch('website_automator.open_webpages')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_valid_set(self, mock_stdout, mock_open_webpages):
        """Test main function with valid set name."""
        # Mock successful opening of all URLs
        mock_open_webpages.return_value = (2, 0)

        # Mock sys.argv
        with patch('sys.argv', ['website_automator.py', 'work']):
            exit_code = main()

        # Check that open_webpages was called with correct URLs
        mock_open_webpages.assert_called_once()
        # Extract the first argument passed to open_webpages
        urls_arg = mock_open_webpages.call_args[0][0]
        assert 'google.com' in urls_arg
        assert exit_code == 0  # Success exit code

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_invalid_set(self, mock_stdout):
        """Test main function with invalid set name."""
        # Mock sys.argv with invalid set name
        with patch('sys.argv', ['website_automator.py', 'invalid_set']):
            exit_code = main()

        # Check output and exit code
        output = mock_stdout.getvalue()
        assert "Available sets:" in output  # This is what's actually printed to stdout
        assert exit_code == 1  # Error exit code

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_list_command(self, mock_stdout):
        """Test main function with 'list' command."""
        # Mock sys.argv with list command
        with patch('sys.argv', ['website_automator.py', 'list']):
            exit_code = main()

        # Check output and exit code
        output = mock_stdout.getvalue()
        assert "Available URL sets:" in output
        assert "work" in output
        assert "personal" in output
        assert exit_code == 0  # Success exit code

    @patch('website_automator.open_webpages')
    def test_main_keyboard_interrupt(self, mock_open_webpages):
        """Test main function handling of KeyboardInterrupt."""
        # Mock KeyboardInterrupt
        mock_open_webpages.side_effect = KeyboardInterrupt()

        # Mock sys.argv
        with patch('sys.argv', ['website_automator.py', 'work']):
            exit_code = main()

        assert exit_code == 130  # Standard exit code for SIGINT

    @patch('website_automator.open_webpages')
    def test_main_general_exception(self, mock_open_webpages):
        """Test main function handling of general exceptions."""
        # Mock general exception
        mock_open_webpages.side_effect = Exception("Test exception")

        # Mock sys.argv
        with patch('sys.argv', ['website_automator.py', 'work']):
            exit_code = main()

        assert exit_code == 1  # Error exit code