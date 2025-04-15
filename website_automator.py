#!/usr/bin/env python3
"""
Utility script to open multiple predefined web pages in browser tabs.
"""

import sys
import webbrowser
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Predefined URL sets
URLS = {
    "work": ["indeed.com", "linkedin.com", "google.com"],
    "personal": ["https://www.udemy.com/", "deezer.com", "https://github.com/Cecile-Hirschauer"]
}


def normalize_url(url):
    """Ensure URL has a proper scheme prefix."""
    if not urlparse(url).scheme:
        return f"https://{url}"
    return url


def open_webpages(urls):
    """Open multiple webpages with error handling."""
    successful = 0
    failed = 0

    for url in urls:
        try:
            normalized_url = normalize_url(url)
            logging.info(f"Opening {normalized_url}")
            webbrowser.open_new_tab(normalized_url)
            successful += 1
        except Exception as e:
            logging.error(f"Failed to open {url}: {str(e)}")
            failed += 1

    return successful, failed


def main():
    """Main function for processing command-line arguments and opening webpages."""
    try:
        # Display usage help if no arguments or help flag
        if len(sys.argv) < 2 or sys.argv[1].lower() in ('-h', '--help'):
            print(f"Usage: python {sys.argv[0]} [set_name]")
            print(f"Available sets: {', '.join(URLS.keys())}")
            print("Or specify 'list' to see URLs in each set")
            return 0

        # Handle 'list' command to show available URL sets
        if sys.argv[1].lower() == 'list':
            print("Available URL sets:")
            for set_name, urls in URLS.items():
                print(f"\n{set_name}:")
                for url in urls:
                    print(f"  - {url}")
            return 0

        # Handle normal operation
        set_name = sys.argv[1].lower()
        if set_name not in URLS:
            logging.error(f"Unknown set name: '{set_name}'")
            print(f"Available sets: {', '.join(URLS.keys())}")
            return 1

        urls = URLS[set_name]
        successful, failed = open_webpages(urls)

        print(f"Summary: Opened {successful} pages successfully, {failed} failed")
        return 0 if failed == 0 else 1

    except KeyboardInterrupt:
        logging.info("Operation canceled by user")
        return 130
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())