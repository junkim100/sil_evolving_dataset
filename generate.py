from external import external_generation
from noise import noise_injection
from filtering import filter_data

import os
from datetime import datetime, timezone, timedelta

def create_folders(current_date=None):
    """Create folders for the current date"""
    if current_date is None: current_date = datetime.now(timezone(timedelta(hours=-16)))
    os.makedirs(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/original/", exist_ok=True)
    os.makedirs(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/noised/", exist_ok=True)
    os.makedirs(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/filtered/", exist_ok=True)

if __name__ == "__main__":
    create_folders()
    external_generation()
    noise_injection()
    filter_data(f"data/{datetime.now(timezone(timedelta(hours=-16))).strftime('%Y-%m-%d')}/dataset/")