import os
import time
import argparse
import logging
from datetime import datetime, timedelta
import instaloader
import schedule

# Initialize Instaloader
L = instaloader.Instaloader()

# Define paths
usernames_file = '/Users/moisiferenc/instaloader/usernames.txt'
download_folder = '/Users/moisiferenc/instaloader/downloads'
log_file = '/Users/moisiferenc/instaloader/app.log'

# Ensure download folder exists
os.makedirs(download_folder, exist_ok=True)

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

def download_latest_images():
    try:
        logging.info("Starting download_latest_images")
        # Read usernames from file
        with open(usernames_file, 'r') as file:
            usernames = file.read().splitlines()
        logging.info(f"Usernames loaded: {usernames}")

        # Calculate date limits
        one_week_ago = datetime.now() - timedelta(weeks=1)
        one_month_ago = datetime.now() - timedelta(days=30)

        # Download images
        for username in usernames:
            try:
                logging.info(f"Processing username: {username}")
                profile = instaloader.Profile.from_username(L.context, username)
                if profile.is_private:
                    logging.info(f"Skipping private profile: {username}")
                    continue
                for post in profile.get_posts():
                    if post.date >= one_week_ago:
                        L.download_post(post, target=download_folder)
                        logging.info(f"Downloaded post from {username} dated {post.date}")
                        time.sleep(10)  # Add delay to avoid rate limiting
            except Exception as e:
                logging.error(f"Error downloading from {username}: {e}")
                if "Please wait a few minutes before you try again" in str(e) or "Redirected to login page" in str(e):
                    logging.info("Encountered rate limiting or login issue, waiting 10 minutes before retrying")
                    time.sleep(600)  # Wait 10 minutes before retrying
                    return

        # Delete images older than one month
        for filename in os.listdir(download_folder):
            file_path = os.path.join(download_folder, filename)
            if os.path.isfile(file_path):
                file_date = datetime.strptime(filename.split('_')[0], '%Y-%m-%d')
                if file_date < one_month_ago:
                    os.remove(file_path)
                    logging.info(f"Deleted old file: {filename}")
    except Exception as e:
        logging.error(f"Error in download_latest_images: {e}")

def main(debug):
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')

    if not username or not password:
        logging.error("Instagram username or password not set in environment variables")
        return

    while True:
        try:
            logging.info("Attempting to log in")
            # Login to Instagram
            try:
                L.login(username, password)
                logging.info("Login successful")
            except Exception as e:
                logging.error(f"Error logging in: {e}")
                logging.info("Waiting 10 minutes before retrying login")
                time.sleep(600)  # Wait 10 minutes before retrying
                continue

            if debug:
                logging.info("Running in debug mode")
                download_latest_images()
            else:
                logging.info("Scheduling task to run at 1 AM every day")
                # Schedule the task to run at 1 AM every day
                schedule.every().day.at("01:00").do(download_latest_images)

                # Keep the script running
                while True:
                    try:
                        schedule.run_pending()
                        time.sleep(60)
                    except Exception as e:
                        logging.error(f"Error in scheduled task: {e}")
                        logging.info("Waiting 10 minutes before retrying scheduled task")
                        time.sleep(600)  # Wait 10 minutes before retrying
        except Exception as e:
            logging.error(f"Error in main: {e}")
            logging.info("Waiting 10 minutes before retrying main loop")
            time.sleep(600)  # Wait 10 minutes before retrying

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download latest Instagram images.')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode to execute immediately.')
    args = parser.parse_args()

    main(args.debug)