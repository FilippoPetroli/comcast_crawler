# Comcast crawler

This script automates the login process and the downloading of bills for specific accounts.

## Prerequisites

- Python 3+
- [camoufox](https://pypi.org/project/camoufox/) (managed in `requirements.txt`)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (also in `requirements.txt`)

## Installation

1. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate   # Windows
    ```

2. **Install the dependencies** from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Creating the `.env` File

Create a file named `.env` in the project's root directory following the template.

## Usage

To run the script, execute:

```bash
python main.py
