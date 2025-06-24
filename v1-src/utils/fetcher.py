import subprocess
import os
from urllib.parse import urlparse

def fetch_dataset(url):
    # Extract filename from URL
    filename = os.path.basename(urlparse(url).path)
    command = ['curl', '-o', filename, url]  # Save as filename

    try:
        subprocess.run(command, check=True)
        return True, filename
    except subprocess.CalledProcessError as e:
        print(f"Error fetching dataset: {e}")
        return False, None

def fetch_dataset_with_wget(url):
    filename = os.path.basename(urlparse(url).path)
    command = ['wget', '-O', filename, url]

    try:
        subprocess.run(command, check=True)
        return True, filename
    except subprocess.CalledProcessError as e:
        print(f"Error fetching dataset: {e}")
        return False, None