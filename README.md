# Instagram Image Downloader

This project is a script to download the latest images from specified Instagram pages. The usernames of the Instagram pages are stored in a text file. The script runs daily at 1 AM, downloads images that are a maximum of 1 week old, and deletes images older than 1 month from the download folder.

## Features

- Downloads the latest images from specified Instagram pages.
- Skips private profiles.
- Runs daily at 1 AM.
- Deletes images older than 1 month.
- Logs all activities and errors to a log file.
- Retries login and download attempts in case of errors.

## Setup Guide

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/moisiFerenc/instaloader_project.git
    cd instaloader_project
    ```

2. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Create a [usernames.txt](http://_vscodecontentref_/1) file:**

    Create a file named [usernames.txt](http://_vscodecontentref_/2) in the project directory and add the Instagram usernames, one per line.

    ```sh
    echo "username1" >> /path/to/your/usernames.txt
    echo "username2" >> /path/to/your/usernames.txt
    ```

4. **Set environment variables for Instagram credentials:**

    ```sh
    export INSTAGRAM_USERNAME='your_instagram_username'
    export INSTAGRAM_PASSWORD='your_instagram_password'
    ```

5. **Update file paths in the script:**

    Open [main.py](http://_vscodecontentref_/3) and update the paths for [usernames_file](http://_vscodecontentref_/4), [download_folder](http://_vscodecontentref_/5), and [log_file](http://_vscodecontentref_/6) to match your system's directory structure.

    ```python
    # filepath: /path/to/your/main.py
    usernames_file = '/path/to/your/usernames.txt'
    download_folder = '/path/to/your/downloads'
    log_file = '/path/to/your/app.log'
    ```

6. **Run the script:**

    To run the script in debug mode (executes immediately):

    ```sh
    python3 /path/to/your/main.py --debug
    ```

    To run the script normally (schedules to run at 1 AM daily):

    ```sh
    python3 /path/to/your/main.py
    ```

### Logging

All activities and errors are logged to [app.log](http://_vscodecontentref_/7) in the project directory.

### Notes

- Ensure that the Instagram credentials are correct and have access to the profiles you want to download images from.
- The script handles rate limiting and login issues by retrying after a delay.
