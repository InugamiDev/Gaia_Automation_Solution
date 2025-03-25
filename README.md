# Knowledge Check Screenshot Automation

This Python script automates the process of capturing screenshots from knowledge check questions on the Kurose & Ross Computer Networking website.

## Features

- Automatically navigates through each question in specified chapters and sections
- Selects correct answers for various question types (checkboxes, radio buttons, dropdowns, text inputs)
- Captures and saves screenshots of answered questions
- Organizes screenshots in a dedicated directory

## Prerequisites

- Python 3.x
- Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Installation

1. Clone or download this repository
2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Ensure ChromeDriver is in the project directory

## Configuration

The script processes questions from the following chapters and sections:
- Chapter 4: Sections 1, 3, 4
- Chapter 5: Sections 1, 2, 3, 4, 6
- Chapter 6: Sections 1, 2, 3, 4

To modify which chapters and sections to process, edit the `chapters_sections` dictionary in `CN.py`.

## Usage

1. Run the script:
   ```
   python CN.py
   ```

2. The script will:
   - Open Chrome browser
   - Navigate through each question
   - Select correct answers
   - Save screenshots in the 'screenshots' directory
   - Name screenshots as: `chapter{X}_section{Y}_question{Z}.png`

## Notes

- Screenshots are saved in the 'screenshots' directory
- The browser is maximized by default
- You can enable headless mode by uncommenting the headless option in the code