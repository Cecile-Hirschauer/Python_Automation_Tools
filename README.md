# Python Automation Tools

This repository contains several Python utility scripts for various common tasks.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Available Scripts](#available-scripts)
  - [YouTube Video Downloader](#youtube-video-downloader)
  - [Currency Converter](#currency-converter)
  - [Automatic Backup](#automatic-backup)
- [Tests](#tests)
- [Project Structure](#project-structure)
- [Environment](#environment)

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)
- Required modules listed in `requirements.txt`

## Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:Cecile-Hirschauer/python_automation.git
   cd python_automation
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Environment variable configuration (for the currency conversion script):

   Create a `.env` file at the root of the project with the following content:

   ```
   API_KEY=your_api_key
   BASE_URL=api_base_url
   ```

## Available Scripts

### YouTube Video Downloader

The `youtube.py` script allows you to download YouTube videos.

#### Usage

```bash
python youtube.py
```

The script will ask for:

1. The URL of the YouTube video to download
2. A destination directory (via a graphical dialog box)

#### Features

- Downloads YouTube videos in the best available quality
- Graphical interface for selecting the save folder
- Handles paths with tilde (~)
- Error handling

### Currency Converter

The `currency.py` script allows conversion between several international currencies.

#### Usage

```bash
python currency.py
```

The script will ask for the base currency for conversion, then display exchange rates for:

- USD (US Dollar)
- EUR (Euro)
- CAD (Canadian Dollar)
- GBP (British Pound)
- INR (Indian Rupee)

To quit, enter 'q'.

#### Required Configuration

The script requires a `.env` file containing your API key and the base URL of the currency conversion API.

### Automatic Backup

The `backup.py` script automatically creates daily backups of a specified folder.

#### Usage

By default, the script is configured to copy the folder `/home/cecile/Images/Screenshots` to `/home/cecile/Bureau/Backups` daily at 6:00 AM.

```bash
python backup.py
```

#### Customization

You can modify the `source_dir` and `destination_dir` variables in the script to change the source and destination folders. You can also modify the backup time by changing the parameter in `schedule.every().day.at("6:00")`.

## Tests

The project includes unit tests for the `currency.py` and `youtube.py` scripts.

To run the tests:

```bash
pytest
```

## Project Structure

```
.
├── backup.py               # Automatic backup script
├── currency.py             # Currency conversion script
├── requirements.txt        # List of dependencies
├── tests/                  # Folder containing tests
│   ├── test_currency.py    # Tests for currency.py
│   └── test_youtube.py     # Tests for youtube.py
└── youtube.py              # YouTube download script
```

## Environment

These scripts have been developed and tested in a Linux environment.

For scripts requiring a graphical interface (youtube.py), a desktop environment is required for folder selection.
