from external import external_generation
from noise import noise_injection

import os
from datetime import datetime, timezone, timedelta

def create_folders(current_date=None):
    """Create folders for the current date"""
    if current_date is None: current_date = datetime.now(timezone(timedelta(hours=-7)))
    os.makedirs(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/original/", exist_ok=True)
    os.makedirs(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/noised/", exist_ok=True)

if __name__ == "__main__":
    create_folders()
    external_generation()
    noise_injection()