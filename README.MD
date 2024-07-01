# Automate Emails and Attachments Sending with Ease!
Take a list of emails/attachments, and send them to clients!

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Example Usage](#example-usage)

## Requirements
- Windows
- Python >= 3.11
- Outlook Desktop App

## Installation
- Clone this repository to your local machine (if you have git installed) by running the following command:
    ```bash
    gh repo clone eschallack/em-log
    ```
- Alternatively, download the zip file and extract it to your documents folder (or wherever you want to keep it).

- Run the following command to create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

- Navigate to `settings.py`, and configure your settings.

## Example Usage
```bash
python cli_main.py --find_pdfs
python cli_main.py --pw_protect
python cli_main.py --schedule_emails
python cli_main.py --send_emails
