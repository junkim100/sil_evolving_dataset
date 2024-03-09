from external import external_generation
from noise import noise_injection

import os
from datetime import datetime, timezone

def create_folders(current_date=None):
    """Create folders for the current date."""
    if current_date is None: current_date = datetime.now()
    os.makedirs(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/original/", exist_ok=True)
    os.makedirs(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/noisy/", exist_ok=True)
    os.makedirs(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/final/", exist_ok=True)

def main():
    create_folders()
    external_generation()
    noise_injection()

if __name__ == "__main__":
    main()