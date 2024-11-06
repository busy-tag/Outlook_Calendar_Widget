from datetime import datetime, timezone
import json

def read_config(drive_letter):
    file_path = f"{drive_letter}://config.json"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip() 
            config = json.loads(content)
            return config
    except FileNotFoundError:
        print(f"Config file not found at {file_path}.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from config file: {e}")
        return None

def update_config(config, drive_letter):
    config["show_after_drop"] = False
    config["activate_pattern"] = False

    file_path = f"{drive_letter}://config.json"

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the config file: {e}")

def config_setup(drive_letter):
    config = read_config(drive_letter)
    if config is None:
        print("Failed to load config.")
        return

    update_config(config, drive_letter)

def get_system_time():
    now_utc = datetime.now()
    return now_utc.strftime("%H:%M")

def get_busy_tag_drive_letter():
    while True:
        drive_letter = input("Enter the Busy Tag disk drive letter (e.g., D or E): ").strip().upper()

        if len(drive_letter) == 1 and drive_letter.isalpha():
            return drive_letter
        else:
            print("Invalid input. Please enter a single letter (e.g., D or E).")