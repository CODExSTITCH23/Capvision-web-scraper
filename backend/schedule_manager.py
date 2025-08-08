import json
import os

SCHEDULE_FILE = "scraper_schedules.json"

def load_schedules():
    print(f"Loading schedules from: {os.path.abspath(SCHEDULE_FILE)}")
    if not os.path.exists(SCHEDULE_FILE):
        print("Schedule file does not exist.")
        return {}
    with open(SCHEDULE_FILE, "r") as f:
        data = json.load(f)
        print("Loaded schedules:", data)
        return data

def save_schedules(schedules):
    print(f"Saving schedules to: {os.path.abspath(SCHEDULE_FILE)}")
    print("Schedules to save:", schedules)
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedules, f, indent=2) 